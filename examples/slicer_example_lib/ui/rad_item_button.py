from collections.abc import Callable

from trame.widgets.vuetify3 import VBtn, VTooltip

from trame.widgets import html
from trame.widgets.radial_menu import RadItem


class RadItemButton(RadItem):
    def __init__(
        self,
        name: str,
        icon: str | tuple,
        click: Callable | str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        with self, VTooltip(text=name), html.Template(v_slot_activator="{ props }"):
            VBtn(
                icon=icon,
                click=click,
                v_bind="props",
                color="#777d",
                variant="flat",
            )
