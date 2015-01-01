""" Security related function """

import hashlib
from . import settings as s

def client_verify(game, player):
    """ Verifies if websocket belongs to client """
    secstr = "%s%s%s" % (game, int(player), s.SECRET)
    secstr = secstr.encode(s.ENCODING)
    return hashlib.sha512(
    ).hexdigest()
