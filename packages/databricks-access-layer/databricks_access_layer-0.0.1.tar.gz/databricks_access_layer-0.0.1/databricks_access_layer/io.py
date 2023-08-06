def read_query(query_path: str) -> str:
    with open(query_path) as data:
        return data.read()
