from rich.table import Table
from textual.app import App, ComposeResult
from textual.widgets import Static

from textual_forms.forms import Form

FIELDS = [
    {
        'id': 'name',
        'required': True,
        'placeholder': 'name...',
        'rules': {
            'min_length': 3,
        }
    },
    {
        'id': 'age',
        'type': 'integer',
        'required': True,
        'placeholder': 'age...',
        'rules': {
            'min': 18,
            'max': 65
        }
    },
    {
        'id': 'email',
        'required': False,
        'placeholder': 'hi@example.com',
    },
]

BUTTONS = [
    {
        'id': 'submit',
        'label': 'Submit',
        'variant': 'success',
        'watch_form_valid': True
    },
]


class BasicTextualForm(App):
    def compose(self) -> ComposeResult:
        yield Static(id='submitted-data')
        yield Form(
            fields=FIELDS,
            buttons=BUTTONS,
        )

    def on_form_event(self, message: Form.Event) -> None:
        if message.event == 'submit':
            table = Table(*message.data.keys())
            table.add_row(*message.data.values())
            self.query_one('#submitted-data').update(table)


if __name__ == '__main__':

    BasicTextualForm().run()
