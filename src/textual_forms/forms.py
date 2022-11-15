from __future__ import annotations

from typing import Dict, List

from textual.app import ComposeResult
from textual.containers import Horizontal
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
    }
    #button_group {
        margin-left: 1;
    }
    #button_group > Button {
        margin-right: 5;
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

    class Canceled(Message):
        pass

    def __init__(self, form_data: List[Dict], *args, **kwargs):
        self.initial_data = form_data
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        fields = [
            FormField(data=field, id=field['id'])
            for field in self.initial_data
        ]
        for field in fields:
            yield field

        yield Horizontal(
            Button('Submit', id='submit_button', disabled=True),
            Button('Cancel', id='cancel_button', variant='error'),
            id='button_group',
        )

    async def watch_allow_submit(self, allow_submit: bool) -> None:
        self.query_one('#submit_button', Button).disabled = not allow_submit

    async def on_form_field_changed(self, message: FormField.Changed) -> None:
        self.data[message.sender.id] = message.value
        form_fields = self.query(FormField)
        self.allow_submit = all([x.valid for x in form_fields])

    async def clear_inputs(self):
        for field in self.query(FormField):
            field.children[0].value = ''

    async def on_button_pressed(self, message: Button.Pressed) -> None:
        if message.button.id == 'submit_button':
            await self.on_submit(self.data)
            await self.emit(self.Submit(self, self.data))
            await self.clear_inputs()
        if message.button.id == 'cancel_button':
            await self.emit(self.Canceled(self))
            await self.clear_inputs()
