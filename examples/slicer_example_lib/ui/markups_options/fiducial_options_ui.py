from slicer import vtkMRMLMarkupsFiducialNode
from trame.widgets.vuetify3 import VList, VListItem, VListItemTitle
from undo_stack import Signal


class ListItemWTitle(VListItem):
    def __init__(self, title: str, action: callable):
        def click() -> None:
            self.ctrl.markup_options_rad_menu_close()
            action()

        super().__init__(click=click)
        with self:
            VListItemTitle(title)


class FiducialMarkupOptionsUI(VList):
    delete_control_point = Signal(vtkMRMLMarkupsFiducialNode)
    select_control_point = Signal(vtkMRMLMarkupsFiducialNode)
    unselect_control_point = Signal(vtkMRMLMarkupsFiducialNode)

    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)
        with self:
            ListItemWTitle("Delete control point", self.delete_control_point)
            ListItemWTitle("Select control point", self.select_control_point)
            ListItemWTitle("Unselect control point", self.unselect_control_point)
