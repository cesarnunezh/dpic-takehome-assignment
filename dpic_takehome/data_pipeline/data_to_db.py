import pandas as pd
from ..data_pipeline import cleaning
import sqlite3
from pathlib import Path
import os

def create_data_model(db_path = Path("data/dpic.db"), schema_path = Path("dpic_takehome/sql/schema.sql")):
    con = sqlite3.connect(db_path)
    with open(schema_path, 'r') as s:
        con.executescript(s.read())
    con.commit()
    con.close()

def describre_tables(db_path = Path("data/dpic.db")):
    
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        for table in ['grievances', 'iti_enrollments', 'districts', 'itis']:
            res = cur.execute(f'PRAGMA table_info({table})')
            print(f'\nTable name: {table}')
            for row in res:
                print(row)

def insert_data(db_path = Path("data/dpic.db")):
    if len(os.listdir(Path('data/clean'))) != 4:
        cleaning.main()
    
    tables = [file[:-4] for file in os.listdir(Path('data/clean')) if file.endswith('.csv')]

    with sqlite3.connect(db_path) as con:
        cur = con.cursor()

        for table in tables:
            df = pd.read_csv(Path(f'data/clean/{table}.csv'))

            cur.executemany(f'''INSERT INTO {table} VALUES ({"?,"*(len(df.columns) - 1)}?)''', df.values.tolist())
            con.commit()

def main(describre = False):
    create_data_model()
    insert_data()
    if describre:
        describre_tables()

if __name__ == '__main__':
    main()