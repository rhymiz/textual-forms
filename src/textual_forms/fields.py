from typing import Dict, Tuple, Union

from textual.app import ComposeResult
from textual.message import Message, MessageTarget
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import Input, Static

from .validators import validators


class FieldError(Static):
    DEFAULT_CSS = """
    FieldError {
        color: red;
    }
    """


class FormField(Widget):
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
    dirty: Reactive[bool] = Reactive(False)
    valid: Reactive[bool] = Reactive(False)
    value: Reactive[Union[str, None]] = Reactive(None)

    field_error_style: Tuple[str] = ('solid', 'red'),
    field_success_style: Tuple[str] = ('solid', 'green')

    class Changed(Message):
        def __init__(
                self,
                sender: MessageTarget,
                value: Union[str, None],
        ) -> None:
            self.value = value
            super().__init__(sender)

    def __init__(
            self,
            data: Dict,
            *args,
            **kwargs
    ) -> None:
        self.data = data
        self._rules = data.pop('rules', {})
        self.validator = validators[data.get('type', 'string')]
        super().__init__(*args, **kwargs)

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
        self.dirty = True if value else False
        input_widget = self.query_one(f"#{self.field_id}", Input)
        error_widget = self.query_one(f"#{self.field_error_id}", FieldError)
        required = self.data.get('required', False)
        if self.dirty:
            self.valid, message = self.validator(value, required, rules=self._rules)
            input_widget.styles.border = (
                self.field_success_style
                if self.valid
                else self.field_error_style
            )
            error_text = '' if self.valid else message
            error_widget.update(error_text)
        else:
            # A field is considered valid if it's not flagged as required
            self.valid = not required
            # Clear borders when field is no longer considered dirty
            input_widget.styles.border = None
            error_widget.update('')

        await self.emit(self.Changed(self, value=value))
