def test_import():
    from trame.widgets.radial_menu import (  # noqa: PLC0415
        RadItem,
        RadMenu,
        RadWheel,
    )
    from trame_radial_menu.widgets.radial_menu import (  # noqa: F401, PLC0415, F811
        RadItem,
        RadMenu,
        RadWheel,
    )
