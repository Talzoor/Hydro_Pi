from RPi import GPIO
from time import sleep

COUNTER = 0
PIN     = 17     #fill pin no


class check_it():
    def tell_me_you_got_pulse(self, channel=None):
        global COUNTER
        GPIO.remove_event_detect(PIN)
        COUNTER += 1
        print("I got pulse now! pulse no:{}".format(COUNTER))
        sleep(2)
        GPIO.add_event_detect(PIN,
                              GPIO.RISING,
                              bouncetime=50, callback=self.tell_me_you_got_pulse)


def setup():
    global PIN

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(PIN,
                          GPIO.RISING,
                          bouncetime=50)  # 50mS
    check_test = check_it()
    GPIO.add_event_callback(PIN, check_test.tell_me_you_got_pulse)


def main():
    while True:
        pass    # do nothing, just wait for pulse


if __name__ == '__main__':
    setup()
    main()
