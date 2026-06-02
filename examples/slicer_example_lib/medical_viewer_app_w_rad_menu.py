from trame.app import TrameApp
from trame_server import Server
from trame_slicer.core import SlicerApp

from .logic import MedicalViewerWRadMenuLogic
from .ui import MedicalViewerWRadMenuUI


class MedicalViewerWRadMenuApp(TrameApp):
    def __init__(self, server: Server = None):
        super().__init__(server)

        self._slicer_app = SlicerApp()
        self._logic = MedicalViewerWRadMenuLogic(self.server, self._slicer_app)
        self._ui = MedicalViewerWRadMenuUI(self.server, self._logic.layout_manager)
        self._logic.set_ui(self._ui)
