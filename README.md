# Textual Forms

[![Python Versions](https://shields.io/pypi/pyversions/textual-inputs)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Dynamic forms for [Textual](https://github.com/willmcgugan/textual) TUI framework.

> #### Note: This library is still very much WIP 🧪

## About

Textual Forms aims to make it easy to add forms to your Textual-powered applications.

### Requirements

* python >=3.7,<4
* poetry

## Install

```bash
pip install textual-forms
```

### Form Field Schema

| Key         | Type        | Required | Options                 |
|-------------|-------------|----------|-------------------------|
| id          | str         | X        |                         |
| type        | str         |          | string, number, integer |
| value       | str, number |          |                         |
| required    | bool        |          |                         |
| placeholder | str         |          |                         |
| rules       | dict        |          |                         |

#### Type Rules

**string**

* min_length
* max_length

**integer**

* min
* max

**number**

* N/A

### Button Schema

| Key              | Type | Required | Options                          |
|------------------|------|----------|----------------------------------|
| id               | str  | x        |                                  |
| label            | str  | x        |                                  |
| variant          | str  |          | primary, error, success, warning |
| watch_form_valid | bool |          |                                  |

Note: If you set the `watch_form_valid` property, the button will only be enabled when the form is valid.

## Overriding Form Widgets

Documentation TBD

---

## Example

```python
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

```

![Screenshot 2022-11-14 at 9 51 54 PM](https://user-images.githubusercontent.com/7029352/201815737-bc2bea1c-aacb-498d-a58e-5d16e61e8718.png)

## Contributing

TBD
