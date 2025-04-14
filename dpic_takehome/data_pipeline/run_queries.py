import sqlite3
import re
from pathlib import Path
import pandas as pd

def read_queries(path: Path):
    with open(path, 'r') as q:
        text = q.read()

    queries = re.split(r"--\s*\d+\.\s*", text)
    headers = re.findall(r"--\s*\d+\.\s*(.+)", text)
    queries = [q.strip() for q in queries if q.strip()]

    query_dict = {title.strip(): query.strip()[len(title)+1:] for title, query in zip(headers, queries)}
    return query_dict

def run_queries(db_path = Path('data/dpic.db'), query_file = Path('dpic_takehome/sql/queries.sql')):
    con = sqlite3.connect(db_path)
    queries = read_queries(query_file)

    result_tables = {}
    for table, query in queries.items():
        print(table)    
        df = pd.read_sql_query(query, con)
        result_tables[table] = df
        print(df)
    con.close()
    return result_tables

if __name__ == "__main__":
    run_queries()