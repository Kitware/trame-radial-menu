from slicer import vtkMRMLMarkupsFiducialNode
from trame.widgets.vuetify3 import VList, VListItem, VListItemTitle
from undo_stack import Signal


def sequence(f1, f2):
    def sequenced_function():
        f1()
        f2()

    return sequenced_function


class FiducialMarkupOptionsUI(VList):
    delete_control_point = Signal(vtkMRMLMarkupsFiducialNode)
    select_control_point = Signal(vtkMRMLMarkupsFiducialNode)
    unselect_control_point = Signal(vtkMRMLMarkupsFiducialNode)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self:
            with VListItem(
                click=sequence(
                    self.ctrl.markup_options_rad_menu_close, self.delete_control_point
                )
            ):
                VListItemTitle("Delete control point")
            with VListItem(
                click=sequence(
                    self.ctrl.markup_options_rad_menu_close, self.select_control_point
                )
            ):
                VListItemTitle("Select control point")
            with VListItem(
                click=sequence(
                    self.ctrl.markup_options_rad_menu_close, self.unselect_control_point
                )
            ):
                VListItemTitle("Unselect control point")
