import RPi.GPIO as GPIO
from Pi_switch.Pi_switch_main import PIN_TAP_1

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_TAP_1, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.output(PIN_TAP_1, False)

    while True:
        pass

finally:
    GPIO.output(PIN_TAP_1, True)
    GPIO.cleanup()
    print("Bye.")
