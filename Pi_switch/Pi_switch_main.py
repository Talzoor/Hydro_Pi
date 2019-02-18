
try:
    from tendo.singleton import *
    Instance = SingleInstance()
except SingleInstanceException:
    print("Error - SingleInstanceException")
    exit(0)
    pass

try:
    sys_platform = sys.platform
    import time as time_lib
    from time import sleep
    import sys
    # from Pi_flow import Pi_flow_main
    import socket
    from datetime import datetime
    from datetime import timedelta
    import linecache

    print("system platform: " + sys_platform)
    if "linux" in sys_platform.lower():
        import RPi.GPIO as GPIO
    else:
        from GPIOEmulator.EmulatorGUI import GPIO

    # from sty import ef, fg, bg, rs
    from sty.register import FgRegister, BgRegister, RsRegister

except ModuleNotFoundError:
    print("Error (Pi_switch_main.py) - ModuleNotFoundError")
    exit(0)
    pass

try:
    from tools.logger import Logger
except ImportError:
    from .tools.logger import Logger
try:
    from Pi_flow import Pi_flow_main
except ImportError:
    from .Pi_flow import Pi_flow_main
try:
    from tools.email_script import SendEmail
except ImportError:
    from .tools.email_script import SendEmail


# print("name_rpi:{}".format(name_rpi))


# noinspection PyPep8
PIN_TAP_1           = 2
PIN_TAP_2           = 3
PIN_MICRO_SWITCH    = 17
# FLOW_PIN            = Pi_flow_main.FLOW_PIN

WATER_LEVEL_SWITCH  = False
CHECK_EVERY         = 1  # ms(100)    # 100mS
DEBUG_PRINT_EVERY   = 1

FLOW_COUNT          = 0
SOLENOID_OPEN       = 99            # init value
FLOW_SENSOR_OK      = True

NEED_TO_CLOSE       = 0     # if 0 ok, if num = no. of failed attempts

# LOG                 = None      # logger instance
LOG_NAME            = "Pi_switch.log"
LOG_FILE_W_PATH     = ""

MICRO_S_CHANGE      = False

# email_alerts        = []
DEBUG_FLOWING_SWITCH = 26
DEBUG                = []


def unix_time():
    return int(round(time_lib.time()))


def time_date():
    return datetime.now().strftime('%Y-%m-%d  %H:%M:%S')


def time():
    return datetime.now().strftime('%H:%M:%S')


def int_hr():
    return int(datetime.now().hour)


def ms(_int_ms):
    return float(_int_ms) / 1000.0


def minutes(_int_min):
    return int(_int_min * 60)


class ColorPrint:
    def __init__(self, _log):
        self.log = _log
        self.fg = FgRegister()
        self.bg = BgRegister()
        self.rs = RsRegister()
        self.bool_bg = False
        self.color_code = 15        # default white

    def __call__(self, _str, **kwargs):
        try:
            if "color_code" in kwargs:
                self.color_code = kwargs["color_code"]
            if "bg" in kwargs:
                self.bool_bg = kwargs["bg"]
            func = self.bg if self.bool_bg else self.fg
        except:
            raise_exception(self.log, "ColorPrint __call__")
        return func(self.color_code) + _str + self.rs.all

    def color(self, _color_code, _bg=False):
        func = self.bg if self.bool_bg else self.fg
        print(func(_color_code))

    def reset(self):
        print(self.rs.all)


class WaterSwitch:

    def __init__(self, _log, _pin):
        self.high = False
        self.low = True

        self.pin = _pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.switch_state = GPIO.input(self.pin)    # get pin state # = False
        self.log = _log
        self.time_open = -1
        self.faulty = 0
        # self.switch_state = GPIO.input(self.pin)

    def state(self, channel=None):
        print_color = ColorPrint(self.log)
        old_state = self.switch_state
        self.switch_state = GPIO.input(self.pin)    # get pin state
        # #### DEBUG OPTION
        if DEBUG[1] == "float_off":
            self.switch_state = False
        #####
        bool_return = (self.switch_state == self.high) and True or False    # choose output

        if old_state is not self.switch_state:
            str_time_open = ''
            if bool_return is True:
                self.time_open = unix_time()
                str_time_open = ''
            elif bool_return is False:
                str_time_open = ", was open for " + \
                                str(timedelta(seconds=(unix_time() - self.time_open)))
                self.time_open = -1

            self.log.info(print_color("Water switch state changed: {}{}".
                                      format(self.switch_state, str_time_open), color_code=98))

        return bool_return


