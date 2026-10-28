"""
Robotics Components Inventory Management System & Cost Estimator
Phase 4 Desktop GUI Application Entry Point.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Ensure root directory is on PYTHONPATH
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from gui.controllers.app_controller import AppController
from gui.views.main_window import MainWindow


def main():
    """Initializes and runs the Phase 4 Desktop GUI Application."""
    # Create Qt Application
    app = QApplication(sys.argv)
    app.setApplicationName("Robotics Laboratory ERP & BOM Estimator")
    app.setOrganizationName("RoboticsEngineeringLab")

    # Locate sample or user inventory.csv
    csv_path = os.path.join(ROOT_DIR, "inventory.csv")

    # Instantiate Model-View-Controller layers
    controller = AppController(default_csv_path=csv_path)
    window = MainWindow(controller=controller)

    # Show application window
    window.show()

    # Enter main event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
