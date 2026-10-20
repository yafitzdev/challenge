"""Minimal stand-in for an Android Handler / view message queue.

Callbacks posted with post_delayed are kept in a pending list; there is no
running looper, so they only execute when ``run_pending`` is called.
"""
import time


def now_millis():
    return int(time.time() * 1000)


class Handler:
    def __init__(self, queue=None):
        self.queue = queue if queue is not None else []

    def post_delayed(self, runnable, delay_ms):
        self.queue.append((runnable, delay_ms))
        return True

    def remove_callbacks(self, runnable):
        self.queue[:] = [e for e in self.queue
                         if not (isinstance(e, tuple) and e and e[0] is runnable)]

    def run_pending(self):
        pending = list(self.queue)
        self.queue[:] = []
        for entry in pending:
            if isinstance(entry, tuple):
                entry[0]()
