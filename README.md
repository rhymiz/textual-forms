# Textual Forms

[![Python Versions](https://shields.io/pypi/pyversions/textual-inputs)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Dynamic forms for [Textual](https://github.com/willmcgugan/textual) TUI framework.

## Install

```bash
pip install textual-forms
```

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

The above snippet, produces the following screen:

<img width="1006" alt="Screenshot 2022-11-12 at 12 51 53 AM" src="https://user-images.githubusercontent.com/7029352/201459554-df7f605b-62cd-4160-80e9-32d6deac9739.png">
