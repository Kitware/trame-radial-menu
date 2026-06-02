from trame.widgets.html import Div, Template
from trame_server import Server

from .markups_options import MarkupsContextMenuUI
from .rad_menu_ui import RadMenuUI


class MarkupOptionsRadMenuUI(RadMenuUI):
    def __init__(self, server: Server):
        super().__init__(
            server,
            ref="markupOptionsRadMenu",
            open_at_right_click_pos=False,
            color="#777d",
        )
        with self._typed_state.state:
            self.data.right_menu_open = True
        with self:
            with Template(v_slot_right_menu=""):
                self._markups_context_menu = MarkupsContextMenuUI()

            with Template(v_slot_right_top=""):
                Div()
            with Template(v_slot_top_right=""):
                Div()
            with Template(v_slot_central=""):
                Div()

    @property
    def markups_context_menu(self):
        return self._markups_context_menu
