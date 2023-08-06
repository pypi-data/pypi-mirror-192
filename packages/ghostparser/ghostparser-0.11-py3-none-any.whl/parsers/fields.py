from . import translators


def default_function(x):
    return x


class Field:
    translator = default_function

    def __init__(self, translator=None, unique=True):
        if translator:
            self.translator = translator
        self.unique = unique

    def convert(self, val):
        return self.translator(val)


class HourMinuteDeltaField(Field):
    translator = translators.hour_minute_to_delta


class HourMinuteIntField(Field):
    translator = translators.hour_minute_to_int


class PhoneField(Field):
    translator = translators.phone


class StrField(Field):
    translator = str


class IntField(Field):
    translator = int


class FloatField(Field):
    translator = float


class BooleanField(Field):
    translator = bool
