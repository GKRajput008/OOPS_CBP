"""
GUI Views Package
"""

from .styles import DARK_STYLESHEET
from .dialog_add_component import AddComponentDialog
from .tab_dashboard import TabDashboard
from .tab_catalog import TabCatalog
from .tab_bom import TabBOM
from .tab_persistence import TabPersistence
from .main_window import MainWindow

__all__ = [
    "DARK_STYLESHEET",
    "AddComponentDialog",
    "TabDashboard",
    "TabCatalog",
    "TabBOM",
    "TabPersistence",
    "MainWindow",
]
