from peewee import *
import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
database = SqliteDatabase('{}/Readings.db'.format(SCRIPT_PATH), **{})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class PulseData(BaseModel):
    date = DateField(column_name='Date')
    litters = FloatField(column_name='Litters')
    pulses = IntegerField(column_name='Pulses')
    time = TimeField(column_name='Time')
    elapsed = TimeField()

    class Meta:
        table_name = 'pulsedata'

