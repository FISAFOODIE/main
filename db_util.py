import logging

import os
import pandas as pd
from sqlalchemy import create_engine, inspect, text


DB_DIR = "data"


def get_database_names():
    return [f.rsplit(".", 1)[0] for f in os.listdir(DB_DIR) if f.endswith(".db")]


def get_table_names(db_name):
    engine = create_engine(f"sqlite:///{DB_DIR}/{db_name}.db")
    inspector = inspect(engine)

    return inspector.get_table_names()


def create_table_with_csv(csv_fname, db_name, table_name):
    df = pd.read_csv(csv_fname)
    engine = create_engine(f"sqlite:///{DB_DIR}/{db_name}.db", echo=True)
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)

    logging.info(f"Table {db_name}.{table_name} created with data from {csv_fname}")


def execute_query(db_name, query):
    engine = create_engine(f"sqlite:///{DB_DIR}/{db_name}.db")
    with engine.connect() as conn:
        query_exec = text(query)
        result = conn.execute(query_exec)

    return result.fetchall()