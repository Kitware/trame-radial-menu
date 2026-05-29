from trame_server import Server

try:
    from slicer_example_lib import MedicalViewerWRadMenuApp
except ModuleNotFoundError:
    from slicer_example_lib import MedicalViewerWRadMenuApp


def main(server: Server = None, **kwargs):
    app = MedicalViewerWRadMenuApp(server)
    app.server.start(**kwargs)


if __name__ == "__main__":
    main()
