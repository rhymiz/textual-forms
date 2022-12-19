from rich.table import Table
from textual.app import App, ComposeResult
from textual.widgets import Static

from src.textual_forms.forms import Form
from textual_forms.fields import IntegerField, StringField
from textual_forms.buttons import Button


class TextualFormApp(App):
    def compose(self) -> ComposeResult:
        yield Static("Order for beers...")
        yield Static(id="submitted-data")
        yield Form(
            fields=[
                StringField("name", required=True),
                IntegerField("age", required=True, min_value=21),
                StringField("email", required=True),
            ],
            buttons=[
                Button(
                    "Submit",
                    enabled_on_form_valid=True,
                )
            ],
        )

    def on_form_event(self, message: Form.Event) -> None:
        if message.event == "submit":
            table = Table(*message.data.keys())
            table.add_row(*message.data.values())
            self.query_one("#submitted-data").update(table)


if __name__ == "__main__":
    TextualFormApp().run()
