from __future__ import annotations

from typing import Dict, List

from textual import reactive
from textual.app import ComposeResult
from textual.containers import Container
from textual.message import Message, MessageTarget
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import Button

from .fields import FormField


async def _noop(*args, **kwargs) -> None:
    pass


class TextualForm(Widget):
    DEFAULT_CSS = """
    TextualForm {
        padding: 1
    }
    TextualForm>Container {
        padding: 0;
        margin: 0;
        height: 50%;
    }
    TextualForm>Container>Button {
        margin-left: 1
    }
    """

    data: Reactive[Dict] = Reactive({})
    on_submit = _noop
    allow_submit: Reactive[bool] = Reactive(False)

    class Submit(Message):
        def __init__(
                self,
                sender: MessageTarget,
                data: Dict,
        ) -> None:
            self.data = data
            super().__init__(sender)

    def __init__(self, form_data: List[Dict], *args, **kwargs):
        self.initial_data = form_data
        self._setup_fields(form_data)
        super().__init__(*args, **kwargs)

    def _setup_fields(self, fields: List[Dict]):
        for field in fields:
            setattr(self, f"_{field['id']}", reactive.var(None))

    def compose(self) -> ComposeResult:
        fields = [
            FormField(data=field, id=field['id'])
            for field in self.initial_data
        ]
        yield Container(
            *fields,
            Button('Submit', id='form_submit', disabled=True)
        )

    async def watch_allow_submit(self, allow_submit: bool) -> None:
        self.query_one('#form_submit', Button).disabled = not allow_submit

    async def on_form_field_changed(self, message: FormField.Changed) -> None:
        self.data[message.sender.id] = message.value
        form_fields = self.query(FormField)
        self.allow_submit = all([x.valid for x in form_fields])

    async def on_button_pressed(self, message: Button.Pressed) -> None:
        if message.button.id == 'form_submit':
            await self.on_submit(self.data)
            await self.emit(self.Submit(self, self.data))
