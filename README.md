# Textual Forms

[![Python Versions](https://shields.io/pypi/pyversions/textual-inputs)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Dynamic forms for [Textual](https://github.com/willmcgugan/textual) TUI framework.


## Example

```python
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
        'required': False,
        'placeholder': 'hi@example.com'
    },
]


class BasicTextualForm(App):
    def compose(self) -> ComposeResult:
        yield Static(id='submitted-data')
        yield TextualForm(FORM_DATA)

    def on_textual_form_submit(self, message: TextualForm.Submit) -> None:
        table = Table(*message.data.keys())
        table.add_row(*message.data.values())
        self.query_one('#submitted-data').update(table)


if __name__ == '__main__':
    BasicTextualForm().run()
```
