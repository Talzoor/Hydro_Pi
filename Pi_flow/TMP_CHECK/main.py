
#TODO =
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
import sys
import os
from peewee import *
from __init__ import db
from flask_peewee.admin import ModelAdmin

import argparse
import random
import models


SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_NAME = 'water_flow_readings.txt'
FULL_FILE_NAME = '{}/{}'.format(SCRIPT_PATH, FILE_NAME)
FLOW_PIN = 14
CONST_mL_P = 1.385


#db = SqliteDatabase('{}/Readings.db'.format(SCRIPT_PATH)
#                    , check_same_thread=False)


#class PulseData(ModelAdmin):
#    # can_delete = True

#    Date = DateField()
#    Time = TimeField()
#    Pulses = IntegerField()
#    Litters = FloatField()
#    elapsed = TimeField()

#    column_list = ('Date', 'Time', 'Litters')
#    column_default_sort = ('Litters', True)
#    column_sortable_list = (['Litters', True], ['Time', False])
#    column_sortable_list = ('Litters', 'Time')

#    class Meta:
#        database = db




#global pulse_count, time_now, time_start, pulse_flag


def init_db():
    database_name = db.database_name
    print('db::{}'.format(database_name))
#    res = db.connect()
#    print('DB connection:{}'.format(res))
#    db.close()
    pass


def init_vars():
    global pulse_count, time_now, time_start, pulse_flag, time_last_pulse
    pulse_count = 0
    time_now = 0
    time_start = 0
    time_last_pulse = 0
    pulse_flag = False
    file_write('---Started:{}---'.format(datetime.now()))


def init_GPIO():
    global FLOW_PIN
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FLOW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def db_write_record():
    _time_now = datetime.now()
    time_date = _time_now.date()
    time_time = _time_now.time().strftime('%H:%M:%S')

#    db.connect()

    #db.create_tables([models.PulseData])
    models.PulseData.create_table()
    _tmp_Pulses = random.randint(1, 2000)
    new_exam = models.PulseData(Date=time_date,
                                Time=time_time,
                                Pulses=_tmp_Pulses,
                                Litters=round(float(_tmp_Pulses) * CONST_mL_P * 0.001, 3),
                                elapsed='00:99:99')

    #new_exam.save()

    print('example saved!')
    pass


def file_write(str_in):
    global FULL_FILE_NAME
    fb = open(FULL_FILE_NAME, 'a+')
    fb.write('{}\n'.format(str_in))
    fb.close()


def db_pulse_write(_date, _time, _count, _litters, _elapsed):
    db.connect()
    db.create_tables([PulseData])
    pulse = PulseData(Date=_date,
                      Time=_time,
                      Pulses=_count,
                      Litters=_litters,
                      elapsed=_elapsed)
    pulse.save()
    db.close()
    pass


def db_read_all():
    pass
#    for pulse in PulseData.select():
#        print(pulse.Date, pulse.Time, pulse.Pulses, pulse.elapsed)


def flow_count(var):
    global pulse_count, time_start, pulse_flag, time_last_pulse
    time_last_pulse = datetime.now()
    if pulse_count == 0 : time_start = time_last_pulse
    pulse_flag = True
    pulse_count += 1

    #print('{:5d}'.format(pulse_count), end='')
    #if pulse_count%10 == 0:
    #    print('')


def sum_flow_event():
    global pulse_running, time_start, time_last_pulse, pulse_count
    pulse_running = False
    elapsed = time_last_pulse - time_start
    elapsed = str(elapsed).split('.', 2)[0]
    # print('Pulses:{}, Time:{}'.format(pulse_count, elapsed))
    _time_now = datetime.now()
    time_date = _time_now.date()
    time_time = _time_now.time().strftime('%H:%M:%S')

    tmp_pulse_count = int(pulse_count)
    pulse_count = 0

    return time_date, time_time, tmp_pulse_count, elapsed


def print_header():
    print('--- Main started ({}) ---'.format(datetime.now().strftime('%Y-%m-%d  %H:%M:%S')))
    print('GPIO:{}, Python:{}'.format(GPIO.VERSION, sys.version))
    print('file:{}'.format(FULL_FILE_NAME))
    print('mL/P const:{}'.format(CONST_mL_P))


def main():
    global pulse_count, \
        time_now, \
        time_start, \
        pulse_flag, \
        time_last_pulse, \
        pulse_running

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--check",
                        help="write one DB record and exit.",
                        action="store_true")
    args = parser.parse_args()
    if args.check == True:
        db_write_record()
        exit(0)
    db_read_all()
    # i = 0
    pulse_running = False
    try:
        GPIO.add_event_detect(14, GPIO.BOTH, callback=flow_count)
        pulse_count = 0
        no_pulse_count = 0

        while True:
            time_now = datetime.now()
            if pulse_flag == True:
                no_pulse_count = 0
                pulse_flag = False
                pulse_running = True
            else:
                no_pulse_count += 1

            #print('no_p_c:{}'.format(no_pulse_count))
            if no_pulse_count == 2000 and pulse_running==True:
                p_date, p_time, p_count, p_elpd = sum_flow_event()
                litters = round(float(p_count) * CONST_mL_P * 0.001, 3)
                # 
                if p_count > 2:
                    str_to_write = 'Time:{} {}, Pulses:{}, Litters:{}, elapsed:{}'.format(
                        p_date, p_time, p_count, litters, p_elpd)
                    print(str_to_write)
                    file_write('p_cont_type:{}'.format(type(p_count)))
                    file_write(str_to_write)
                    db_pulse_write(p_date, p_time, p_count, litters, p_elpd)

            sleep(1.0/1000.0)   #1mS
            sys.stdout.flush()
            pass

    except KeyboardInterrupt:
        print("Bye.")

    except Exception as err:
        print('Error!:{}'.format(err))

    finally:
        GPIO.cleanup()  # this ensures a clean exit
        db.close()
        print("---Exit ({})---".format(datetime.now().strftime('%Y-%m-%d  %H:%M:%S')))


if __name__ == '__main__':
    print_header()
    init_vars()
    init_GPIO()
    init_db()
    main()
