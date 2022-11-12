from rich.table import Table
from textual.app import App, ComposeResult
from textual.widgets import Static

from textual_forms.forms import TextualForm

FORM_DATA = [
    {
        'id': 'name',
        'required': True,
        'placeholder': 'name...'
    },
    {
        'id': 'age',
        'type': 'integer',
        'required': True,
        'placeholder': 'age...'
    },
    {
        'id': 'email',
        'value': 'john@example.com',
        'required': False,
        'placeholder': 'hi@example.com'
    },
]


class BasicTextualForm(App):
    def compose(self) -> ComposeResult:
        yield Static(id='submitted-data')
        yield TextualForm(form_data=FORM_DATA)

    async def on_textual_form_submit(self, message: TextualForm.Submit) -> None:
        table = Table(*message.data.keys())
        table.add_row(*message.data.values())
        self.query_one('#submitted-data').update(table)


if __name__ == '__main__':

    BasicTextualForm().run()
