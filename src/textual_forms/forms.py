from __future__ import annotations

from typing import Dict, List, Type

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.message import Message, MessageTarget
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import Button, Static

from .fields import FormField


class Form(Widget):
    DEFAULT_CSS = """  
    Form {
        padding: 1
    }
    Form>Container {
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

    data: Reactive[dict] = Reactive({})
    valid: Reactive[bool] = Reactive(False)
    button_widget: Type[Static] = Button
    form_field_widget: Type[Widget] = FormField
    button_group_container: Type[Widget] = Horizontal

    class Event(Message):
        """
        message that's emitted whenever a button is pressed
        """

        def __init__(self, sender: MessageTarget, event: str, data: dict) -> None:
            self.data = data
            self.event = event
            super().__init__(sender)

    def __init__(self, *, fields: List[Dict], buttons: List[Dict], **kwargs):
        self.fields = fields
        self.buttons = buttons
        self._watching_valid = []
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        for field in self.fields:
            yield self.form_field_widget(
                id=field['id'],
                data=field,
            )

        buttons = []
        for button in self.buttons:
            btn = self.button_widget(
                id=button['id'],
                label=button['label'],
                variant=button.get('variant', 'primary'),
                classes=button.get('classes'),
                disabled=button.get('disabled', True)
            )
            if button.get('watch_form_valid', False):
                self._watching_valid.append(btn)
            buttons.append(btn)

        yield self.button_group_container(*buttons, id='button_group')

    async def watch_valid(self, allow_submit: bool) -> None:
        for button in self._watching_valid:
            button.disabled = not allow_submit

    async def on_form_field_changed(self, message: FormField.Changed) -> None:
        self.data[message.sender.id] = message.value
        self.valid = all([x.valid for x in self.query(FormField)])

    async def on_button_pressed(self, message: Button.Pressed) -> None:
        await self.emit(self.Event(
            self,
            data=self.data,
            event=message.button.id,
        ))
