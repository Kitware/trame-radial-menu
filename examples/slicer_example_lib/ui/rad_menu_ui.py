from dataclasses import dataclass

from trame_server import Server
from trame_server.utils.typed_state import TypedState

from trame.widgets.radial_menu import RadMenu


@dataclass
class RadMenuState:
    is_open: bool = False
    right_menu_open: bool = False
    up_menu_open: bool = False
    down_menu_open: bool = False
    left_menu_open: bool = False


class RadMenuUI(RadMenu):
    def __init__(
        self,
        server: Server,
        state_type: type[RadMenuState] = RadMenuState,
        ref: str = "",
        **kwargs: dict,
    ):
        self._typed_state = TypedState(server.state, state_type, namespace=ref)
        self._ref = ref

        super().__init__(
            ref=ref,
            v_model_open=self.name.is_open,
            v_model_rightmenuopen=self.name.right_menu_open,
            v_model_upmenuopen=self.name.up_menu_open,
            v_model_downmenuopen=self.name.down_menu_open,
            v_model_leftmenuopen=self.name.left_menu_open,
            **kwargs,
        )

    @property
    def name(self) -> RadMenuState:
        return self._typed_state.name

    @property
    def data(self) -> RadMenuState:
        return self._typed_state.data

    def close(self) -> None:
        self.data.is_open = False

    def open_at_cursor(self) -> None:
        self.server.js_call(ref=self._ref, method="openAtCursor")
