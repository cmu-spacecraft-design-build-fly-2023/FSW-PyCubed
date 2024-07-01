import time


def collect():
    """
    emulate gc.collect() by waiting a short time
    """
    time.sleep(0.001)


def mem_free():
    """
    just returns a constant value for now
    """
    return 1024 * 30
