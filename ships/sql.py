""" Initialize SQL source """

import os
import momoko
import urllib.parse as parse
import logging as lg
import getpass

parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])
_dsntpl = 'dbname=%(db)s user=%(usr)s password=%(pw)s host=%(hst)s port=%(prt)s'
user = url.username
if not user:
    user = getpass.getuser()
dsn=_dsntpl % {
    'db'   : url.path[1:],
    'usr'  : user,
    'pw'   : url.password,
    'hst'  : url.hostname,
    'prt'  : url.port,
}

lg.debug("Momoko dsn: %s", dsn)
db = momoko.Pool(
    dsn=dsn,
    size=2
)
