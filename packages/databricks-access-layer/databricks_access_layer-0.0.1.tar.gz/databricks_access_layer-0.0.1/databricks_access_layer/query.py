from databricks_access_layer.io import read_query


class Query:
    def __init__(self, query: str) -> None:
        self.query = read_query(query) if query.endswith(".sql") else query

    @property
    def sql(self) -> str:
        # ToDo: support jinja and accept params
        return self.query

    def __str__(self) -> str:
        return self.sql
