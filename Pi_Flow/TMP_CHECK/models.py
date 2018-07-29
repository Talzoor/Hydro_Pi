from peewee import *

database = SqliteDatabase('Readings.db', **{})


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

