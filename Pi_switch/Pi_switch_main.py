
import time
from time import sleep
import sys
import RPi.GPIO as GPIO
#from Pi_flow import Pi_flow_main
import socket
from datetime import datetime
import linecache

try:
    from .tools.logger import Logger
except ImportError:
    from tools.logger import Logger
try:
    from .Pi_flow import Pi_flow_main
except ImportError:
    from Pi_flow import Pi_flow_main
try:
    from .tools.email_script import SendEmail
except ImportError:
    from tools.email_script import SendEmail

PIN_TAP_1           = 2
PIN_TAP_2           = 3
PIN_MICRO_SWITCH    = 17
FLOW_PIN            = Pi_flow_main.FLOW_PIN

WATER_LEVEL_SWITCH  = False
CHECK_EVERY         = 1  # ms(100)    # 100mS
DEBUG_PRINT_EVERY   = 60

FLOW_COUNT          = 0
SOLENOID_OPEN       = 0

NEED_TO_CLOSE       = 0     # if 0 ok, if num = no. of failed attempts

LOG                 = None      # logger instance
LOG_NAME            = "Pi_switch.log"
LOG_FILE_W_PATH     = ""

MICRO_S_CHANGE      = False

TIME_S = int(round(time.time()))
EMAIL_ALRETS        = True
DEBUG_FLOWING_SWITCH = 26
DEBUG                = False


def init_import_project_modules():
    _tmp_dir = sys.argv[0]
    this_project_dir = _tmp_dir[:_tmp_dir.rfind("/")]
    main_project_dir = this_project_dir[:this_project_dir.rfind("/")]

    sys.path.append(main_project_dir)


def micro_s_func(var=None):
    global WATER_LEVEL_SWITCH, MICRO_S_CHANGE, NEED_TO_CLOSE

    try:
        sleep(ms(5))
        state = not GPIO.input(PIN_MICRO_SWITCH)
        # GPIO.output(PIN_TAP_1, int(state))
        # GPIO.output(PIN_TAP_2, int(state))

        LOG.debug("State: {}".format(state))
        WATER_LEVEL_SWITCH = state
        MICRO_S_CHANGE = True
        if state:
            NEED_TO_CLOSE = False
        else:
            NEED_TO_CLOSE = True

    except:
        raise_exception("micro_s_func")

#def flow_change(var):
#    bool_flowing = True
#    pass


def logger_init():
    global LOG, LOG_NAME, LOG_FILE_W_PATH
    running_file = sys.path[0]
    running_path = str(running_file)[:running_file.rfind("/")]
    log_file_full_path = "{}/{}".format(running_path, LOG_NAME)

    print("running_file:{}".format(running_file))
    print("running_path:{}".format(running_path))
    print("log_file_full_path:{}".format(log_file_full_path))
    logger_class = Logger(log_file_full_path, "Pi switch")
    LOG = logger_class.logger
    LOG_FILE_W_PATH = logger_class.log_file_name


