from RPi import GPIO

COUNTER = 0
PIN     = 27     #fill pin no
PIN2    = 17


def tell_me_you_got_pulse(channel=None):
    global COUNTER
    COUNTER += 1
    print("I got pulse now! pulse no:{}".format(COUNTER))


def setup():
    global PIN, PIN2
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.IN)
    GPIO.setup(PIN2, GPIO.OUT)
    GPIO.output(PIN2, False)
    GPIO.add_event_detect(PIN, GPIO.RISING, callback=tell_me_you_got_pulse, bouncetime=50) # 50mS


def main():
    while True:
        pass # do nothing, just wait for pulse


if __name__ == '__main__':
    setup()
    main()
