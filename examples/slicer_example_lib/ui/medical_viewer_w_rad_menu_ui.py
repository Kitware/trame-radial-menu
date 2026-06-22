from trame_server import Server
from trame_slicer.app.ui import MedicalViewerUI, SegmentEditorUI
from trame_slicer.core import LayoutManager

from .markup_options_rad_menu_ui import MarkupOptionsRadMenuUI
from .tool_rad_menu_ui import ToolRadMenuUI


class MedicalViewerWRadMenuUI(MedicalViewerUI):
    def __init__(self, server: Server, layout_manager: LayoutManager):
        super().__init__(server, layout_manager)

        with self.layout:
            self._tool_rad_menu = ToolRadMenuUI(
                self.tool_registry[SegmentEditorUI], server
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

    @property
    def tool_rad_menu(self) -> ToolRadMenuUI:
        return self._tool_rad_menu

    @property
    def markup_options_rad_menu(self) -> MarkupOptionsRadMenuUI:
        return self._markup_options_rad_menu
