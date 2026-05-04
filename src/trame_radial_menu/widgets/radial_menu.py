from contextlib import contextmanager

from trame_client.widgets.core import AbstractElement

from trame.widgets import vuetify3 as v3

from .. import module


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

    @contextmanager
    def sideMenu(self):
        v3.Template.slot_names.update(["side-menu"])
        with v3.Template(v_slot_side_menu=""):
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
