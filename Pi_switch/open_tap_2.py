import RPi.GPIO as GPIO
PIN_TAP_2 = 3

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_TAP_2, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.output(PIN_TAP_2, False)

    while True:
        pass

except KeyboardInterrupt:
    print("Bye")

finally:
    GPIO.output(PIN_TAP_2, True)
    GPIO.cleanup()
