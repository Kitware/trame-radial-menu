from trame.app import TrameApp
from trame.decorators import change
from trame.ui.vuetify3 import VAppLayout

from trame.widgets import html
from trame.widgets import vuetify3 as v3
from trame.widgets.radial_menu import RadItem, RadMenu, RadWheel


class TrameSlicerRadialMenu(RadMenu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def selectMenu(self, number):
        print(number)  # noqa: T201

    def _build_ui(self):
        with self:
            with RadWheel(
                color=("inner_color",),
                beginAngle=("inner_begin_angle",),
                endAngle=("inner_end_angle",),
                innerRadius=("inner_inner_radius",),
                outerRadius=("inner_outer_radius",),
            ):
                with RadItem(tooltipLabel="Button 1"):
                    v3.VBtn(icon="mdi-circle")
                with RadItem(tooltipLabel="Print 'TEST'"):
                    v3.VBtn(
                        icon="mdi-square-outline",
                        click=lambda: print("TEST"),  # noqa: T201
                    )
                with RadItem(tooltipLabel="Button 3", size=("ruler_size",)):
                    v3.VBtn(icon="mdi-ruler")

                with RadWheel(
                    color=("outer_color",),
                    beginAngle=("outer_begin_angle",),
                    endAngle=("outer_end_angle",),
                    innerRadius=("outer_inner_radius",),
                    outerRadius=("outer_outer_radius",),
                ):
                    with RadItem(tooltipLabel="Select side menu 0"):
                        v3.VBtn(
                            icon="mdi-trash-can-outline",
                            click=lambda: self.selectMenu(0),
                        )
                    with RadItem(tooltipLabel="Select side menu 1"):
                        v3.VBtn(
                            icon="mdi-cube-outline", click=lambda: self.selectMenu(1)
                        )
                    with RadItem(tooltipLabel="Select side menu 2"):
                        v3.VBtn(
                            icon="mdi-vector-polygon", click=lambda: self.selectMenu(2)
                        )
                    with RadItem(tooltipLabel="Select side menu 3"):
                        v3.VBtn(
                            icon="mdi-angle-acute", click=lambda: self.selectMenu(3)
                        )
                    with RadItem(tooltipLabel="Select side menu 4"):
                        v3.VBtn(
                            icon="mdi-vector-polyline", click=lambda: self.selectMenu(4)
                        )

            # Central placeholder
            with html.Template(v_slot_central_button=""):
                html.P("Middle placeholder")

            # Side menu
            with (
                html.Template(v_slot_side_menu=""),
                v3.VCard(title="Side Menu", color="#7772", width="200px"),
            ):
                html.P("Lorem ipsum")

            with (
                html.Template(v_slot_left_bottom=""),
                v3.VTooltip(text="Undo", location="start"),
                html.Template(v_slot_activator="{ props }"),
            ):
                v3.VBtn(icon="mdi-undo", v_bind="props")
            with (
                html.Template(v_slot_bottom_left=""),
                v3.VTooltip(text="Redo", location="bottom"),
                html.Template(v_slot_activator="{ props }"),
            ):
                v3.VBtn(icon="mdi-redo", v_bind="props")


class ExampleRadialMenu(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._build_ui()

    @change("use_outer_inner_radius")
    def change_outer_inner_radius(self, use_outer_inner_radius, **_):
        if not (use_outer_inner_radius):
            self.state["outer_inner_radius"] = -1

    @change("use_outer_outer_radius")
    def change_outer_outer_radius(self, use_outer_outer_radius, **_):
        if not (use_outer_outer_radius):
            self.state["outer_outer_radius"] = -1

    def _build_ui(self):
        with VAppLayout(self.server) as self.ui, self.ui.root:
            html.H1("Right click to open the radial menu")
            with v3.VCard(width="500px", color="#eeee"):
                v3.VSwitch(
                    v_model=("close_menu_button", True),
                    label="Central close menu button",
                )
                v3.VSwitch(v_model=("show_rad_menu", False), label="Open radial menu")
                v3.VColorPicker(v_model=("menu_color", "#47FF4077"))
                v3.VSwitch(
                    v_model=("show_rad_menu_side_menu", False), label="Open side menu"
                )
                with v3.VCard(title="Inner Wheel", color=("inner_color",)):
                    v3.VSlider(
                        thumb_label="always",
                        v_model=("inner_inner_radius", 40.0),
                        label="inner radius",
                        min=0,
                        max=360,
                    )
                    v3.VSlider(
                        thumb_label="always",
                        v_model=("inner_outer_radius", 100.0),
                        label="outer radius",
                        min=0,
                        max=360,
                    )
                    v3.VColorPicker(v_model=("inner_color", "#777777ee"))
                    v3.VSlider(
                        thumb_label="always",
                        v_model=("inner_begin_angle", 0),
                        label="inner begin angle",
                        min=0,
                        max=360,
                    )
                    v3.VSlider(
                        thumb_label="always",
                        v_model=("inner_end_angle", 360.0),
                        label="inner end angle",
                        min=0,
                        max=360,
                    )
                    v3.VSlider(
                        thumb_label="always",
                        v_model=("ruler_size", 1.0),
                        label="ruler size",
                        min=0,
                        max=4,
                    )
                with v3.VCard(title="Outer Wheel", color=("outer_color",)):
                    v3.VCheckbox(
                        label="force inner radius",
                        v_model=("use_outer_inner_radius", False),
                    )
                    v3.VSlider(
                        v_if="use_outer_inner_radius",
                        thumb_label="always",
                        v_model=("outer_inner_radius", -1.0),
                        label="inner radius",
                        min=0,
                        max=360,
                    )
                    v3.VCheckbox(
                        label="force outer radius",
                        v_model=("use_outer_outer_radius", False),
                    )
                    v3.VSlider(
                        v_if="use_outer_outer_radius",
                        thumb_label="always",
                        v_model=("outer_outer_radius", -1.0),
                        label="outer radius",
                        min=0,
                        max=360,
                    )
                    v3.VColorPicker(v_model=("outer_color", "#777777bb"))
                    v3.VSlider(
                        thumb_label="always",
                        v_model=("outer_begin_angle", 0),
                        label="outer begin angle",
                        min=0,
                        max=360,
                    )
                    v3.VSlider(
                        thumb_label="always",
                        v_model=("outer_end_angle", 360.0),
                        label="outer end angle",
                        min=0,
                        max=360,
                    )

            TrameSlicerRadialMenu(
                v_model_open=("show_rad_menu",),
                v_model_sidemenuopen=("show_rad_menu_side_menu",),
                color=("menu_color",),
                closeMenu=("close_menu_button",),
            )


def main():
    app = ExampleRadialMenu()
    app.server.start()


if __name__ == "__main__":
    main()
