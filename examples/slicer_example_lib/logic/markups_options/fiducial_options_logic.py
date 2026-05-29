from typing import TYPE_CHECKING

from slicer import vtkMRMLMarkupsFiducialNode
from trame_server import Server
from trame_slicer.app.logic import BaseLogic
from trame_slicer.core import SlicerApp

from ...ui import FiducialMarkupOptionsUI, MarkupsContextMenuUI

if TYPE_CHECKING:
    from markups_context_menu_logic import MarkupsContextMenuLogic


class FiducialOptionsLogic(BaseLogic):
    def __init__(
        self,
        server: Server,
        slicer_app: SlicerApp,
        markups_context_menu_logic: "MarkupsContextMenuLogic",
    ):
        super().__init__(server, slicer_app, None)
        self._markups_context_menu_logic = markups_context_menu_logic

    def _delete_control_point(self):
        markups_node_id = self._markups_context_menu_logic.clicked_node_id
        markups_node: vtkMRMLMarkupsFiducialNode = self.scene.GetNodeByID(
            markups_node_id
        )

        display_node = markups_node.GetDisplayNode()
        if display_node is None:
            return
        active_index = display_node.GetActiveComponentIndex()
        if 0 <= active_index < markups_node.GetNumberOfControlPoints():
            markups_node.RemoveNthControlPoint(active_index)

    def _select_control_point(self):
        markups_node_id = self._markups_context_menu_logic.clicked_node_id
        markups_node: vtkMRMLMarkupsFiducialNode = self.scene.GetNodeByID(
            markups_node_id
        )
        display_node = markups_node.GetDisplayNode()
        if display_node is None:
            return

        active_index = display_node.GetActiveComponentIndex()
        if 0 <= active_index < markups_node.GetNumberOfControlPoints():
            markups_node.SetNthControlPointSelected(active_index, True)

    def _unselect_control_point(self):
        markups_node_id = self._markups_context_menu_logic.clicked_node_id
        markups_node: vtkMRMLMarkupsFiducialNode = self.scene.GetNodeByID(
            markups_node_id
        )
        display_node = markups_node.GetDisplayNode()
        if display_node is None:
            return

        active_index = display_node.GetActiveComponentIndex()
        if 0 <= active_index < markups_node.GetNumberOfControlPoints():
            markups_node.SetNthControlPointSelected(active_index, False)

    def _set_options_ui(self, options_ui: FiducialMarkupOptionsUI):
        options_ui.delete_control_point.connect(self._delete_control_point)
        options_ui.select_control_point.connect(self._select_control_point)
        options_ui.unselect_control_point.connect(self._unselect_control_point)

    def set_ui(self, ui: MarkupsContextMenuUI):
        self._set_options_ui(ui.markups_options_uis[vtkMRMLMarkupsFiducialNode])
