import pandas as pd

def fetch_data(cnxn):
    query = "SELECT * FROM [dbo].[customer]"
    print(query)
    df = pd.read_sql(query, cnxn)
    return df