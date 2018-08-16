import RPi.GPIO as GPIO
PIN_TAP_1 = 2

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
