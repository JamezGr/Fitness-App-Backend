# https://stackoverflow.com/questions/25188119/test-if-code-is-executed-from-within-a-py-test-session
def pytest_configure(config):
    import sys
    sys._TEST_MODE = True

def pytest_unconfigure(config):
    import sys
    del sys._TEST_MODE