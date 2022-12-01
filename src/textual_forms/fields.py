from typing import Any, Dict, Iterable, Union

from textual.app import ComposeResult
from textual.message import Message, MessageTarget
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input, Static

from .validators import validators


class FieldError(Static):
    """A form field error label"""
    DEFAULT_CSS = """
    FieldError {
        color: red;
    }
    """


class FormField(Widget):
    """
    A form field
    """
    DEFAULT_CSS = """
    FormField {
        height: 5;
        margin: 0;
    }
    FormField>Input {
        height: 1;
        margin: 0;
    }
    """
    value: str = reactive.var('')
    dirty: bool = reactive.var(False)
    valid: bool = reactive.var(False)

    field_error_style: Iterable[str] = ('solid', 'red')
    field_success_style: Iterable[str] = ('solid', 'green')

    class Changed(Message):
        """
        message that's emitted when
        the value of an input changes
        """

        def __init__(self, sender: MessageTarget, value: Union[str, None]) -> None:
            self.value = value
            super().__init__(sender)

    def __init__(self, data: Dict[str, Any], **kwargs: Dict[str, Any]) -> None:
        self.data = data
        self.rules = data.pop('rules', {})
        self.validator = validators[data.get('type', 'string')]
        super().__init__(**kwargs)

    @property
    def field_id(self) -> str:
        return f"tf_{self.data['id']}"

    @property
    def field_error_id(self) -> str:
        return f"{self.field_id}_error"

    @property
    def placeholder(self) -> str:
        default = f"{self.data['id']}"
        return self.data.get('placeholder', default)

    def compose(self) -> ComposeResult:
        yield Input(
            id=self.field_id,
            value=self.data.get('value'),
            placeholder=self.placeholder,
        )
        yield FieldError('', id=self.field_error_id)

    async def on_input_changed(self, event: Input.Changed) -> None:
        self.value = event.value

    async def watch_value(self, value: str) -> None:
        self.dirty = bool(value)
        input_widget = self.query_one(f"#{self.field_id}", Input)
        error_widget = self.query_one(f"#{self.field_error_id}", FieldError)
        required = self.data.get('required', False)
        if self.dirty:
            self.valid, message = self.validator(value, required, rules=self.rules)
            input_widget.styles.border = (
                self.field_success_style
                if self.valid
                else self.field_error_style
            )
            error_text: str = '' if self.valid else message
            error_widget.update(error_text)
        else:
            # A field is considered valid if it's not flagged as required
            self.valid = not required
            # Clear borders when field is no longer considered dirty
            input_widget.styles.border = None
            error_widget.update('')

        await self.emit(self.Changed(self, value=value))