class FlowSensor:
    def __init__(self, _log, _pin):
        self.ok = True
        self.pin = _pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.faulty_count = 0
        self.start_time = 0
        self.log = _log

    def not_ok(self):
        self.faulty_count += 1
        if self.faulty_count > 5:
            self.ok = False
            self.faulty_count = 0

    def flow(self, _int_period):
        flowing = check_flow(self.log, _int_period)
        if flowing:
            if self.start_time == 0:
                self.start_time = unix_time()
        elif not flowing:
            self.start_time = 0

        return flowing

    def time_flowing(self):
        _tmp_time = unix_time()
        return _tmp_time - self.start_time


class Solenoid:
    def __init__(self, _log, _pin, _no):
        self.pin = _pin
        self.start_time = 0
        self.no = _no
        self.log = _log

    def open(self):
        self.start_time = unix_time()
        solenoid_change(self.log, self.no)

    def close(self):
        self.start_time = 0

    def state(self):
        _tmp_state = not GPIO.input(self.pin)
        return _tmp_state

    def time_open(self):
        _tmp_time = unix_time()
        _time_open = _tmp_time - self.start_time
        return self.state() and _time_open or -1

    def restart(self):
        solenoid_change(self.log, self.no)
        sleep(ms(50))
        solenoid_change(self.log, 0)


def init_import_project_modules():
    _tmp_dir = sys.argv[0]
    this_project_dir = _tmp_dir[:_tmp_dir.rfind("/")]
    main_project_dir = this_project_dir[:this_project_dir.rfind("/")]

    sys.path.append(main_project_dir)


def logger_init():
    global LOG_NAME, LOG_FILE_W_PATH
    # running_file = sys.argv[0]
    running_path = sys.path[0]  # str(running_file)[:running_file.rfind("/")]
    log_file_full_path = "{}/{}".format(running_path, LOG_NAME)

    logger_class = Logger(log_file_full_path, "Pi switch")
    log_h = logger_class.logger_handle
    LOG_FILE_W_PATH = logger_class.log_file_name

    return log_h


