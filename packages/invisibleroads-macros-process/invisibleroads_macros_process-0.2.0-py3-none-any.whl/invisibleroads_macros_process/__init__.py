import os
import signal
from logging import getLogger
from multiprocessing import Process


class LoggableProcess:

    def __init__(self, Class=Process, *args, **kwargs):
        self.instance = Class(*args, **kwargs)

    def start(self, *args, **kwargs):
        instance = self.instance
        instance.start(*args, **kwargs)
        L.debug(
            'started %s%s process %s', instance.name,
            ' daemon' if instance.daemon else '', instance.ident)

    def join(self, *args, **kwargs):
        instance = self.instance
        instance.join(*args, **kwargs)


class StoppableProcess(LoggableProcess):

    def stop(
            self,
            sigint_timeout_in_seconds=5,
            sigkill_timeout_in_seconds=1):
        '''
        Stop the process using SIGINT and, if necessary, SIGKILL.
        https://github.com/samuelcolvin/watchfiles/blob/main/watchfiles/run.py
        '''
        instance = self.instance
        if not instance.is_alive():
            return
        name = instance.name
        ident = instance.ident
        process_id = instance.pid
        L.debug('interrupting %s process %s', name, ident)
        try:
            os.kill(process_id, signal.SIGINT)
        except OSError:
            return
        instance.join(sigint_timeout_in_seconds)
        if instance.exitcode is None:
            L.debug('killing %s process %s', name, ident)
            os.kill(process_id, signal.SIGKILL)
            instance.join(sigkill_timeout_in_seconds)


L = getLogger(__name__)
