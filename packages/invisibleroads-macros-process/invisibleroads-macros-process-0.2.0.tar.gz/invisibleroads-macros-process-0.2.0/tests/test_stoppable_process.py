import signal
from time import sleep

from invisibleroads_macros_process import StoppableProcess


def test_stoppable_process_stops(mocker):
    log_mock = mocker.patch('invisibleroads_macros_process.L')

    def f():
        sleep(1)

    process = StoppableProcess(name='test', target=f, daemon=True)
    process.start()
    process.stop()
    assert log_mock.debug.call_count == 2


def test_stoppable_process_dies(mocker):
    log_mock = mocker.patch('invisibleroads_macros_process.L')

    def f():
        sleep(1)

    def g(signal_number, stack_frame):
        sleep(7)

    signal.signal(signal.SIGTERM, g)
    process = StoppableProcess(name='test', target=f, daemon=True)
    process.start()
    process.stop()
    assert log_mock.debug.call_count == 3