def setup(email_settings):
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_TAP_1, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(PIN_TAP_2, GPIO.OUT, initial=GPIO.HIGH)

        GPIO.setup(DEBUG_FLOWING_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        init_import_project_modules()
        log = logger_init()
        tap_1 = Solenoid(log, PIN_TAP_1, 1)
        tap_2 = Solenoid(log, PIN_TAP_2, 2)
        flow_sensor = FlowSensor(log, Pi_flow_main.FLOW_PIN)
        water_level = WaterSwitch(log, PIN_MICRO_SWITCH)

        # GPIO.add_event_detect(water_level.pin, GPIO.BOTH, callback=water_level.state, bouncetime=50)
        GPIO.add_event_detect(flow_sensor.pin,  GPIO.BOTH, callback=flow_in_count, bouncetime=5)

        print_header(log)
        water_level.state()
        solenoid_change(log, 0)
        email_h = SendEmail(log, email_settings[1:])

    except:
        raise_exception(log, "setup")

    return log, tap_1, tap_2, flow_sensor, water_level, email_h


def print_header(_log):
    global PIN_MICRO_SWITCH
    log = _log
    print_color = ColorPrint(log)
    str_debug = (DEBUG is True) and " DEBUG MODE" or ""
    log.info(print_color('--- Main started ({}){} ---'.format(time_date(), str_debug), color_code=69))
    log.info('GPIO:{}, Python:{}'.format(GPIO.VERSION, sys.version.replace('\n', ',')))
    name_rpi = socket.gethostname()
    rpi2 = (name_rpi == "RPI2")
    PIN_MICRO_SWITCH = rpi2 and 26 or 17    # debug for rpi2 test
    log.info("running on:" + print_color("{}".format(name_rpi), color_code=46))
    log.info("log file: {}".format(LOG_FILE_W_PATH))
    log.debug("sys.argv[0] is {}".format(repr(sys.argv[0])))
    log.debug("__file__ is {}".format(repr(__file__)))
    log.debug("lock file:{}".format(Instance.lockfile))


def check_flow(log, _int_period):
    global FLOW_COUNT, MICRO_S_CHANGE

    # count as least 10 ticks to consider 'flow state'
    time_start = unix_time()
    time_now = time_start

    while ((time_now - time_start) < _int_period) and \
            (not MICRO_S_CHANGE):  # wait to see if flowing
        sleep(ms(5))  # 0.5mS
        # if DEBUG: flow_in_count_prog()
        time_now = unix_time()
        # if MICRO_S_CHANGE:
        #    MICRO_S_CHANGE = False
        #    break

    flowing = False
    if FLOW_COUNT > 10:
        log.info("Flow count during {} sec: {}".format(time_now - time_start, FLOW_COUNT))
        flowing = True

    FLOW_COUNT = 0

    return flowing


def flow_in_count(channel=None):
    global FLOW_COUNT
    if not DEBUG:
        FLOW_COUNT += 1
    else:
        FLOW_COUNT += 11


def flow_in_count_prog():
    global FLOW_COUNT
    # time_now = unix_time()

    if FLOW_COUNT > 500: FLOW_COUNT = 0
    # if time_now - TIME_S > 10: FLOW_COUNT = 0
    state = not GPIO.input(DEBUG_FLOWING_SWITCH)
    if state:
        FLOW_COUNT += 1
    else:
        FLOW_COUNT = 0


def close(log, _code=None):
    print_color = ColorPrint(log)
    log.debug("Cleaning GPIOs")
    GPIO.cleanup()
    log.info(print_color("Bye.", color_code=69))
    exit(_code is None and 0 or _code)


def solenoid_change(log, _int_tap_number):
    # global SOLENOID_OPEN
    print_color = ColorPrint(log)
    to_close = []
    to_open = []
    try:
        if _int_tap_number == 1:
            to_close    = [PIN_TAP_2, ]
            to_open     = [PIN_TAP_1, ]
            log.info(print_color("OPENING tap 1", color_code=34) +
                     "(pin {})".format([PIN_TAP_1]))

        if _int_tap_number == 2:
            to_close    = [PIN_TAP_1, ]
            to_open     = [PIN_TAP_2, ]
            log.info(print_color("CLOSING tap 1", color_code=160) +
                     " (pin {}), ".format([PIN_TAP_1]) +
                     print_color("OPENING 2", color_code=34) +
                     " (pin {})".format([PIN_TAP_2]))

        if _int_tap_number == 0:
            to_close    = [PIN_TAP_1, PIN_TAP_2]
            to_open     = [0, ]
            log.info(print_color("CLOSING taps 1 and 2", color_code=160) +
                     " (pins {},{})".format([PIN_TAP_1], [PIN_TAP_2]))

        for tap_to_close in to_close:
            if not tap_to_close == 0:
                GPIO.output(tap_to_close, True)            # close

        sleep(ms(200))

        for tap_to_open in to_open:
            if not tap_to_open == 0:
                GPIO.output(tap_to_open, False)      # open

        # SOLENOID_OPEN = _int_tap_number

    except:
        raise_exception(log, "open_solenoid({})".format(_int_tap_number))


def something_wrong(log, email_alerts, email_handle, _str_msg):
    # global EMAIL_ALERTS
    str_msg = _str_msg.upper()
    str_msg_w_time = datetime.now().strftime('%H:%M:%S') + ' ' + _str_msg

    log.warning("something wrong: {}".format(str_msg))
    # print("EMAIL_ALERTS:{}".format(EMAIL_ALERTS))
    print("email_alerts[0]:{}, [1]:{}, [2]:{}".format(
        email_alerts[0],
        email_alerts[1],
        email_alerts[2]
    ))
    if email_alerts[0] is True:
        str_subject = "-- Hydro Pi alert -- {}".format(str_msg)
        email_handle.send(subject=str_subject, msg=str_msg_w_time, log_file=LOG_FILE_W_PATH)


def raise_exception(log, _str_func):
    print_color = ColorPrint(log)
    exc_type, exc_obj, tb = sys.exc_info()
    frm = tb.tb_frame
    lineno = tb.tb_lineno
    filename = frm.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, frm.f_globals)

    print_color.color(196)
    log.critical("\n\nfucn '{}' error: \n{}, {} \nline:{}- {}"
                 .format(_str_func, exc_type, exc_obj, lineno, line))
    print_color.reset()

    if exc_type == KeyboardInterrupt:
        raise KeyboardInterrupt
    close(log, 99)


def check_args(**kwargs):
    global DEBUG    # , EMAIL_ALERTS
    debug = [False, "float_on"]
    email = [True, 1, 8]    # [send, how many a day, first one on(24h)]
    taps = 2
    if "debug" in kwargs:
        debug = kwargs["debug"]
    if "email" in kwargs:
        email = kwargs["email"]
    if "taps" in kwargs:
        taps = kwargs["taps"]

    DEBUG = debug
    # EMAIL_ALERTS = email
    print("DEBUG:{}".format(DEBUG))
    print("EMAIL_ALERTS:{}".format(email))
    print("Taps:{}".format(taps))

    sys.stdout.flush()
    return email, taps


