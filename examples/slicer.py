from trame.app import TrameApp
from trame.ui.vuetify3 import VAppLayout

from trame.widgets import html
from trame.widgets import vuetify3 as v3
from trame.widgets.radial_menu import RadItem, RadMenu, RadWheel


class TrameSlicerRadialMenu(RadMenu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # State variables
        self.state.selected_tool = [0, 0]
        self.state.brush_diameter_slider = 20
        self.state.use_sphere_brush = False
        self.state.brush_interaction_mode = "continuous"
        self.state.fill_mode = "erase_inside"
        self.state.range_mode = "unlimited"
        self.state.symmetric_distance = 0.0

        # Define tools
        self.marker_tools = [
            {
                "label": "Place points",
                "icon": "mdi-circle-small",
                "click": lambda: self.marker_tool(0),
            },
            {
                "label": "Place ruler",
                "icon": "mdi-ruler",
                "click": lambda: self.marker_tool(1),
            },
            {
                "label": "Place angle measurement",
                "icon": "mdi-angle-acute",
                "click": lambda: self.marker_tool(2),
            },
            {
                "label": "Place open curve",
                "icon": "mdi-vector-polyline",
                "click": lambda: self.marker_tool(3),
            },
            {
                "label": "Place closed curve",
                "icon": "mdi-vector-polygon",
                "click": lambda: self.marker_tool(4),
            },
            {
                "label": "Place plane",
                "icon": "mdi-square-outline",
                "click": lambda: self.marker_tool(5),
            },
            {
                "label": "Place ROI",
                "icon": "mdi-cube-outline",
                "click": lambda: self.marker_tool(6),
            },
            {
                "label": "Clear markers",
                "icon": "mdi-trash-can-outline",
                "click": lambda: self.marker_tool(7),
            },
        ]

        self.seg_tools = [
            {
                "label": "No tool",
                "icon": "mdi-cursor-default",
                "click": lambda: self.seg_tool(0),
            },
            {"label": "Paint", "icon": "mdi-brush", "click": lambda: self.seg_tool(1)},
            {"label": "Erase", "icon": "mdi-eraser", "click": lambda: self.seg_tool(2)},
            {
                "label": "Scissors",
                "icon": "mdi-content-cut",
                "click": lambda: self.seg_tool(3),
            },
            {"label": "Draw", "icon": "mdi-draw", "click": lambda: self.seg_tool(4)},
            {
                "label": "Logical Operators",
                "icon": "mdi-vector-intersection",
                "click": lambda: self.seg_tool(5),
            },
            {
                "label": "Threshold",
                "icon": "mdi-auto-fix",
                "click": lambda: self.seg_tool(6),
            },
            {
                "label": "Islands",
                "icon": "mdi-scatter-plot",
                "click": lambda: self.seg_tool(7),
            },
            {
                "label": "Smoothing",
                "icon": "mdi-square-rounded-outline",
                "click": lambda: self.seg_tool(8),
            },
        ]

        self.brush_interaction_modes = [
            {"label": "Continuous", "value": "continuous"},
            {"label": "Point By Point", "value": "point_by_point"},
        ]

        self.fill_modes = [
            {"label": "Erase Inside", "value": "erase_inside"},
            {"label": "Erase Outside", "value": "erase_outside"},
            {"label": "Fill Inside", "value": "fill_inside"},
            {"label": "Fill Outside", "value": "fill_outside"},
        ]

        self.range_modes = [
            {"label": "Unlimited", "value": "unlimited"},
            {"label": "Positive", "value": "positive"},
            {"label": "Negative", "value": "negative"},
            {"label": "Symmetric", "value": "symmetric"},
        ]

        self._build_ui()

    def marker_tool(self, tool_id):
        self.state.selected_tool = [0, tool_id]
        self.state.flush()

    def seg_tool(self, tool_id):
        self.state.selected_tool = [1, tool_id]
        self.state.flush()

    def _build_ui(self):
        with self:
            with RadWheel():
                for tool in self.marker_tools:
                    with (
                        RadItem(),
                        v3.VTooltip(text=tool["label"]),
                        html.Template(v_slot_activator="{ props }"),
                    ):
                        v3.VBtn(
                            icon=tool["icon"],
                            slim=True,
                            density="default",
                            variant="tonal",
                            theme="dark",
                            v_bind="props",
                            click=tool["click"],
                        )

                with RadWheel():
                    for tool in self.seg_tools:
                        with (
                            RadItem(),
                            v3.VTooltip(text=tool["label"]),
                            html.Template(v_slot_activator="{ props }"),
                        ):
                            v3.VBtn(
                                icon=tool["icon"],
                                slim=True,
                                density="default",
                                variant="tonal",
                                theme="dark",
                                v_bind="props",
                                click=tool["click"],
                            )

            # Side menu
            with self.side_menu():
                # Brush panel
                with (
                    v3.VCard(
                        v_if=(
                            "selected_tool[0] == 1 && (selected_tool[1] == 1 || selected_tool[1] == 2)",
                            [0, 0],
                        ),
                        width="300px",
                    ),
                    v3.VContainer(fluid=True),
                    v3.VRow(),
                ):
                    v3.VSlider(
                        v_model=("brush_diameter_slider", 20),
                        min=0,
                        max=100,
                        hide_details=True,
                    )
                    v3.VBtn(
                        icon="mdi-sphere",
                        variant="text",
                        click="use_sphere_brush = !use_sphere_brush",
                        color=("use_sphere_brush ? 'primary' : 'default'", ""),
                    )

                # Scissors panel
                with v3.VCard(
                    v_if=("selected_tool[0] == 1 && selected_tool[1] == 3", [0, 0]),
                    width="300px",
                ):
                    with (
                        v3.VRow(),
                        v3.VRadioGroup(
                            v_model=("brush_interaction_mode", "continuous"),
                            label="Brush interaction mode",
                            classes="pt-8",
                        ),
                    ):
                        for mode in self.brush_interaction_modes:
                            v3.VRadio(label=mode["label"], value=mode["value"])

                    with v3.VRow():
                        with (
                            v3.VCol(),
                            v3.VRadioGroup(
                                v_model=("fill_mode", "erase_inside"),
                                label="Operation",
                                hide_details=True,
                            ),
                        ):
                            for mode in self.fill_modes:
                                v3.VRadio(label=mode["label"], value=mode["value"])

                        with (
                            v3.VCol(),
                            v3.VRadioGroup(
                                v_model=("range_mode", "unlimited"),
                                label="Cut mode",
                                hide_details=True,
                            ),
                        ):
                            for mode in self.range_modes:
                                v3.VRadio(label=mode["label"], value=mode["value"])

                    with v3.VRow():
                        v3.VNumberInput(
                            v_model=("symmetric_distance", 0),
                            label="Distance (mm)",
                            disabled=("range_mode !== 'symmetric'", ""),
                            min=0,
                            max=9999,
                            step=0.0001,
                            precision=4,
                            density="comfortable",
                            control_variant="stacked",
                            hide_details=True,
                        )

                # Draw panel
                with (
                    v3.VCard(
                        v_if=("selected_tool[0] == 1 && selected_tool[1] == 4", [0, 0]),
                        width="300px",
                    ),
                    v3.VRow(),
                    v3.VRadioGroup(
                        v_model=("brush_interaction_mode", "continuous"),
                        label="Brush interaction mode",
                        classes="pt-8",
                    ),
                ):
                    for mode in self.brush_interaction_modes:
                        v3.VRadio(label=mode["label"], value=mode["value"])


class ExampleRadialMenu(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._build_ui()

    def _build_ui(self):
        with VAppLayout(self.server) as self.ui, self.ui.root:
            TrameSlicerRadialMenu()


def main():
    app = ExampleRadialMenu()
    app.server.start()


if __name__ == "__main__":
    main()
