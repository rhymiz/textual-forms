from __future__ import annotations

from typing import Any, Iterable, Type

from textual.app import ComposeResult
from textual.message import Message, MessageTarget
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input, Static

from .validators import (
    FieldValidator,
    IntegerFieldValidator,
    NumberFieldValidator,
    StringValidator,
)


class FieldError(Static):
    """A form field error label"""

    DEFAULT_CSS = """
    FieldError {
        color: red;
    }
    """


class Field(Widget):
    """
    A form field
    """

    DEFAULT_CSS = """
    Field {
        height: 5;
        margin: 0;
    }
    Field>Input {
        height: 1;
        margin: 0;
    }
    """
    value: str = reactive("")
    dirty: bool = reactive(False)
    valid: bool = reactive(False)

    validator = Type[FieldValidator]

    field_error_style: Iterable[str] = ("solid", "red")
    field_success_style: Iterable[str] = ("solid", "green")

    def __init__(self, data: dict[str, Any], **kwargs: dict[str, Any]) -> None:
        self.data = data
        self.rules = data.pop("rules", {})
        super().__init__(**kwargs)

    class ValueChanged(Message):
        """
        message that's emitted when
        the value of an input changes
        """

        def __init__(self, sender: MessageTarget, value: str | None) -> None:
            self.value = value
            super().__init__(sender)

    @property
    def _field_name(self) -> str:
        return self.data["name"]

    @property
    def _field_id(self) -> str:
        return f"tf_{self._field_name}"

    @property
    def _field_error_id(self) -> str:
        return f"{self._field_id}_error"

    @property
    def placeholder(self) -> str:
        return self.data.get("placeholder") or self._field_name

    def compose(self) -> ComposeResult:
        input_kwargs = {
            "id": self._field_id,
            "name": self._field_name,
            "placeholder": self.placeholder,
        }
        if self.data["value"]:
            input_kwargs["value"] = self.data["value"]
        yield Input(**input_kwargs)
        yield FieldError("", id=self._field_error_id)

    async def on_input_changed(self, event: Input.Changed) -> None:
        self.value = event.value

    async def watch_value(self, value: str) -> None:
        self.dirty = bool(value)
        input_widget = self.query_one(f"#{self._field_id}", Input)
        error_widget = self.query_one(f"#{self._field_error_id}", FieldError)
        required = self.data.get("required", False)

        if self.validator is None:
            self.post_message_no_wait(self.ValueChanged(sender=self, value=value))
            return

        if self.dirty:
            self.valid, message = self.validator(value, required, rules=self.rules)
            input_widget.styles.border = (
                self.field_success_style if self.valid else self.field_error_style
            )
            error_text: str = "" if self.valid else message  # type: ignore
            error_widget.update(error_text)
        else:
            # A field is considered valid if it's not flagged as required
            self.valid = not required
            # Clear borders when field is no longer considered dirty
            input_widget.styles.border = None
            error_widget.update("")

        self.post_message_no_wait(self.ValueChanged(sender=self, value=value))


class StringField(Field):
    validator = StringValidator()

    def __init__(
        self,
        name: str,
        *,
        value: str | None = None,
        required: bool = False,
        placeholder: str | None = None,
        min_length: int = 0,
        max_length: int | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        # TODO: make custom formfield creation more
        #   generic. This is kind of alot...
        data: dict[str, Any] = {
            "name": name,
            "value": value,
            "required": required,
            "placeholder": placeholder,
            "rules": {
                "min_length": min_length,
                "max_length": max_length,
            },
        }
        super().__init__(data, **kwargs)


class NumberField(Field):
    validator = NumberFieldValidator()

    def __init__(
        self,
        name: str,
        *,
        value: int | None = None,
        required: bool = False,
        placeholder: str | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        data: dict[str, Any] = {
            "name": name,
            "value": value,
            "required": required,
            "placeholder": placeholder,
            "rules": {},
        }
        super().__init__(data, **kwargs)


class IntegerField(Field):
    validator = IntegerFieldValidator()

    def __init__(
        self,
        name: str,
        *,
        value: int | None = None,
        required: bool = False,
        placeholder: str | None = None,
        min_value: int | None = None,
        max_value: int | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        data: dict[str, Any] = {
            "name": name,
            "value": value,
            "required": required,
            "placeholder": placeholder,
            "rules": {
                "min": min_value,
                "max": max_value,
            },
        }
        super().__init__(data, **kwargs)
