""" Initialize db schema """
import momoko
import psycopg2
import tornado.ioloop as ioloop
import tornado.gen as gen
from ships.sql import db
from ships.common import coro_engine


@gen.coroutine
def init():
    """ Helper to call db code after ioloop has started """
    print("Executing initialization")
    print(db.dsn)
    cursor = yield momoko.Op(
        db.execute,
        """
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
        CREATE TABLE game
        (
            game_id text PRIMARY KEY,
            players integer,
            state bytea,
            timestamp timestamp
        );
        CREATE UNIQUE INDEX ix_game_id
            ON game
            (game_id);
        CREATE INDEX ix_timestamp
            ON game
            (timestamp);
    """)
    try:
        print(cursor.fetchall())
    except psycopg2.ProgrammingError:
        pass
    io = ioloop.IOLoop.instance()
    io.stop()

def main():
    """ Initialize ioloop """
    io = ioloop.IOLoop.instance()
    io.add_callback(coro_engine(init))
    io.start()

if __name__ == "__main__":
    main()
