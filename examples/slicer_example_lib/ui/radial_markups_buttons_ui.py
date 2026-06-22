from undo_stack import Signal

from trame.widgets.radial_menu import RadWheel

from .rad_item_button import RadItemButton


class RadialMarkupsButtonsUI(RadWheel):
    place_node_type = Signal(str, bool)
    clear_clicked = Signal()

    def __init__(self, **kwargs: dict):
        super().__init__(color="#aaad", innerRadius=(40,), outerRadius=(120,), **kwargs)
        self._markup_nodes = []

        with self:
            self._create_markups_buttons_on_radial_wheel(
                name="Place points",
                icon="mdi-circle-small",
                node_type="vtkMRMLMarkupsFiducialNode",
                is_persistent=True,
            )

            self._create_markups_buttons_on_radial_wheel(
                name="Place ruler",
                icon="mdi-ruler",
                node_type="vtkMRMLMarkupsLineNode",
                is_persistent=False,
            )

            self._create_markups_buttons_on_radial_wheel(
                name="Place angle measurement",
                icon="mdi-angle-acute",
                node_type="vtkMRMLMarkupsAngleNode",
                is_persistent=False,
            )

            self._create_markups_buttons_on_radial_wheel(
                name="Place open curve",
                icon="mdi-vector-polyline",
                node_type="vtkMRMLMarkupsCurveNode",
                is_persistent=True,
            )

            self._create_markups_buttons_on_radial_wheel(
                name="Place closed curve",
                icon="mdi-vector-polygon",
                node_type="vtkMRMLMarkupsClosedCurveNode",
                is_persistent=True,
            )

            self._create_markups_buttons_on_radial_wheel(
                name="Place plane",
                icon="mdi-square-outline",
                node_type="vtkMRMLMarkupsPlaneNode",
                is_persistent=False,
            )

            self._create_markups_buttons_on_radial_wheel(
                name="Place ROI",
                icon="mdi-cube-outline",
                node_type="vtkMRMLMarkupsROINode",
                is_persistent=False,
            )

            def clear_click() -> None:
                self.ctrl.tool_rad_menu_close()
                self.clear_clicked()

            RadItemButton(
                name="Clear Markups",
                icon="mdi-trash-can-outline",
                click=clear_click,
            )

    def _create_markups_buttons_on_radial_wheel(
        self, name: str, icon: str, node_type: str, is_persistent: bool
    ) -> None:
        def on_click() -> None:
            self.ctrl.tool_rad_menu_close()
            self.place_node_type(node_type, is_persistent)

        RadItemButton(name=name, icon=icon, click=on_click)
