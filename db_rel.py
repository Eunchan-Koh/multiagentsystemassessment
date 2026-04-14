import os

import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from config import Config
# from utils import hash_schema, summary_creator, insert_info

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)

db = SessionLocal()

# select comparison
selectCom = {'SELECT', 'select', 'Select'}

# testing
def select_from_table(postgresql_query: str):
    print(f'DB_CONNECTION: select_from_table is called with postgresql_query: {postgresql_query}')
    
    if postgresql_query.split(" ")[0] not in selectCom:
        print(f"postgresql_query does not start with select: {postgresql_query}")
        return "postgresql_query does not start with select. Only SELECT postgresql_querys are allowed."
    
    try:
        # rows = db.session.execute(
        rows = db.execute(
            text(postgresql_query),
        ).fetchall()
        print(f"postgresql_query executed successfully. Retrieved rows: {rows}")
    except Exception as e:
        # db.session.rollback()
        db.rollback()
        print(f"Error executing postgresql_query: {postgresql_query}. Error: {e}")
        return f"Error executing postgresql_query: {e}"
    
    return rows

def get_table_info(table_name: str):
    """Return schema of the table with table_name. Not a tool! but can be added as a tool if needed."""
    print(f'get_table_info is called with table_name: {table_name}')
    
    try:
        # rows = db.session.execute(
        rows = db.execute(
            text(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = :t"),
            {"t": table_name}
        ).fetchall()
    except Exception as e:
        # db.session.rollback()
        db.rollback()
        print(f"Error retrieving table info for {table_name}: {e}")
        return {}
    
    schema = {}
    table = table_name
    try:
        for row in rows:
            if table not in schema:
                schema[table] = {"columns": {}}
            schema[table]["columns"][row.column_name] = row.data_type
    except Exception as e:
        print(f"Error processing rows for rows {rows}: {e}")
        return {}
      
    try:
        # to get primary key column  
        # row = db.session.execute(
        row = db.execute(
            text(f"\
                SELECT kcu.column_name \
                FROM information_schema.table_constraints AS tc\
                JOIN information_schema.key_column_usage AS kcu\
                ON tc.constraint_name = kcu.constraint_name\
                WHERE tc.table_name = :t\
                AND tc.constraint_type = 'PRIMARY KEY'\
                "),
            {"t": table_name}
            ).fetchone()
    except Exception as e:
        # db.session.rollback()
        db.rollback()
        print(f"Error retrieving primary key for {table_name}: {e}")
        row = None
        
    if table not in schema:
        if row is None:
            schema[table] = {"columns": {}}
        else:
            schema[table] = {"columns": {}, "PRIMARY KEY COLUMN": {}}
            # in theory, there is only one primary key column

    if row is not None:
        schema[table]["PRIMARY KEY COLUMN"] = row.column_name
    
    print(f'table schema is successfully retrieved.')
    return schema

