from trame_client.widgets.core import AbstractElement

from trame.widgets import html

from .. import module

new_slot_names = [
    "right-menu",
    "left-menu",
    "up-menu",
    "down-menu",
    "central",
    "right-bottom",
    "bottom-right",
    "bottom-left",
    "left-bottom",
    "left-top",
    "top-left",
    "top-right",
    "right-top",
]
html.Template.slot_names.update(new_slot_names)


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
        self._attr_names += [
            ("open_at_right_click_pos", "openAtRightClickPos"),
            ("close_menu_button_radius", "closeMenuButtonRadius"),
            "color",
            ("drag_button_position", "dragButtonPosition"),
        ]


class RadWheel(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "rad-wheel",
            **kwargs,
        )
        self._attr_names += [
            ("inner_radius", "innerRadius"),
            ("outer_radius", "outerRadius"),
            ("begin_angle", "beginAngle"),
            ("end_angle", "endAngle"),
            "color",
        ]


class RadItem(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "rad-item",
            **kwargs,
        )
        self._attr_names += [
            "size",
        ]
