import atexit
import multiprocessing
import threading
from multiprocessing.connection import Listener as MPL, Client
from typing import Callable, Dict
from queue import Queue

__all__ = ['Listener', 'Sender']


class Listener:
    def __init__(self, key: str):
        pipe = r'\\.\pipe\{}'.format(key.replace("-", ""))
        print(pipe)
        self.server = MPL(pipe, family='AF_PIPE', authkey=key.encode())
        self.thread = threading.Thread(name=repr(self), target=self._loop, daemon=True)
        self.callbacks: Dict[str, Callable] = {}
        self.queue: "Queue[Callable]" = Queue(1)
        atexit.register(self._cleanup)

    def _loop(self):
        while True:
            try:
                with self.server.accept() as con:
                    msg = con.recv()
            except multiprocessing.AuthenticationError:
                continue

            self.run_callback(self.callbacks.get(msg, lambda: print(f'no such callbacks: {msg}')))

    def run_callback(self, func: Callable):
        """
        call function callback, or put it in queue
        :param func: callback's function object
        :return:
        """
        if hasattr(func, 'rimt'):  # put func to queue
            self.queue.put(func)
        else:
            func()

    def start(self):
        self.thread.start()
        print(f"Thread {self.thread.name}, {self.thread.is_alive()}")

    def _cleanup(self):
        self.server.close()


class Sender:
    def __init__(self, key: str):
        pipe = rf"\\.\pipe\{key.replace('-', '')}"
        connected = False
        while not connected:
            try:
                self.con = Client(pipe, family='AF_PIPE', authkey=key.encode())
                connected = True
            except multiprocessing.AuthenticationError:
                continue

    def send(self, data):
        self.con.send(data)
        self.con.close()

