import os
import threading
from pathvalidate import is_valid_filepath
from typing import Any, ClassVar, Final, List, Optional

from dlt.common.configuration import configspec
from dlt.common.configuration.specs import ConnectionStringCredentials
from dlt.common.configuration.specs.exceptions import InvalidConnectionString
from dlt.common.destination import DestinationClientDwhConfiguration
from dlt.common.typing import DictStrAny, TSecretValue

DEFAULT_DUCK_DB_NAME = "quack.duckdb"


@configspec
class DuckDbCredentials(ConnectionStringCredentials):
    drivername: Final[str] = "duckdb" # type: ignore
    password: Optional[TSecretValue] = None
    username: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None

    read_only: bool = False  # open database read/write

    # __config_gen_annotations__: ClassVar[List[str]] = ["database"]

    def borrow_conn(self, read_only: bool, config: DictStrAny = None) -> Any:
        import duckdb

        if not hasattr(self, "_conn_lock"):
            self._conn_lock = threading.Lock()

        # obtain a lock because duck releases the GIL and we have refcount concurrency
        with self._conn_lock:
            if not hasattr(self, "_conn"):
                self._conn = duckdb.connect(database=self.database, read_only=read_only, config=config)
                self._conn_owner = True
                self._conn_borrows = 0

            # track open connections to properly close it
            self._conn_borrows += 1
            # print(f"getting conn refcnt {self._conn_borrows} at {id(self)}")
            return self._conn.cursor()

    def return_conn(self, borrowed_conn: Any) -> None:
        # print(f"returning conn refcnt {self._conn_borrows} at {id(self)}")
        # close the borrowed conn
        borrowed_conn.close()

        with self._conn_lock:
            # close the main conn if the last borrowed conn was closed
            assert self._conn_borrows > 0, "Returning connection when borrows is 0"
            self._conn_borrows -= 1
            if self._conn_borrows == 0 and self._conn_owner:
                self._delete_conn()

    def parse_native_representation(self, native_value: Any) -> None:
        try:
            # check if database was passed as explicit connection
            import duckdb
            if isinstance(native_value, duckdb.DuckDBPyConnection):
                self._conn = native_value
                self._conn_owner = False
                self._conn_borrows = 0
                self.database = ":external:"
                return
        except ImportError:
            pass
        try:
            super().parse_native_representation(native_value)
        except InvalidConnectionString:
            if is_valid_filepath(native_value, platform="auto"):
                self.database = native_value
            else:
                raise

    def on_resolved(self) -> None:
        # if database is not set, try the pipeline context
        if not self.database:
            self.database = self._path_in_pipeline(DEFAULT_DUCK_DB_NAME)
        # if pipeline context was not present
        if not self.database:
            # create database locally
            self.database = DEFAULT_DUCK_DB_NAME
        # always make database an abs path
        self.database = os.path.abspath(self.database)

    def _path_in_pipeline(self, rel_path: str) -> str:
        from dlt.common.configuration.container import Container
        from dlt.common.pipeline import PipelineContext
        context = Container()[PipelineContext]
        if context.is_active():
            # pipeline is active, get the working directory
            return os.path.join(context.pipeline().working_dir, rel_path)
        return None

    def _delete_conn(self) -> None:
        # print("Closing conn because is owner")
        self._conn.close()
        delattr(self, "_conn")

    def __del__(self) -> None:
        # print("Bye duck")
        if hasattr(self, "_conn") and self._conn_owner:
            self._delete_conn()


@configspec(init=True)
class DuckDbClientConfiguration(DestinationClientDwhConfiguration):
    destination_name: Final[str] = "duckdb"  # type: ignore
    credentials: DuckDbCredentials
