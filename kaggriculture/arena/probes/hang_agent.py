"""Adversarial cluster probe: disable the child timer and never return."""
import signal
import time


def agent(observation, configuration=None):
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    signal.setitimer(signal.ITIMER_REAL, 0)
    while True:
        time.sleep(.05)
