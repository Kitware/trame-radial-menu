from dataclasses import dataclass

import vtk
from slicer import (
    vtkMRMLDisplayNode,
    vtkMRMLScene,
)
from trame_server import Server
from trame_slicer.app.logic import BaseLogic
from trame_slicer.core import SlicerApp
from undo_stack import Signal
from vtkmodules.vtkCommonCore import VTK_OBJECT

from ...ui import MarkupsContextMenuUI
from .fiducial_options_logic import FiducialOptionsLogic


@dataclass
class MarkupsContextMenuLogicState:
    clicked_markups_node_id: str = ""


class MarkupsContextMenuLogic(BaseLogic[MarkupsContextMenuLogicState]):
    _set_clicked_node_type = Signal(str)

    def __init__(self, server: Server, slicer_app: SlicerApp):
        super().__init__(server, slicer_app, MarkupsContextMenuLogicState)
        self._markups_option_logics: list[BaseLogic] = []

        self.scene.AddObserver(vtkMRMLScene.NodeAddedEvent, self._on_node_added)
        self._register_logic(slicer_app, FiducialOptionsLogic)

    @vtk.calldata_type(VTK_OBJECT)
    def _on_node_added(self, _scene, _event_id, node):
        if isinstance(node, vtkMRMLDisplayNode):
            node.AddObserver(vtkMRMLDisplayNode.MenuEvent, self._on_menu_event)

    def _on_menu_event(self, caller, _event):
        markups_node = caller.GetDisplayableNode()
        if markups_node is None:
            return
        self._set_clicked_node_id(markups_node.GetID())
        self._set_clicked_node_type(type(markups_node).__name__)
        self.server.controller.markup_options_rad_menu_open_at_cursor()

    def _set_clicked_node_id(self, id: str):
        self.data.clicked_markups_node_id = id

    @property
    def clicked_node_id(self):
        return self.data.clicked_markups_node_id

    def _register_logic(self, slicer_app: SlicerApp, logic: type[BaseLogic]):
        self._markups_option_logics.append(logic(self.server, slicer_app, self))

    def set_ui(self, ui: MarkupsContextMenuUI):
        self._set_clicked_node_type.connect(ui.set_clicked_node_type)
        for logic in self._markups_option_logics:
            logic.set_ui(ui)
