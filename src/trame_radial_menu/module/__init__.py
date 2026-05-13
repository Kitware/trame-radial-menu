from pathlib import Path

from trame_radial_menu import __version__

# Compute local path to serve
serve_path = str(Path(__file__).with_name("serve").resolve())
serve_directory = f"__trame_radial_menu_{__version__}"

# Serve directory for JS/CSS files
serve = {serve_directory: serve_path}

# List of JS files to load (usually from the serve path above)
scripts = [serve_directory + "/trame_radial_menu.umd.js"]

# List of CSS files to load (usually from the serve path above)
if (Path(serve_path) / "style.css").exists():
    styles = [serve_directory + "/style.css"]

# List of Vue plugins to install/load
vue_use = ["trame_radial_menu"]

# Uncomment to add entries to the shared state
# state = {}


# Optional if you want to execute custom initialization at module load
def setup(app, **kwargs):
    """Method called at initialization with possibly some custom keyword arguments"""
