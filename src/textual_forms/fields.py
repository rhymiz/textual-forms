from typing import Dict, Tuple, Union

from textual.app import ComposeResult
from textual.message import Message, MessageTarget
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import Input

from .validators import validators


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
    value: Reactive[str, None] = Reactive(None)

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
        self.validator = validators[data.get('type', 'string')]
        super().__init__(*args, **kwargs)

    def _make_id(self, data: dict) -> str:
        return f"input_{data['id']}"

    def _make_placeholder(self, data: dict) -> str:
        return data.get('placeholder', f"{data['id']}...")

    def compose(self) -> ComposeResult:
        yield Input(
            id=self._make_id(self.data),
            value=self.data.get('value'),
            placeholder=self._make_placeholder(self.data),
        )

    async def on_input_changed(self, event: Input.Changed) -> None:
        self.value = event.value

    async def watch_value(self, value: str) -> None:
        self.dirty = True if value else False
        widget = self.query_one(f"#{self._make_id(self.data)}", Input)
        required = self.data.get('required', False)
        if self.dirty:
            self.valid = self.validator(value, required)
            widget.styles.border = (
                self.field_success_style
                if self.valid
                else self.field_error_style
            )
        else:
            # A field can be considered valid if it's not required
            self.valid = not required
            # Clear borders when field is no longer considered dirty
            widget.styles.border = None

        await self.emit(self.Changed(self, value=value))
