from invisibleroads_macros_process import LoggableProcess


def test_loggable_process_starts(mocker):
    log_mock = mocker.patch('invisibleroads_macros_process.L')

    def f():
        pass

    process = LoggableProcess(name='test', target=f, daemon=True)
    process.start()
    process.join()
    log_mock.debug.assert_called()
