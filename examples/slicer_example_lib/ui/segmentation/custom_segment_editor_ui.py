# This is the same as SegmentEditorUI but with separated in down_menu, up_menu and right_menu

from trame.widgets.html import Template
from trame.widgets.vuetify3 import VBtn, VCard, VCardActions, VCardText, VTooltip
from trame_slicer.app.ui import (
    DrawEffectUI,
    IslandsEffectUI,
    LogicalOperatorsEffectUI,
    PaintEffectUI,
    ScissorsEffectUI,
    SegmentEditorUI,
    SegmentList,
    SmoothingEffectUI,
    ThresholdEffectUI,
)
from trame_slicer.segmentation import (
    SegmentationEffect,
    SegmentationEffectDraw,
    SegmentationEffectErase,
    SegmentationEffectIslands,
    SegmentationEffectLogicalOperators,
    SegmentationEffectNoTool,
    SegmentationEffectPaint,
    SegmentationEffectScissors,
    SegmentationEffectSmoothing,
    SegmentationEffectThreshold,
)

from trame.widgets.radial_menu import RadWheel

from ..rad_item_button import RadItemButton
from .custom_segment_edit_area_ui import CustomSegmentEditAreaUI


class CustomSegmentEditorUI(RadWheel):
    def __init__(self, segment_editor_ui: SegmentEditorUI, **kwargs):
        super().__init__(color="#aaad", outer_radius=(120,), **kwargs)
        self._segment_editor_ui = segment_editor_ui
        self._build_ui()

    def _build_ui(self, **kwargs):
        with self:
            self._create_radial_effect_button(
                "No tool",
                "mdi-cursor-default",
                SegmentationEffectNoTool,
                **kwargs,
            )
            self._create_radial_effect_button(
                "Paint",
                "mdi-brush",
                SegmentationEffectPaint,
                **kwargs,
            )
            self._create_radial_effect_button(
                "Erase",
                "mdi-eraser",
                SegmentationEffectErase,
                **kwargs,
            )
            self._create_radial_effect_button(
                "Scissors",
                "mdi-content-cut",
                SegmentationEffectScissors,
                **kwargs,
            )
            self._create_radial_effect_button(
                "Draw",
                "mdi-draw",
                SegmentationEffectDraw,
                **kwargs,
            )
            if all:
                self._create_radial_effect_button(
                    "Logical Operators",
                    "mdi-vector-intersection",
                    SegmentationEffectLogicalOperators,
                )
                self._create_radial_effect_button(
                    "Threshold",
                    "mdi-auto-fix",
                    SegmentationEffectThreshold,
                )
                self._create_radial_effect_button(
                    "Islands",
                    "mdi-scatter-plot",
                    SegmentationEffectIslands,
                    **kwargs,
                )
                self._create_radial_effect_button(
                    "Smoothing",
                    "mdi-square-rounded-outline",
                    SegmentationEffectSmoothing,
                    **kwargs,
                )

    def build_right_menu(self):
        with VCard(width=310, classes="pa-4"):
            self._segment_editor_ui._register_effect_ui(
                SegmentationEffectPaint, PaintEffectUI
            )
            self._segment_editor_ui._register_effect_ui(
                SegmentationEffectErase, PaintEffectUI
            )
            self._segment_editor_ui._register_effect_ui(
                SegmentationEffectLogicalOperators, LogicalOperatorsEffectUI
            )
            self._segment_editor_ui._register_effect_ui(
                SegmentationEffectThreshold, ThresholdEffectUI
            )
            self._segment_editor_ui._register_effect_ui(
                SegmentationEffectIslands, IslandsEffectUI
            )
            self._segment_editor_ui._register_effect_ui(
                SegmentationEffectDraw, DrawEffectUI
            )
            self._segment_editor_ui._register_effect_ui(
                SegmentationEffectScissors, ScissorsEffectUI
            )
            self._segment_editor_ui._register_effect_ui(
                SegmentationEffectSmoothing, SmoothingEffectUI
            )

    def build_up_menu(self):
        with VCard(variant="flat", height="50%", width="310px"):
            with VCardText(style="height: calc(100% - 64px); overflow-y: auto;"):
                self._segment_list = SegmentList(
                    typed_state=self._segment_editor_ui.sub_state(
                        self._segment_editor_ui._typed_state.name.segment_list
                    ),
                    edit_ui=self._segment_editor_ui.edit_ui,
                )
                self._segment_list.toggle_segment_visibility_clicked.connect(
                    self._segment_editor_ui.toggle_segment_visibility_clicked
                )
                self._segment_list.edit_segment_color_clicked.connect(
                    self._segment_editor_ui.edit_segment_color_clicked
                )
                self._segment_list.delete_segment_clicked.connect(
                    self._segment_editor_ui.delete_segment_clicked
                )
                self._segment_list.select_segment_clicked.connect(
                    self._segment_editor_ui.select_segment_clicked
                )

            with (
                VCardActions(classes="justify-center", style="height: 64px;"),
                VTooltip(text="Add Segment"),
                Template(v_slot_activator="{ props }"),
            ):
                VBtn(
                    v_bind="props",
                    variant="tonal",
                    icon="mdi-plus",
                    click=self._segment_editor_ui.add_segment_clicked,
                )

    def build_down_menu(self):
        self._segment_edit_area = CustomSegmentEditAreaUI(
            segment_edit_area_typed_state=self._segment_editor_ui.sub_state(
                self._segment_editor_ui._typed_state.name.segment_edit_area
            ),
            variant="flat",
        )

    def _create_radial_effect_button(
        self,
        name: str,
        icon: str,
        effect_type: type[SegmentationEffect],
        **kwargs,
    ):
        RadItemButton(
            name=name,
            icon=icon,
            click=lambda: self._segment_editor_ui.effect_button_clicked(effect_type),
            active=self._segment_editor_ui.is_active_effect(effect_type),
            **kwargs,
        )
