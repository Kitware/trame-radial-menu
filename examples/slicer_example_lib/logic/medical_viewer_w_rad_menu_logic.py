from slicer import vtkMRMLApplicationLogic
from trame_server import Server
from trame_slicer.app.logic import MedicalViewerLogic
from trame_slicer.core import SlicerApp

from ..ui import MedicalViewerWRadMenuUI
from .markups_options import MarkupsContextMenuLogic
from .radial_markups_button_logic import RadialMarkupsButtonLogic


class MedicalViewerWRadMenuLogic(MedicalViewerLogic):
    def __init__(self, server: Server, slicer_app: SlicerApp):
        super().__init__(server, slicer_app)

        self._radial_markups_button_logic = RadialMarkupsButtonLogic(server, slicer_app)
        self._markups_context_menu_logic = MarkupsContextMenuLogic(server, slicer_app)

        # Intercept right click on slicer's background to open tool radial menu
        slicer_app.app_logic.AddObserver(
            vtkMRMLApplicationLogic.ShowViewContextMenuEvent,
            lambda *_: server.controller.tool_rad_menu_open_at_cursor(),
        )

    def set_ui(self, ui: MedicalViewerWRadMenuUI):
        super().set_ui(ui)
        self._radial_markups_button_logic.set_ui(ui.tool_rad_menu.markups_wheel)
        self._markups_context_menu_logic.set_ui(
            ui.markup_options_rad_menu.markups_context_menu
        )
