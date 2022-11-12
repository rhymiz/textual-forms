import re
from collections import defaultdict

_UUID = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}')
_INTEGER = re.compile(r'\d+$')
_NUMBERS = re.compile(r'\d*[.,]?\d+$')


class FieldValidator:
    def validate(self, value, **kwargs) -> bool:
        return True

    def __call__(self, value, required, **kwargs) -> bool:
        if required and value is None:
            return False
        return self.validate(value, required=required, **kwargs)


class IntegerFieldValidator(FieldValidator):
    def validate(self, value, **kwargs) -> bool:
        # TODO: add min, max validation
        return bool(_INTEGER.match(value))


class StringValidator(FieldValidator):
    def validate(self, value, **kwargs) -> bool:
        # TODO: add min_length, max_length validation
        return isinstance(value, str)


class NumberFieldValidator(FieldValidator):
    def validate(self, value, **kwargs) -> bool:
        # TODO: add min_length, max_length validation
        return bool(_NUMBERS.match(value))


class UUIDFieldValidator(FieldValidator):
    def validate(self, value, **kwargs) -> bool:
        return bool(_UUID.match(value))


validators = defaultdict(lambda: StringValidator())
validators.update(**{
    'uuid': UUIDFieldValidator(),
    'number': NumberFieldValidator(),
    'integer': IntegerFieldValidator(),
})
