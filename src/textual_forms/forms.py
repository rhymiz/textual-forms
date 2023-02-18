from __future__ import annotations

from typing import Any, Type

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.message import Message, MessageTarget
from textual.reactive import reactive
from textual.widget import Widget

from .buttons import Button
from .fields import Field, IntegerField, NumberField, StringField


class Form(Widget):
    """
    A container widget for inputs and buttons that
    behaves kind of like a web-based form with validations.
    """

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

    data: dict[str, Any] = reactive({})
    valid: bool = reactive(False)
    button_widget: Type[Button] = Button
    form_field_widget: Type[Field] = Field
    button_group_container: Type[Widget] = Horizontal

    class Event(Message):
        """
        message that's emitted whenever a button is pressed
        """

        def __init__(
            self,
            sender: MessageTarget,
            event: str,
            data: dict[str, Any],
        ) -> None:
            self.data = data
            self.event = event
            super().__init__(sender)

    def __init__(
        self,
        *,
        fields: list[Field | IntegerField | NumberField | StringField],
        buttons: list[Button],
        **kwargs: dict[str, Any],
    ) -> None:
        self.fields = fields
        self.buttons = buttons
        self._watching_form_valid: list[Button] = []
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        for field in self.fields:
            yield field

        buttons: list[Button] = []
        for data in self.buttons:
            enabled_on_form_valid = getattr(data, "enabled_on_form_valid", False)
            if enabled_on_form_valid:
                self._watching_form_valid.append(data)
            buttons.append(data)

        yield self.button_group_container(*buttons, id="button_group")

    async def watch_valid(self, valid: bool) -> None:
        """
        enable/disable buttons based on the state of the form
        """
        for button in self._watching_form_valid:
            button.disabled = not valid

    async def on_field_value_changed(self, message: Field.ValueChanged) -> None:
        """
        listens for form field changes and assesses the validity of the form
        """
        self.data[getattr(message.sender, "_field_name")] = message.value
        self.valid = all([x.valid for x in self.query(Field)])

    async def on_button_pressed(self, message: Button.Pressed) -> None:
        """
        emit an event whenever any button inside the form is pressed
        """
        await self.post_message(
            self.Event(
                self,
                data=self.data,
                event=getattr(message.button, "id"),
            )
        )
