import pandas as pd
import snowflake.connector
from snowflake.connector import DictCursor

from databricks_access_layer.credentials import SnowflakeCredentials
from databricks_access_layer.query import Query


class DBConnector:
    def __init__(self, credentials: SnowflakeCredentials) -> None:
        self.__conn = snowflake.connector.connect(
            user=credentials.username,
            password=credentials.password,
            account=credentials.account,
            database=credentials.database,
            warehouse=credentials.warehouse,
            role=credentials.role,
            region=credentials.region,
        )

    def __fetch_data(self, query: Query) -> list[dict]:
        cs = self.__conn.cursor(DictCursor)
        cs.execute(query.sql)
        return cs.fetchall()  # type: ignore

    def get_data_df(self, query: Query) -> pd.DataFrame:
        results = self.__fetch_data(query)
        return pd.DataFrame(results)

    def get_data_dict(self, query: Query) -> list[dict]:
        results = self.__fetch_data(query)
        return results
