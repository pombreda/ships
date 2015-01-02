""" Common functions """

import tornado.gen as gen

def coro_engine(coro):
    """Wrap coroutine to make it a engine. An engine
    will log exceptions when added as timeout, because
    it does't return a future."""
    # If tornado ever drops support of engine, convert this
    # to a coroutine that catches, logs and reraises any exception
    # because thats the goal of this method.
    @gen.engine
    def engine_func(*args, **kwargs):
        """Engine wrapper"""
        yield coro(*args, **kwargs)
    return engine_func
