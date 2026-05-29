# This is the same as SegmentEditAreaUI but without the Collapsible

from trame_server.utils.typed_state import TypedState
from trame_slicer.app.ui import (
    DynamicSelect,
    SegmentEditAreaState,
    VolumeIntensityRangeMaskUI,
    enum_to_title,
)
from trame_slicer.segmentation import SegmentationOverwriteMode
from trame_vuetify.widgets.vuetify3 import (
    VCard,
    VCardText,
    VSelect,
)


class CustomSegmentEditAreaUI(VCard):
    def __init__(
        self, segment_edit_area_typed_state: TypedState[SegmentEditAreaState], **kwargs
    ):
        super().__init__(**kwargs)
        self._typed_state = segment_edit_area_typed_state

        with (
            self,
            VCardText(
                classes="align-center",
            ),
        ):
            DynamicSelect(
                label="Editable Area",
                state=self._typed_state.get_sub_state(
                    self._typed_state.name.mask_select
                ),
            )
            VSelect(
                label="Overwrite mode",
                v_model=self._typed_state.name.overwrite_mode,
                items=(
                    [
                        {
                            "title": enum_to_title(e),
                            "value": self._typed_state.encode(e),
                        }
                        for e in SegmentationOverwriteMode
                    ],
                ),
                item_value="value",
                item_title="title",
                hide_details=True,
                density="compact",
                style="margin-top: 5px;",
            )

            VolumeIntensityRangeMaskUI(classes="pt-6")
