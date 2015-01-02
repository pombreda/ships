""" Initialize db schema """
import psycopg2
import tornado.ioloop as ioloop
from ships.sql import db

def _done(cursor, error):
    """ Giving feedback """
    print("Intialization done: %s " % error)
    try:
        print(cursor.fetchall())
    except psycopg2.ProgrammingError:
        pass
    io = ioloop.IOLoop.instance()
    io.stop()

def init():
    """ Helper to call db code after ioloop has started """
    print("Executing initialization")
    print(db.dsn)
    db.execute("""
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
    """, callback=_done)

def main():
    """ Initialize ioloop """
    io = ioloop.IOLoop.instance()
    io.add_callback(init)
    io.start()

if __name__ == "__main__":
    main()
