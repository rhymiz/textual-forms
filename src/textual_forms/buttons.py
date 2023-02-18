from __future__ import annotations

from rich.text import Text
from textual.widgets import Button as _Button
from textual.widgets._button import ButtonVariant


class Button(_Button):
    """
    A textual Button with a few customizations.
    """

    def __init__(
        self,
        label: str | Text | None = None,
        disabled: bool = False,
        variant: ButtonVariant = "default",
        *,
        id: str | None = None,
        name: str | None = None,
        classes: str | None = None,
        enabled_on_form_valid: bool = False,
    ) -> None:
        super().__init__(
            id=id,
            name=name,
            label=label,
            variant=variant,
            disabled=disabled,
            classes=classes,
        )
        self.enabled_on_form_valid = enabled_on_form_valid
