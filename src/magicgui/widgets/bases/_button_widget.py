from __future__ import annotations

from typing import Any, Callable

from psygnal import Signal, SignalInstance

from magicgui.types import Undefined, _Undefined
from magicgui.widgets import protocols

from ._value_widget import ValueWidget


class ButtonWidget(ValueWidget[bool]):
    """Widget with a value, Wraps ButtonWidgetProtocol.

    Parameters
    ----------
    value : bool
        The starting state of the widget.
    text : str, optional
        The text to display on the button. If not provided, will use ``name``.
    bind : Any, optional
        A value or callback to bind this widget, then whenever `widget.value` is
        accessed, the value provided here will be returned.  ``value`` can be a
        callable, in which case ``value(self)`` will be returned (i.e. your callback
        must accept a single parameter, which is this widget instance.).
    nullable : bool, optional
        If `True`, the widget will accepts `None` as a valid value, by default `False`.
    **base_widget_kwargs : Any
        All additional keyword arguments are passed to the base
        :class:`~magicgui.widgets.Widget` constructor.
    """

    _widget: protocols.ButtonWidgetProtocol
    changed = Signal(object)

    def __init__(
        self,
        value: bool | _Undefined = Undefined,
        *,
        text: str | None = None,
        bind: bool | Callable[[ValueWidget], bool] | _Undefined = Undefined,
        nullable: bool = False,
        **base_widget_kwargs: Any,
    ) -> None:
        if text and base_widget_kwargs.get("label"):
            from warnings import warn

            warn(
                "'text' and 'label' are synonymous for button widgets. To suppress this"
                " warning, only provide one of the two kwargs."
            )
        text = text or base_widget_kwargs.get("label")
        # TODO: make a backend hook that lets backends inject their optional API
        # ipywidgets button texts are called descriptions
        text = text or base_widget_kwargs.pop("description", None)
        super().__init__(
            value=value, bind=bind, nullable=nullable, **base_widget_kwargs
        )
        self.text = (text or self.name).replace("_", " ")

    @property
    def options(self) -> dict:
        """Return options currently being used in this widget."""
        d = super().options.copy()
        d.update({"text": self.text})
        return d

    @property
    def text(self) -> str:
        """Text of the widget."""
        return self._widget._mgui_get_text()

    @text.setter
    def text(self, value: str) -> None:
        self._widget._mgui_set_text(value)

    @property
    def clicked(self) -> SignalInstance:
        """Alias for changed event."""
        return self.changed
