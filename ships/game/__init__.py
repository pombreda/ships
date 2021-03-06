""" This package contains the actual game """

import logging as lg
import tornado.gen as gen
from ..base_game import BaseGame
from . import commands
import freeze

class Ships(BaseGame):
    """ The game ships """
    @gen.coroutine
    def on_command(self, command, state):
        """ Handle commands from the player """
        lg.debug("Command handled: %s", command)
        cmd_arr = command['command'].split(" ")
        cmd = getattr(commands, cmd_arr[0])
        res = cmd(state, *cmd_arr[1:])
        self.send_notify({
            'type': 'player_command',
            'player': self.player_id
        })
        return res


    @gen.coroutine
    def on_notify(self, notify, state):
        """ Handle notify from other players """
        lg.debug("Notify handled: %s", notify)
        if notify['type'] == 'player_command':
            self.socket.send_html(0, "Oppenent moved")
            self.visualize(state)

    @gen.coroutine
    def on_visualize(self, state):
        """ Visualize the current state for the current player """
        lg.debug("Visualize handled")
        return freeze.vformat(state)
