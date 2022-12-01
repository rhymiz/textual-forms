from typing import Any, Dict, List, Type

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.message import Message, MessageTarget
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import Button

from .fields import FormField


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

    data: Reactive[Dict[str, Any]] = Reactive({})
    valid: Reactive[bool] = Reactive(False)
    button_widget: Type[Button] = Button
    form_field_widget: Type[FormField] = FormField
    button_group_container: Type[Widget] = Horizontal

    class Event(Message):
        """
        message that's emitted whenever a button is pressed
        """

        def __init__(
            self,
            sender: MessageTarget,
            event: str,
            data: Dict[str, Any]
        ) -> None:
            self.data = data
            self.event = event
            super().__init__(sender)

    def __init__(
        self,
        *,
        fields: List[Dict[str, Any]],
        buttons: List[Dict[str, Any]],
        **kwargs: Dict[str, Any]
    ) -> None:
        self.fields = fields
        self.buttons = buttons
        self._watching_form_valid: List[Button] = []
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        for field in self.fields:
            yield self.form_field_widget(
                id=field['id'],
                data=field,
            )

        buttons: List[Button] = []
        for button in self.buttons:
            btn = self.button_widget(
                id=button['id'],
                label=button['label'],
                variant=button.get('variant', 'primary'),
                classes=button.get('classes'),
                disabled=button.get('disabled', True)
            )
            if button.get('watch_form_valid', False):
                self._watching_form_valid.append(btn)
            buttons.append(btn)

        yield self.button_group_container(*buttons, id='button_group')

    async def watch_valid(self, valid: bool) -> None:
        """
        enable/disable buttons based on the state of the form
        """
        for button in self._watching_form_valid:
            button.disabled = not valid

    async def on_form_field_changed(self, message: FormField.Changed) -> None:
        """
        listens for form field changes and assesses the validity of the form
        """
        self.data[getattr(message.sender, 'id')] = message.value
        self.valid = all([x.valid for x in self.query(FormField)])

    async def on_button_pressed(self, message: Button.Pressed) -> None:
        """
        emit an event whenever any button inside the form is pressed
        """
        await self.emit(self.Event(
            self,
            data=self.data,
            event=getattr(message.button, 'id'),
        ))
