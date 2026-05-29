from trame.app import TrameApp
from trame.ui.vuetify3 import VAppLayout
from trame.widgets.html import H1, Template

from trame.widgets.radial_menu import RadItem, RadMenu, RadWheel


class MinimalExample(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._build_ui()

    def _build_ui(self):
        with (
            VAppLayout(self.server) as layout,
            layout.root,
            RadMenu(),
        ):
            with Template(v_slot_right_menu=""):
                H1("TEST")
            with RadWheel():
                with RadItem():
                    H1("TEST1")
                with RadItem():
                    H1("TEST2")
                with RadItem():
                    H1("TEST3")


if __name__ == "__main__":
    app = MinimalExample()
    app.server.start()