def setup():
    try:
        init_import_project_modules()
        logger_init()

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(PIN_TAP_1, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(PIN_TAP_2, GPIO.OUT, initial=GPIO.HIGH)

        GPIO.setup(PIN_MICRO_SWITCH,        GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(FLOW_PIN,                GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(DEBUG_FLOWING_SWITCH,    GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(PIN_MICRO_SWITCH, GPIO.BOTH, callback=micro_s_func, bouncetime=2)
        GPIO.add_event_detect(FLOW_PIN,         GPIO.FALLING,    callback=flow_in_count, bouncetime=5)

        print_header()
        micro_s_func()      # init 'WATER_LEVEL_SWITCH' var
        # open_solenoid(0)

    except:
        raise_exception("setup")


def print_header():
    str_debug = (DEBUG is True) and " DEBUG MODE" or ""
    LOG.info('\n\n--- Main started ({}){} ---'.format(datetime.now().strftime('%Y-%m-%d  %H:%M:%S'), str_debug))
    LOG.info('GPIO:{}, Python:{}'.format(GPIO.VERSION, sys.version.replace('\n', ',')))
    name_rpi = socket.gethostname()
    LOG.info("running on: {}".format(name_rpi))
    LOG.info("log file: {}".format(LOG_FILE_W_PATH))
    LOG.debug("sys.argv[0] is {}".format(repr(sys.argv[0])))
    LOG.debug("__file__ is {}".format(repr(__file__)))


def main():
    global NEED_TO_CLOSE, MICRO_S_CHANGE, WATER_LEVEL_SWITCH
    try:
        LOG.debug("Flow_pin:{}".format(FLOW_PIN))
        time_start = int(round(time.time()))
        debug_print = True

        while True:
            time_now = int(round(time.time()))

            if WATER_LEVEL_SWITCH:
                MICRO_S_CHANGE = False
                if SOLENOID_OPEN == 0:
                    open_solenoid(1)                # open tap_1
                    # LOG.info("opening tap 1")
                flowing = check_flow(5)             # check to see if there is water flow
                if not flowing:
                    if NEED_TO_CLOSE:
                        open_solenoid(0)
                    else:
                        if SOLENOID_OPEN == 1:
                            open_solenoid(2)            # open tap_2
                        flowing = check_flow(5)
                        if not flowing:
                            something_wrong("NO WATER")
                            open_solenoid(0)
                            # error! send email no water
            else:                                    # water_level == False (micro off)

                if NEED_TO_CLOSE:
                    open_solenoid(0)
                    flowing = check_flow(1)
                    while flowing:
                        LOG.info("closing taps")
                        open_solenoid(0)
                        flowing = check_flow(2)
                        NEED_TO_CLOSE += 1
                        if NEED_TO_CLOSE > 5:
                            something_wrong("DRIPPING")
                            # error! send email DRIPPING
                        LOG.debug("flowing:{}".format(flowing))
                        if MICRO_S_CHANGE:
                            MICRO_S_CHANGE = False
                            break
                    NEED_TO_CLOSE = 0
                else:
                    flowing = check_flow(1)
                    if flowing:
                        open_solenoid(0)
                        NEED_TO_CLOSE += 1
                        if NEED_TO_CLOSE > 5:
                            something_wrong()
                            # error! send email DRIPPING
                    else:
                        if debug_print: LOG.debug("all good, all closed")

            if debug_print: LOG.debug("flowing:{}".format(flowing))
            sleep(CHECK_EVERY)

            debug_print = False

            if time_now - time_start > DEBUG_PRINT_EVERY:
                time_start = time_now
                debug_print = True


    except KeyboardInterrupt:
        LOG.info("Keyboard Exc.")
        raise KeyboardInterrupt
    except:
        raise_exception("main")

    finally:
        close()


def check_flow(_int_period):
    global FLOW_COUNT, MICRO_S_CHANGE

    # count as least 10 ticks to consider 'flow state'
    time_start = int(round(time.time()))
    time_now = time_start

    while (time_now - time_start) < (_int_period):  # wait to see if flowing
        sleep(ms(5))  # 0.5mS
        if DEBUG: flow_in_count_prog()
        time_now = int(round(time.time()))
        if MICRO_S_CHANGE:
            MICRO_S_CHANGE = False
            break

    if FLOW_COUNT > 4:
        LOG.info("Flow count during {} sec: {}".format(time_now - time_start, FLOW_COUNT))
    #FLOW_COUNT = 0

    return FLOW_COUNT > 10


def flow_in_count():
    global FLOW_COUNT
    FLOW_COUNT += 1


def flow_in_count_prog():
    global FLOW_COUNT, TIME_S
    time_now = int(round(time.time()))

    if FLOW_COUNT > 500: FLOW_COUNT = 0
    #if time_now - TIME_S > 10: FLOW_COUNT = 0
    state = not GPIO.input(DEBUG_FLOWING_SWITCH)
    if state:
        FLOW_COUNT += 1
    else:
        FLOW_COUNT = 0


def close(_code=None):
    GPIO.cleanup()
    LOG.debug("Bye.")
    exit(_code is None and 0 or _code)


def ms(_int_ms):
    return float(_int_ms) / 1000.0


def open_solenoid(_int_tap_number):
    global SOLENOID_OPEN
    try:
        if _int_tap_number == 1:
            to_close    =  [PIN_TAP_2]
            to_open     =  [PIN_TAP_1]
            LOG.info("OPENING tap 1({})".format([PIN_TAP_1]))

        if _int_tap_number == 2:
            to_close    =  [PIN_TAP_1]
            to_open     =  [PIN_TAP_2]
            LOG.info("CLOSING tap 1({}), OPENING 2({})".format([PIN_TAP_1], [PIN_TAP_2]))

        if _int_tap_number == 0:
            to_close    = [PIN_TAP_1, PIN_TAP_2]
            to_open     = [0]
            LOG.info("closing taps 1({}) and 2({})".format([PIN_TAP_1], [PIN_TAP_2]))

        for tap_to_close in to_close:
            if not tap_to_close == 0:
                GPIO.output(tap_to_close, True)            # close

        sleep(ms(200))

        for tap_to_open in to_open:
            if not tap_to_open == 0:
                GPIO.output(tap_to_open, False)      # open

        SOLENOID_OPEN = _int_tap_number
    except:
        raise_exception("open_solenoid({})".format(_int_tap_number))


def something_wrong(_str_msg):
    LOG.warning("something wrong: {}".format(_str_msg))
    str_subject = "-- Hydro Pi alert -- {}".format(_str_msg.upper())
    if EMAIL_ALRETS:
        send_email_warning = SendEmail(LOG)
        send_email_warning.send(subject=str_subject, log_file=LOG_FILE_W_PATH, msg=_str_msg)


def raise_exception(_str_func):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    LOG.critical("\n\nfucn '{}' error: \n{}, {} \nline:{}- {}".format(_str_func, exc_type, exc_obj, lineno, line))
    if exc_type == KeyboardInterrupt:
        raise KeyboardInterrupt
    close(99)


def run(debug=False, email=True):
    global DEBUG, EMAIL_ALRETS
    DEBUG = debug
    EMAIL_ALRETS = email
    setup()
    main()


if __name__ == '__main__':
    run()


