from RPi import GPIO

COUNTER = 0
PIN     = 17     #fill pin no


def tell_me_you_got_pulse(channel=None):
    global COUNTER
    COUNTER += 1
    print("I got pulse now! pulse no:{}".format(COUNTER))


def setup():
    global PIN

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(PIN,
                          GPIO.RISING,
                          bouncetime=50)  # 50mS
    GPIO.add_event_callback(PIN, tell_me_you_got_pulse)


def main():
    while True:
        pass    # do nothing, just wait for pulse


if __name__ == '__main__':
    setup()
    main()
