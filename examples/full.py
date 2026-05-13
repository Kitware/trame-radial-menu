from trame.app import TrameApp
from trame.decorators import change
from trame.ui.vuetify3 import VAppLayout

from trame.widgets import html
from trame.widgets import vuetify3 as v3
from trame.widgets.radial_menu import RadItem, RadMenu, RadWheel


class CustomButtonRadItem(RadItem):
    def __init__(self, text: str, icon: str, click=lambda: None, **kwargs):
        super().__init__(**kwargs)
        with self, v3.VTooltip(text=text), html.Template(v_slot_activator="{ props }"):
            v3.VBtn(icon=icon, click=click, v_bind="props")


class TrameSlicerRadialMenu(RadMenu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def set_selected_menu(self, number: int):
        self.state.selected_menu = number

    def _build_ui(self):
        with self:
            with RadWheel(
                color=("inner_color",),
                begin_angle=("inner_begin_angle",),
                end_angle=("inner_end_angle",),
                inner_radius=("inner_inner_radius",),
                outer_radius=("inner_outer_radius",),
            ):
                CustomButtonRadItem(text="Button 1", icon="mdi-circle")
                CustomButtonRadItem(
                    text="Print 'TEST'",
                    icon="mdi-square-outline",
                    click=lambda: print("TEST"),  # noqa: T201
                )
                CustomButtonRadItem(
                    text="Button 3", icon="mdi-ruler", size=("ruler_size",)
                )

                with RadWheel(
                    color=("outer_color",),
                    begin_angle=("outer_begin_angle",),
                    end_angle=("outer_end_angle",),
                    inner_radius=("outer_inner_radius",),
                    outer_radius=("outer_outer_radius",),
                ):
                    CustomButtonRadItem(
                        text="Select side menu 0",
                        icon="mdi-trash-can-outline",
                        click=lambda: self.set_selected_menu(0),
                    )
                    CustomButtonRadItem(
                        text="Select side menu 1",
                        icon="mdi-cube-outline",
                        click=lambda: self.set_selected_menu(1),
                    )
                    CustomButtonRadItem(
                        text="Select side menu 2",
                        icon="mdi-vector-polygon",
                        click=lambda: self.set_selected_menu(2),
                    )
                    CustomButtonRadItem(
                        text="Select side menu 3",
                        icon="mdi-angle-acute",
                        click=lambda: self.set_selected_menu(3),
                    )
                    CustomButtonRadItem(
                        text="Select side menu 4",
                        icon="mdi-vector-polyline",
                        click=lambda: self.set_selected_menu(4),
                    )

            # Central placeholder
            with html.Template(v_slot_central="", v_if="close_menu_button"):
                html.P("Middle placeholder")

            # Right menu
            with (
                html.Template(v_slot_right_menu=""),
                v3.VCard(title="Right Menu", color="#7772", width="200px"),
            ):
                html.P("Lorem ipsum")

            # Left menu
            with (
                html.Template(v_slot_left_menu=""),
                v3.VCard(title="Left Menu", color="#7772", width="200px"),
            ):
                html.P("Lorem ipsum")

            # Up menu
            with (
                html.Template(v_slot_up_menu=""),
                v3.VCard(title="Up Menu", color="#7772", width="200px"),
            ):
                html.P("Lorem ipsum")

            # Down menu
            with (
                html.Template(v_slot_down_menu=""),
                v3.VCard(title="Down Menu", color="#7772", width="200px"),
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

    @change("use_close_menu_button_radius")
    def change_close_menu_button_redius(self, use_close_menu_button_radius, **_):
        if not (use_close_menu_button_radius):
            self.state["close_menu_button_radius"] = -1

    @change("use_outer_inner_radius")
    def change_outer_inner_radius(self, use_outer_inner_radius, **_):
        if not (use_outer_inner_radius):
            self.state["outer_inner_radius"] = -1

    @change("use_outer_outer_radius")
    def change_outer_outer_radius(self, use_outer_outer_radius, **_):
        if not (use_outer_outer_radius):
            self.state["outer_outer_radius"] = -1

    @change("selected_menu")
    def change_selected_menu(self, selected_menu, **_):
        print(f"Menu {selected_menu} selected !")  # noqa: T201

    def _build_ui(self):
        with VAppLayout(self.server) as self.ui, self.ui.root:
            html.H1("Right click to open the radial menu")
            with v3.VCard(width="500px", color="#eeee"):
                v3.VSwitch(
                    v_model=("close_menu_button", False),
                    label="Replace central close menu button",
                )
                v3.VCheckbox(
                    label="force central button radius",
                    v_model=("use_close_menu_button_radius", False),
                )
                v3.VSlider(
                    v_if="use_close_menu_button_radius",
                    thumb_label="always",
                    v_model=("close_menu_button_radius", -1.0),
                    label="inner radius",
                    min=0,
                    max=360,
                )
                v3.VSwitch(v_model=("show_rad_menu", False), label="Open radial menu")
                v3.VColorPicker(v_model=("menu_color", "#47FF4077"))
                v3.VSwitch(
                    v_model=("show_rad_menu_right_menu", False), label="Open right menu"
                )
                v3.VSwitch(
                    v_model=("show_rad_menu_left_menu", False), label="Open left menu"
                )
                v3.VSwitch(
                    v_model=("show_rad_menu_up_menu", False), label="Open up menu"
                )
                v3.VSwitch(
                    v_model=("show_rad_menu_down_menu", False), label="Open down menu"
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
                v_model_rightmenuopen=("show_rad_menu_right_menu",),
                v_model_leftmenuopen=("show_rad_menu_left_menu",),
                v_model_upmenuopen=("show_rad_menu_up_menu",),
                v_model_downmenuopen=("show_rad_menu_down_menu",),
                color=("menu_color",),
                close_menu_button_radius=("close_menu_button_radius",),
            )


def main():
    app = ExampleRadialMenu()
    app.server.start()


if __name__ == "__main__":
    main()
