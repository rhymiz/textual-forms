from __future__ import annotations

import re
from collections import defaultdict
from typing import Any, Pattern, Union

_INTEGER: Pattern[str] = re.compile(r"\d+$")
_NUMBERS: Pattern[str] = re.compile(r"\d*[.,]?\d+$")


class FieldValidator:
    """
    base field validator class
    """

    def validate(self, value: str, rules: dict[str, Any]) -> tuple[bool, str | None]:
        raise NotImplementedError

    def __call__(
        self,
        value: str,
        required: bool,
        rules: dict[str, Any],
    ) -> tuple[bool, str | None]:
        if required and value is None:
            return False, "This value is required"
        return self.validate(value, rules=rules)


class IntegerFieldValidator(FieldValidator):
    """a validator that ensures a given value is an integer.
    additional, it can also ensure that the number is within certain bounds.
    """

    def validate(
        self,
        value: str,
        rules: dict[str, Any],
    ) -> tuple[bool, str | None]:
        """
        Validates whether a given string is a valid integer.

        Additionally, validates min, max bounds of the given integer.
        """
        match: bool = bool(_INTEGER.match(value))
        if not match:
            return False, "Invalid integer"

        int_value = int(value)
        min_number: int | None = rules.get("min")
        max_number: int | None = rules.get("max")

        message: str | None = None
        is_valid: bool = True

        if min_number and max_number:
            is_valid = min_number <= int_value <= max_number
            message = (
                f"value must be between {min_number} and {max_number}"
                if not is_valid
                else None
            )
            return is_valid, message

        if min_number:
            if int_value < min_number:
                message = f"value must be greater than or equal to {min_number}"
                is_valid = False
        elif max_number:
            if int_value > max_number:
                message = f"value must be less than or equal to {max_number}"
                is_valid = False
        return is_valid, message


class StringValidator(FieldValidator):
    """a validator that "ensures" a given value is an string.
    additional, it can also ensure that the value is within certain bounds.
    """

    def validate(
        self,
        value: str,
        rules: dict[str, Any],
    ) -> tuple[bool, str | None]:
        """validate a given string"""
        min_length = rules.get("min_length")
        max_length = rules.get("max_length")

        message: str | None = None
        is_valid: bool = True
        string_length = len(value)

        if min_length and max_length:
            is_valid = min_length <= string_length <= max_length
            message = (
                f"value must be between {min_length} and {max_length} characters"
                if is_valid
                else None
            )
            return is_valid, message

        if min_length:
            if string_length < min_length:
                message = f"value must not be less than {min_length} characters"
                is_valid = False
        elif max_length:
            if string_length > max_length:
                message = f"value must be no longer than {max_length} characters"
                is_valid = False
        return is_valid, message


class NumberFieldValidator(FieldValidator):
    """a validator that ensures a given value is numeric."""

    def validate(
        self,
        value: str,
        rules: dict[str, Any],
    ) -> tuple[bool, Union[str, None]]:
        match = bool(_NUMBERS.match(value))
        if not match:
            return False, "invalid number"
        return True, None


validators: dict[str, FieldValidator] = defaultdict(lambda: StringValidator())
validators.update(
    **{
        "number": NumberFieldValidator(),
        "integer": IntegerFieldValidator(),
    }
)
