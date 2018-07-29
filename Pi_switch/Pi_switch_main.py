
import time
from time import sleep

PIN_TAP_1 = 00
PIN_TAP_2 = 00

Tap_open = False


def main():
    if Tap_open:
        check_flow(5)


def check_flow(_int_period):
    flow_flag = False
    millis = int(round(time.time() * 1000))
    time_now = millis
    while (time_now - millis) < (_int_period * 1000):  # wait to see if flowing
        time_now = int(round(time.time() * 1000))
        if
        sleep(0.5/1000.0)   # 0.5mS


