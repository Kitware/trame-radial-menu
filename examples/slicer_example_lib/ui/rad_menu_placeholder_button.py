from trame.widgets.html import Div, Template
from trame.widgets.vuetify3 import VBtn, VTooltip


class RadMenuPlaceholderButton(Div):
    def __init__(self, **kwargs: dict):
        if "location" not in kwargs and "text" in kwargs:
            kwargs["location"] = "end"
        if "color" not in kwargs:
            kwargs["color"] = "#777d"
        if "size" not in kwargs:
            kwargs["size"] = 40

        super().__init__(v_if=kwargs.pop("v_if", ("true",)))

        with self:
            if "text" in kwargs:
                with (
                    VTooltip(text=kwargs.pop("text"), location=kwargs.pop("location")),
                    Template(v_slot_activator="{ props }"),
                ):
                    kwargs["v_bind"] = "props"
                    VBtn(**kwargs)
            else:
                VBtn(**kwargs)
