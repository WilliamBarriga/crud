# Psycopg2
import psycopg2
from psycopg2.extensions import connection, cursor
from psycopg2.errors import InFailedSqlTransaction, DuplicateTable

# Env
from decouple import config


class DBManager:
    def __init__(self) -> None:
        self.conn = self.connect()

    def _check_connection(func):
        def wrapper(self, *args, **kwargs):
            if self.conn.closed:
                self.conn = self.connect()
            try:
                return func(self, *args, **kwargs)
            except InFailedSqlTransaction:
                self.conn.rollback()
                self.conn.close()
                self.conn = self.connect()
                return func(self, *args, **kwargs)
            except Exception as e:
                if not self.conn.closed:
                    self.conn.rollback()
                    self.conn.close()
                self.conn = self.connect()
                detail = "Something went wrong with the database: "
                raise Exception(f"{detail} {e}")

        return wrapper

    def connect(self) -> connection:
        """Connect to database"""
        conn = psycopg2.connect(
            host=config("DATABASE_HOST"),
            dbname=config("DATABASE_NAME"),
            user=config("DATABASE_USER"),
            password=config("DATABASE_PASS"),
            port=config("DATABASE_PORT"),
        )
        return conn

    def create_db(self) -> None:
        """validate the created tables and recreate db if its necessary"""
        print("create db ----", flush=True)
        cur = self.conn.cursor()
        cur.execute(open("commons/db_creation.sql", "r").read())
        cur.close()
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    @_check_connection
    def sp(self, sp: str, args: list[str]) -> list[dict]:
        """execute a stored procedure

        Args
        sp: name of the stored procedure
        args: args for the stored procedure write on format value::cast ('example'::varchar)
        """
        cur = self.conn.cursor()

        stm = f"select * from {sp}({', '.join(args)})"
        cur.execute(stm)
        self.conn.commit()

        columns = [column[0] for column in cur.description]

        data = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()
        return data


db = DBManager()
