from radial_menu.widgets.radial_menu import *  # noqa: F403


def initialize(server):
    from radial_menu import module  # noqa: PLC0415

    server.enable_module(module)
