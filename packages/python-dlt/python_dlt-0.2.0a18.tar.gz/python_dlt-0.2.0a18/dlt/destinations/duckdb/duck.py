from typing import ClassVar, Dict, Optional

from dlt.common.arithmetics import DEFAULT_NUMERIC_PRECISION, DEFAULT_NUMERIC_SCALE
from dlt.common.destination import DestinationCapabilitiesContext
from dlt.common.schema import TColumnSchema, TDataType, TColumnHint, Schema

from dlt.destinations.insert_job_client import InsertValuesJobClient

from dlt.destinations.duckdb import capabilities
from dlt.destinations.duckdb.sql_client import DuckDbSqlClient
from dlt.destinations.duckdb.configuration import DuckDbClientConfiguration


SCT_TO_PGT: Dict[TDataType, str] = {
    "complex": "JSON",
    "text": "VARCHAR",
    "double": "DOUBLE",
    "bool": "BOOLEAN",
    "timestamp": "TIMESTAMP WITH TIME ZONE",
    "bigint": "BIGINT",
    "binary": "BLOB",
    "decimal": f"DECIMAL({DEFAULT_NUMERIC_PRECISION},{DEFAULT_NUMERIC_SCALE})"
}

PGT_TO_SCT: Dict[str, TDataType] = {
    "VARCHAR": "text",
    "JSON": "complex",
    "DOUBLE": "double",
    "BOOLEAN": "bool",
    "TIMESTAMP WITH TIME ZONE": "timestamp",
    "BIGINT": "bigint",
    "BLOB": "binary",
    "DECIMAL": "decimal"
}

HINT_TO_POSTGRES_ATTR: Dict[TColumnHint, str] = {
    "unique": "UNIQUE"
}


class DuckDbClient(InsertValuesJobClient):

    capabilities: ClassVar[DestinationCapabilitiesContext] = capabilities()

    def __init__(self, schema: Schema, config: DuckDbClientConfiguration) -> None:
        sql_client = DuckDbSqlClient(
            schema.normalize_make_dataset_name(config.dataset_name, config.default_schema_name, schema.name),
            config.credentials
        )
        super().__init__(schema, config, sql_client)
        self.config: DuckDbClientConfiguration = config
        self.sql_client: DuckDbSqlClient = sql_client  # type: ignore

    def _get_column_def_sql(self, c: TColumnSchema) -> str:
        hints_str = " ".join(HINT_TO_POSTGRES_ATTR.get(h, "") for h in HINT_TO_POSTGRES_ATTR.keys() if c.get(h, False) is True)
        column_name = self.capabilities.escape_identifier(c["name"])
        return f"{column_name} {self._to_db_type(c['data_type'])} {hints_str} {self._gen_not_null(c['nullable'])}"

    @staticmethod
    def _to_db_type(sc_t: TDataType) -> str:
        if sc_t == "wei":
            return "DECIMAL(38,0)"
        return SCT_TO_PGT[sc_t]

    @staticmethod
    def _from_db_type(pq_t: str, precision: Optional[int], scale: Optional[int]) -> TDataType:
        # duckdb provides the types with scale and precision
        pq_t = pq_t.split("(")[0].upper()
        if pq_t == "DECIMAL":
            if precision == 38 and scale == 0:
                return "wei"
        return PGT_TO_SCT[pq_t]
