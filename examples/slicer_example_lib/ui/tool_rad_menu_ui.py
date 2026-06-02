from dataclasses import dataclass

from trame.widgets.html import Div, Template
from trame_server import Server
from trame_slicer.app.ui import SegmentEditorUI

from .rad_menu_placeholder_button import RadMenuPlaceholderButton
from .rad_menu_ui import RadMenuState, RadMenuUI
from .radial_markups_buttons_ui import RadialMarkupsButtonsUI
from .segmentation.custom_segment_editor_ui import CustomSegmentEditorUI


@dataclass
class ToolRadMenuState(RadMenuState):
    segment_mode: bool = False


class ToolRadMenuUI(RadMenuUI):
    # The objects must know the medical_view_ui to use its active_tool mechanism
    def __init__(self, segment_editor_ui: SegmentEditorUI, server: Server):
        super().__init__(
            server,
            ToolRadMenuState,
            ref="toolRadMenu",
            open_at_right_click_pos=False,
            color="#777d",
        )

        with self:
            self._markups_wheel = RadialMarkupsButtonsUI(
                v_if=f"!{self.opened_segmentation_wheel}"
            )
            self._segmentation_wheel = CustomSegmentEditorUI(
                segment_editor_ui, v_if=f"{self.opened_segmentation_wheel}"
            )

            with Template(v_slot_right_menu=""):
                self._segmentation_wheel.build_right_menu()

            with Template(v_slot_up_menu=""):
                self._segmentation_wheel.build_up_menu()

            with Template(v_slot_down_menu=""):
                self._segmentation_wheel.build_down_menu()

            with Template(v_slot_left_top=""):
                RadMenuPlaceholderButton(
                    text=(
                        f"{self.opened_segmentation_wheel} ? 'Markups' : 'Segmentation'",
                    ),
                    location="start",
                    icon=(
                        f"{self.opened_segmentation_wheel} ? 'mdi-circle-small' : 'mdi-brush'",
                    ),
                    click=self._toggle_segment_menu_selected,
                    variant="flat",
                )

            with Template(v_slot_right_top=""):
                RadMenuPlaceholderButton(
                    text=(
                        f"{self.name.right_menu_open} ? 'Close segmentation tool options' : 'Open segmentation tool options'",
                    ),
                    v_if=self.opened_segmentation_wheel,
                    icon=(
                        f"{self.name.right_menu_open} ? 'mdi-chevron-left' : 'mdi-chevron-right'",
                    ),
                    click=self._toggle_right_menu_opened,
                    active=self.name.right_menu_open,
                    variant="flat",
                )
                Div(v_else="")

            with Template(v_slot_top_left=""):
                RadMenuPlaceholderButton(
                    text=(
                        f"{self.name.up_menu_open} ? 'Close segments list' : 'Open segments list'",
                    ),
                    v_if=self.opened_segmentation_wheel,
                    location="top",
                    icon=(
                        f"{self.name.up_menu_open} ? 'mdi-chevron-down' : 'mdi-chevron-up'",
                    ),
                    click=self._toggle_up_menu_opened,
                    active=self.name.up_menu_open,
                    variant="flat",
                )

            with Template(v_slot_bottom_left=""):
                RadMenuPlaceholderButton(
                    text=(
                        f"{self.name.down_menu_open} ? 'Close masking options' : 'Open masking options'",
                    ),
                    v_if=self.opened_segmentation_wheel,
                    location="bottom",
                    icon="mdi-domino-mask",
                    click=self._toggle_down_menu_opened,
                    active=self.name.down_menu_open,
                    variant="flat",
                )

            with Template(v_slot_bottom_right=""):
                RadMenuPlaceholderButton(
                    v_if=self.opened_segmentation_wheel,
                    text="Undo",
                    location="bottom",
                    icon="mdi-undo",
                    click=segment_editor_ui.undo_clicked,
                    variant="flat",
                )
            with Template(v_slot_right_bottom=""):
                RadMenuPlaceholderButton(
                    v_if=self.opened_segmentation_wheel,
                    text="Redo",
                    location="end",
                    icon="mdi-redo",
                    click=segment_editor_ui.redo_clicked,
                    variant="flat",
                )

    @property
    def opened_segmentation_wheel(self):
        return self._typed_state.name.segment_mode

    def _toggle_segment_menu_selected(self):
        self._typed_state.data.segment_mode = not (self._typed_state.data.segment_mode)
        if not (self._typed_state.data.segment_mode):
            self.data.right_menu_open = False
            self.data.up_menu_open = False
            self.data.down_menu_open = False

    def _toggle_right_menu_opened(self):
        self.data.right_menu_open = not (self.data.right_menu_open)

    def _toggle_up_menu_opened(self):
        self.data.up_menu_open = not (self.data.up_menu_open)

    def _toggle_down_menu_opened(self):
        self.data.down_menu_open = not (self.data.down_menu_open)

    @property
    def markups_wheel(self):
        return self._markups_wheel

    @property
    def segmentation_wheel(self):
        return self._segmentation_wheel
