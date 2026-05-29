from trame.app import TrameApp
from trame_server import Server
from trame_slicer.app.medical_viewer_app import (
    MedicalViewerLogic,
    MedicalViewerUI,
)
from trame_slicer.core import SlicerApp

from .logic import MedicalViewerWRadMenuLogic
from .ui import MedicalViewerWRadMenuUIExtension


class MedicalViewerWRadMenuApp(TrameApp):
    def __init__(self, server: Server = None):
        super().__init__(server)
        self._slicer_app = SlicerApp()
        self._base_logic = MedicalViewerLogic(self.server, self._slicer_app)
        self._base_ui = MedicalViewerUI(self.server, self._base_logic.layout_manager)
        self._base_logic.set_ui(self._base_ui)

        self._more_logic = MedicalViewerWRadMenuLogic(self.server, self._slicer_app)
        self._more_ui = MedicalViewerWRadMenuUIExtension(self._base_ui, self.server)
        self._more_logic.set_ui(self._more_ui)
