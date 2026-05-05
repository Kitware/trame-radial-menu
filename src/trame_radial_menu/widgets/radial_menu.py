from contextlib import contextmanager

from trame_client.widgets.core import AbstractElement

from trame.widgets import html

from .. import module

html.Template.slot_names.update(["side-menu"])


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


__all__ = [
    "RadItem",
    "RadMenu",
    "RadWheel",
]


class RadMenu(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "rad-menu",
            **kwargs,
        )
        self._event_names += [("click_close", "click:close")]

    @contextmanager
    def side_menu(self):
        html.Template.slot_names.update(["side-menu"])
        with html.Template(v_slot_side_menu=""):
            yield


class RadWheel(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "rad-wheel",
            **kwargs,
        )
        self._attr_names += [
            "innerRadius",
            "outerRadius",
            "beginAngle",
            "endAngle",
            "color",
        ]


class RadItem(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "rad-item",
            **kwargs,
        )
        self._attr_names += [
            "label",
            "icon",
            "size",
            "closeOnClick",
        ]
