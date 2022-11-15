import re
from collections import defaultdict
from typing import Tuple, Union

_INTEGER = re.compile(r'\d+$')
_NUMBERS = re.compile(r'\d*[.,]?\d+$')


class FieldValidator:
    def validate(self, value: str, rules: str, **kwargs) -> Tuple[bool, Union[str, None]]:
        return True, None

    def __call__(self, value: str, required: bool, **kwargs) -> Tuple[bool, str]:
        if required and value is None:
            return False, 'This value is required'
        return self.validate(value, required=required, **kwargs)


class IntegerFieldValidator(FieldValidator):
    def validate(
            self,
            value: str,
            rules: dict,
            **kwargs
    ) -> Tuple[bool, Union[str, None]]:
        """
        Validates whether a given string is a valid integer.

        Additionally, validates min, max bounds of the given integer.
        """
        match = bool(_INTEGER.match(value))
        if not match:
            return False, 'Invalid integer'

        int_value = int(value)
        min_number = rules.get('min')
        max_number = rules.get('max')

        message = None
        is_valid = True

        if min_number and not max_number:
            if int_value < min_number:
                message = f'value must be greater than or equal to {min_number}'
                is_valid = False
        elif max_number and not min_number:
            if int_value > max_number:
                message = f'value must be less than or equal to {max_number}'
                is_valid = False
        elif not (min_number <= int_value <= max_number):
            message = f'value must be between {min_number} and {max_number}'
            is_valid = False
        return is_valid, message


class StringValidator(FieldValidator):
    def validate(
            self,
            value: str,
            rules: dict,
            **kwargs
    ) -> Tuple[bool, Union[str, None]]:

        min_length = rules.get('min_length')
        max_length = rules.get('max_length')

        message = None
        is_valid = True
        string_length = len(value)

        if min_length and not max_length:
            if string_length < min_length:
                message = f"value must not be less than {min_length} characters"
                is_valid = False
        elif max_length and not min_length:
            if string_length > max_length:
                message = f"value must be no longer than {max_length} characters"
                is_valid = False
        elif min_length and max_length:
            if not (min_length <= string_length <= max_length):
                message = f"value must be between {min_length} and {max_length} characters"
                is_valid = False
        return is_valid, message


class NumberFieldValidator(FieldValidator):
    def validate(self, value, rules, **kwargs) -> Tuple[bool, Union[str, None]]:
        match = bool(_NUMBERS.match(value))
        if not match:
            return False, "invalid number"
        return True, None


validators = defaultdict(lambda: StringValidator())
validators.update(**{
    'number': NumberFieldValidator(),
    'integer': IntegerFieldValidator(),
})
