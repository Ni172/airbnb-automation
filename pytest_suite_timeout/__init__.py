import signal
import pytest
import time

def pytest_addoption(parser):
    parser.addoption(
        "--suite-timeout",
        action="store",
        type=int,
        default=None,
        help="Fail the entire test suite if it exceeds this timeout in seconds"
    )

def timeout_handler(signum, frame):
    raise TimeoutError("❌ Test suite exceeded allowed timeout")

def pytest_sessionstart(session):
    timeout = session.config.getoption("--suite-timeout")
    if timeout:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)  # Set global alarm
        session._alarm_set = True

def pytest_sessionfinish(session, exitstatus):
    if getattr(session, "_alarm_set", False):
        signal.alarm(0)  # Disable alarm
