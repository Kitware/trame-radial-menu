from dataclasses import dataclass
from typing import Any

from slicer import vtkMRMLMarkupsFiducialNode, vtkMRMLMarkupsNode
from trame.widgets.vuetify3 import VList
from trame_server.utils.typed_state import TypedState

from .fiducial_options_ui import FiducialMarkupOptionsUI


@dataclass
class MarkupsContextMenuState:
    clicked_node_type: str = ""


class MarkupsContextMenuUI(VList):
    def __init__(self):
        super().__init__(width="300px")
        self._typed_state = TypedState(self.state, MarkupsContextMenuState)
        self._markups_options_uis: dict[type[vtkMRMLMarkupsNode], Any] = {}

        with self:
            self._register_ui(vtkMRMLMarkupsFiducialNode, FiducialMarkupOptionsUI)

    def _is_selected_markup_type(self, markup_type: vtkMRMLMarkupsNode):
        return f"{self.name.clicked_node_type} == '{markup_type.__name__}'"

    def _register_ui(self, markup_type: vtkMRMLMarkupsNode, markup_ui):
        ui_instance = markup_ui(v_if=self._is_selected_markup_type(markup_type))
        self._markups_options_uis[markup_type] = ui_instance

    def set_clicked_node_type(self, node_type: str):
        self.data.clicked_node_type = node_type

    @property
    def name(self):
        return self._typed_state.name

    @property
    def data(self):
        return self._typed_state.data

    @property
    def markups_options_uis(self):
        return self._markups_options_uis
