import os
from typing import Optional

import psycopg2
from psycopg2 import Error

from config import Config


def insert_user(name: str, email: str, age: Optional[int]) -> None:
    # Using default env value for now - in actual env, it will be better to set .env file and use Config class to manage env variables
    db_host = Config.DB_HOST
    db_port = Config.DB_PORT
    db_name = Config.DB_NAME
    db_user = Config.DB_USER
    db_password = Config.DB_PASS

    try:
        # DB conenction
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password,
        )

        try:
            with conn.cursor() as cur:
                # create sample table is not exists
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        age INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )

                # 값 삽입
                cur.execute(
                    """
                    INSERT INTO users (name, email, age)
                    VALUES (%s, %s, %s)
                    """,
                    (name, email, age),
                )

            conn.commit()
            print("successfully inserted user data.")

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

    except Error as e:
        print(f"DB error: {e}")

# sample user data for testing
user_infos = [
    {"name": "John Doe", "email": "john.doe@example.com", "age": 25},
    {"name": "Jane Doe", "email": "jane.doe@example.com", "age": 28},
    {"name": "Jane Smith", "email": "jane.smith@example.com", "age": 30},
    {"name": "Alice Johnson", "email": "alice.johnson@example.com", "age": 35},
    {"name": "Bob Brown", "email": "bob.brown@example.com", "age": 40},
]

if __name__ == "__main__":
    for user_info in user_infos:
        insert_user(
            name=user_info["name"],
            email=user_info["email"],
            age=user_info["age"],
        )