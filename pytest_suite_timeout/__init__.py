import os
import sys
import threading

timer = None

def timeout_handler():
    print("❌ Test suite exceeded allowed timeout", file=sys.stderr)
    os._exit(1)

def pytest_addoption(parser):
    parser.addoption(
        "--suite-timeout",
        action="store",
        type=int,
        default=None,
        help="Hard timeout for entire test suite in seconds"
    )

def pytest_sessionstart(session):
    global timer
    timeout = session.config.getoption("--suite-timeout")
    if timeout:
        print(f"⏳ Setting up timeout watchdog: {timeout} seconds")
        timer = threading.Timer(timeout, timeout_handler)
        timer.start()

def pytest_sessionfinish(session, exitstatus):
    global timer
    if timer:
        timer.cancel()
