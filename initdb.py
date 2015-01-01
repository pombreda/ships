""" Initialize db schema """

import sqlalchemy
import os

engine = sqlalchemy.create_engine(os.environ['DATABASE_URL'])

with engine.begin() as conn:
    conn.execute("""
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
    """)



