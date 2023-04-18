import pandas as pd
from google.protobuf.json_format import MessageToDict


def parseStream(stream, ignoreFields=None, pandas=True):
    """
    This one doesn't flatten the results, so you get multiple tables
    """
    tables = {}

    if ignoreFields is None:
        ignoreFields = ()

    for batch in stream:
        for row in batch.results:
            if hasattr(row, "_pb"):
                results_dict = MessageToDict(row._pb)
            else:
                results_dict = MessageToDict(row)

            for resource_name, values in results_dict.items():
                if resource_name not in tables:
                    tables[resource_name] = {}

                for col, value in values.items():
                    if col not in ignoreFields:
                        if col not in tables[resource_name]:
                            tables[resource_name][col] = []
                        tables[resource_name][col].append(value)

    if pandas:
        return toPandas(tables)
    return tables


def toPandas(tables):
    dfs = {}
    for table in tables:
        dfs[table] = pd.DataFrame.from_dict(tables[table])
    return dfs