def decide(log, taps_no, tap_1, tap_2, flow_sensor, water_level, email_alerts, email_handle):

    try:
        state_2 = GPIO.input(DEBUG_FLOWING_SWITCH)
        if state_2:
            something_wrong(log, email_alerts, email_handle, "test")

        flowing = check_flow(log, 2)
        solenoid_open = tap_1.state() or tap_2.state()
        # print("tap_1.state():{}, tap_2.state():{}".format(tap_1.state(), tap_2.state()))
        if water_level.state() is True:       # need to fill water
            if water_level.faulty > 0:
                if abs(int_hr()-water_level.faulty) == 12:
                    water_level.faulty = 0
                else:
                    pass
            elif water_level.faulty <= 0:
                if solenoid_open:                           # if tap already open
                    if flowing:
                        pass                                # nothing
                    elif not flowing:                                   # not flowing
                        if flow_sensor.ok:
                            if tap_1.state() or tap_2.state():
                                pass
                                # log.debug("time open- tap1:{}, tap2:{}"
                                #          .format(tap_1.time_open(), tap_2.time_open()))
                            if tap_1.state():               # tap 1 open?
                                if tap_1.time_open() >= 2:  # more than 20 sec?
                                    if taps_no == 1:
                                        flow_sensor.not_ok()    # count faulty
                                    else:
                                        tap_2.open()  # switch to tap 2
                                elif tap_1.time_open() < 2:                       # tap 1 - less than 20 sec
                                    pass                    # nothing
                            elif tap_2.state():
                                if tap_2.time_open() >= 20:    # more than 2 sec
                                    tap_1.open()
                                    flow_sensor.not_ok()    # count faulty
                                elif tap_2.time_open() < 20:
                                    pass                    # nothing
                        elif not flow_sensor.ok:
                            if taps_no == 2:
                                if not tap_2.state(): tap_2.open()
                                if tap_2.time_open() >= minutes(10):    # more than 10 min?
                                    tap_1.open()
                                    if tap_1.time_open() >= minutes(3):   # more than 3 min?
                                        solenoid_change(log, 0)      # close all taps
                                        something_wrong(log, email_alerts, email_handle,
                                                        "NO WATER OR FLOAT BAD")     # no water
                                    elif tap_1.time_open() < minutes(3):                       # less than 3 min
                                        pass                    # nothing
                                elif tap_2.time_open() > minutes(10):                           # less than 10 min
                                    pass                       # nothing
                            elif taps_no == 1:
                                if tap_1.time_open() >= minutes(3):  # more than 3 min?
                                    solenoid_change(log, 0)  # close all taps
                                    if water_level.faulty <= -5:     # float is not going up
                                        water_level.faulty = int_hr()       # save the 24hr time
                                        log.warning("Closing system for 12 hours.")
                                    elif water_level.faulty > -5:    # float still considered ok
                                        water_level.faulty -= 1
                                        something_wrong(log, email_alerts, email_handle,
                                                        "NO WATER OR FLOAT BAD")  # no water
                                elif tap_1.time_open() < minutes(3):  # less than 3 min
                                    pass  # nothing
                elif not solenoid_open:                                       # Solenoid close
                    tap_1.open()                            # open tap 1
        elif water_level.state() is False:                          # water level ok
            if solenoid_open:
                # solenoid_change(log, 0)                          # close all taps
            water_level.faulty = 0
            if (not flow_sensor.ok) and \
                    (tap_1.time_open() > minutes(2) or tap_2.time_open() > minutes(2)):
                something_wrong(log, email_alerts, email_handle, "FLOW SENSOR BAD")
            if flowing:
                if flow_sensor.time_flowing() >= 30:      # flowing more than 30 sec?
                    tap_1.restart()                     # restart taps
                    tap_2.restart()
                    something_wrong(log, email_alerts, email_handle, "DRIPPING")
                elif flow_sensor.time_flowing() < 30:                                   # if flowing less than 30 sec?
                    if flow_sensor.time_flowing() > 10:  # flowing more than 10 sec?
                        tap_1.restart()                 # restart taps
                        tap_2.restart()
            else:       # no flow
                pass
    except:
        raise_exception(log, "decide")


def main(log, taps_no, tap_1, tap_2, flow_sensor, water_level, email_alerts, email_handle):
    global NEED_TO_CLOSE, MICRO_S_CHANGE, WATER_LEVEL_SWITCH

    try:
        log.debug("Flow_pin:{}".format(flow_sensor.pin))
        # time_start = unix_time()

        while True:
            # time_now = unix_time()
            sys.stdout.flush()
            decide(log, taps_no, tap_1, tap_2, flow_sensor, water_level, email_alerts, email_handle)
            sleep(CHECK_EVERY)

    except KeyboardInterrupt:
        log.info("Keyboard Exc.")
        raise KeyboardInterrupt
    except:
        raise_exception(log, "main")

    finally:
        close(log)


def run(**kwargs):
    email_alerts, taps = check_args(**kwargs)
    log, tap_1, tap_2, flow_sensor, water_level, email_handle = setup(email_alerts)
    main(log, taps, tap_1, tap_2, flow_sensor, water_level, email_alerts, email_handle)


if __name__ == '__main__':
    run()


