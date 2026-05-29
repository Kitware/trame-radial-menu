from trame_server import Server
from trame_slicer.app.ui import MedicalViewerUI, SegmentEditorUI

from .markup_options_rad_menu_ui import MarkupOptionsRadMenuUI
from .tool_rad_menu_ui import ToolRadMenuUI


class MedicalViewerWRadMenuUIExtension:
    def __init__(self, medical_viewer_ui: MedicalViewerUI, server: Server):
        with medical_viewer_ui.layout:
            self._tool_rad_menu = ToolRadMenuUI(
                medical_viewer_ui.tool_registry[SegmentEditorUI], server
            )
            server.controller.tool_rad_menu_close = self._tool_rad_menu.close
            server.controller.tool_rad_menu_open_at_cursor = (
                self._tool_rad_menu.open_at_cursor
            )

            self._markup_options_rad_menu = MarkupOptionsRadMenuUI(server)
            server.controller.markup_options_rad_menu_close = (
                self._markup_options_rad_menu.close
            )
            server.controller.markup_options_rad_menu_open_at_cursor = (
                self._markup_options_rad_menu.open_at_cursor
            )

    def _is_tool_active(self, tool_ui_type: type):
        return self._obj._is_tool_active(tool_ui_type)

    @property
    def tool_rad_menu(self):
        return self._tool_rad_menu

    @property
    def markup_options_rad_menu(self):
        return self._markup_options_rad_menu
