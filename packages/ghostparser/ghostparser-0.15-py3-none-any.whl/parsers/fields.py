from . import translators
import datetime as dt


def default_function(cls, x):
    return x


class Field:
    translator = default_function
    type = str

    def __init__(self, translator=None, unique=False, default=None, null=False):
        if translator:
            self.translator = translator
        self.unique = unique
        self.default = default
        self.null = null

    def convert(self, val):
        return self.translator(val)


class HourMinuteDeltaField(Field):
    type = dt.timedelta
    translator = translators.hour_minute_to_delta


class HourMinuteIntField(Field):
    type = int
    translator = translators.hour_minute_to_int


class PhoneField(Field):
    translator = translators.phone


class StrField(Field):
    translator = str


class IntField(Field):
    type = int
    translator = int


class FloatField(Field):
    type = float
    translator = float


class BooleanField(Field):
    translator = bool
