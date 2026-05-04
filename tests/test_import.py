def test_import():
    from radial_menu.widgets.radial_menu import CustomWidget  # noqa: PLC0415

    # For components only, the CustomWidget is also importable via trame
    from trame.widgets.radial_menu import CustomWidget  # noqa: F401, F811, PLC0415
