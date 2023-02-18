# Textual Forms

[![Python Versions](https://shields.io/pypi/pyversions/textual-inputs)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/textual-forms)](https://pepy.tech/project/textual-forms)
[![Downloads](https://pepy.tech/badge/textual-forms/month)](https://pepy.tech/project/textual-forms)

Dynamic forms for [Textual](https://github.com/willmcgugan/textual) TUI framework.

> #### Note: This library is still very much WIP 🧪. This means that breaking changes can be introduced at any point in time.

## About

Textual Forms aims to make it easy to add forms to your Textual-powered applications.

### Development Requirements

* python >=3.7,<4
* poetry
* textual >=0.11.0

## Install

```bash
pip install textual-forms
```

## Forms

`textual_forms.forms.Form`

## Buttons

`textual_forms.buttons.Button`

## Fields

`textual_forms.fields.StringField`

`textual_forms.fields.NumberField`

`textual_forms.fields.IntegerField`

### Custom fields and validators

```python
from __future__ import annotations

from typing import Any

from textual_forms.fields import Field
from textual_forms.validators import FieldValidator


class UUIDValidator(FieldValidator):
    def validate(self, value: str, rules: dict[str, Any]) -> tuple[bool, str | None]:
        return True, None


class UUIDField(Field):
    validator = UUIDValidator()

    def __init__(
        self,
        name: str,
        *,
        value: str | None = None,
        required: bool = False,
        placeholder: str | None = None,
        **kwargs,
    ):
        data: dict[str, Any] = {
            "name": name,
            "value": value,
            "required": required,
            "placeholder": placeholder,
            "rules": {},
        }
        super().__init__(data, **kwargs)
```

---

## Example

```python
from rich.table import Table
from textual.app import App, ComposeResult
from textual.widgets import Static

from textual_forms.forms import Form
from textual_forms.fields import StringField, IntegerField
from textual_forms.buttons import Button


class BasicTextualForm(App):
    def compose(self) -> ComposeResult:
        yield Static(id="submitted-data")
        yield Static("Order for beers")
        yield Form(
            fields=[
                StringField("name"),
                IntegerField("age", required=True, min_value=21),
            ],
            buttons=[
                Button(
                    "Submit",
                    enabled_on_form_valid=True,
                )
            ],
        )

    def on_form_event(self, message: Form.Event) -> None:
        if message.event == 'submit':
            table = Table(*message.data.keys())
            table.add_row(*message.data.values())
            self.query_one('#submitted-data').update(table)


if __name__ == '__main__':

    BasicTextualForm().run()

```

**Initial render**
<img width="1004" alt="Screenshot 2022-11-15 at 3 49 46 PM" src="https://user-images.githubusercontent.com/7029352/202023490-e6494105-a102-4d9d-9072-90872ecad41a.png">

**Valid form**
<img width="1006" alt="Screenshot 2022-11-15 at 3 51 15 PM" src="https://user-images.githubusercontent.com/7029352/202023592-1a16f742-6af2-4e88-a9d3-7b84339fd231.png">

**Invalid form**
<img width="1006" alt="Screenshot 2022-11-15 at 3 51 39 PM" src="https://user-images.githubusercontent.com/7029352/202023734-76ae0b55-01b4-48a4-8a34-7c972d7a7df9.png">

## Contributing

TBD
