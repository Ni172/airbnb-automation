import signal
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--suite-timeout",
        action="store",
        type=int,
        default=None,
        help="Hard timeout for entire test suite in seconds"
    )

def timeout_handler(signum, frame):
    raise TimeoutError("❌ Test suite exceeded allowed timeout")

def pytest_sessionstart(session):
    timeout = session.config.getoption("--suite-timeout")
    if timeout:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)

def pytest_sessionfinish(session, exitstatus):
    signal.alarm(0)  # Disable alarm if session ends early
