from trame.app import TrameApp
from trame.ui.vuetify3 import VAppLayout

from trame.widgets import html
from trame.widgets import vuetify3 as v3
from trame.widgets.radial_menu import RadItem, RadMenu, RadWheel


class RadButtonItem(RadItem):
    def __init__(self, label, icon, click=None, **kwargs):
        super().__init__(**kwargs)
        with (
            self,
            v3.VTooltip(text=label),
            html.Template(v_slot_activator="{ props }"),
        ):
            v3.VBtn(
                icon=icon,
                slim=True,
                density="default",
                v_bind="props",
                click=click,
            )


class TrameSlicerRadialMenu(RadMenu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.selectedMenu = 0

        self._build_ui()

    def selectMenu(self, number):
        self.state.selectedMenu = number
        self.selectedMenu = number
        print(self.state.selectedMenu)  # noqa: T201

    def _build_ui(self):
        with self:
            with RadWheel(
                color=("innerColor",),
                beginAngle=("innerBeginAngle",),
                endAngle=("innerEndAngle",),
                innerRadius=("innerInnerRadius",),
                outerRadius=("innerOuterRadius",),
            ):
                RadButtonItem("Button 1", "mdi-circle")
                RadButtonItem(
                    "Print 'TEST'",
                    "mdi-square-outline",
                    lambda: print("TEST"),  # noqa: T201
                )
                RadButtonItem("Button 3", "mdi-ruler", size=("rulerSize",))

                with RadWheel(color=("outerColor",)):
                    RadButtonItem(
                        "Select side menu 0",
                        "mdi-trash-can-outline",
                        lambda: self.selectMenu(0),
                    )
                    RadButtonItem(
                        "Select side menu 1",
                        "mdi-cube-outline",
                        lambda: self.selectMenu(1),
                    )
                    RadButtonItem(
                        "Select side menu 2",
                        "mdi-vector-polygon",
                        lambda: self.selectMenu(2),
                    )
                    RadButtonItem(
                        "Select side menu 3",
                        "mdi-angle-acute",
                        lambda: self.selectMenu(3),
                    )
                    RadButtonItem(
                        "Select side menu 4",
                        "mdi-vector-polyline",
                        lambda: self.selectMenu(4),
                    )

            # Side menu
            with (
                self.side_menu(),
                v3.VCard(title="Side Menu", color="#7772", width="200px"),
            ):
                html.P("Lorem ipsum")


class ExampleRadialMenu(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._build_ui()

    def _build_ui(self):
        with VAppLayout(self.server) as self.ui, self.ui.root:
            html.H1("Right click to open the radial menu")
            with v3.VCard(width="500px", color="#eeee"):
                v3.VSwitch(v_model=("show_rad_menu", False), label="Opened radial menu")
                v3.VColorPicker(v_model=("menuColor", "#47FF4077"))
                v3.VSwitch(
                    v_model=("show_rad_menu_side_menu", False), label="Opened side menu"
                )
                with v3.VCard(title="Inner Wheel", color=("innerColor",)):
                    v3.VSlider(
                        thumb_label="always",
                        v_model=("innerInnerRadius", 40.0),
                        label="inner radius",
                        min=0,
                        max=360,
                    )
                    v3.VSlider(
                        thumb_label="always",
                        v_model=("innerOuterRadius", 100.0),
                        label="outer radius",
                        min=0,
                        max=360,
                    )
                    v3.VColorPicker(v_model=("innerColor", "#777777ee"))
                    v3.VSlider(
                        thumb_label="always",
                        v_model=("innerBeginAngle", 0),
                        label="inner begin angle",
                        min=0,
                        max=360,
                    )
                    v3.VSlider(
                        thumb_label="always",
                        v_model=("innerEndAngle", 360.0),
                        label="inner end angle",
                        min=0,
                        max=360,
                    )
                    v3.VSlider(
                        thumb_label="always",
                        v_model=("rulerSize", 1.0),
                        label="ruler size",
                        min=0,
                        max=4,
                    )
                with v3.VCard(title="Outer Wheel", color=("outerColor",)):
                    v3.VColorPicker(v_model=("outerColor", "#777777bb"))
                    v3.VSlider(
                        thumb_label="always",
                        v_model=("outerBeginAngle", 0),
                        label="outer begin angle",
                        min=0,
                        max=360,
                    )
                    v3.VSlider(
                        thumb_label="always",
                        v_model=("outerEndAngle", 360.0),
                        label="outer end angle",
                        min=0,
                        max=360,
                    )

            TrameSlicerRadialMenu(
                v_model_open=("show_rad_menu",),
                v_model_sidemenuopen=("show_rad_menu_side_menu",),
                color=("menuColor",),
            )


def main():
    app = ExampleRadialMenu()
    app.server.start()


if __name__ == "__main__":
    main()
