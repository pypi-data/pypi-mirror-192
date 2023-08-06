class UniqueParseError(Exception):
    def __init__(self, field, val) -> None:
        super().__init__(f'{field} must be unique. {val} already exists.')


class MissingFieldsParseError(Exception):
    def __init__(self, cls, missing_fields):
        super().__init__(f'{cls} missing {missing_fields}.')


class ExtraFieldsParseError(Exception):
    def __init__(self, cls, extra_fields):
        super().__init__(f'{cls} does not contain {extra_fields}.')


class CreateWithIdParseError(Exception):
    def __init__(self, cls):
        super().__init__(f'{cls} cannot use id on creation.')
