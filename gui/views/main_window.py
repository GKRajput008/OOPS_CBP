"""
Main Application Window
Integrates all tabs, header branding, responsive layout, status telemetry, and global styling.
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTabWidget,
    QStatusBar,
    QFrame,
)
from PyQt6.QtCore import Qt, QTimer
from datetime import datetime

from gui.controllers.app_controller import AppController
from gui.views.tab_dashboard import TabDashboard
from gui.views.tab_catalog import TabCatalog
from gui.views.tab_bom import TabBOM
from gui.views.tab_persistence import TabPersistence
from gui.views.styles import DARK_STYLESHEET


class MainWindow(QMainWindow):
    """
    Top-Level Desktop Application Window for Robotics Inventory & BOM Cost Estimator.
    """

    def __init__(self, controller: AppController):
        super().__init__()
        self.controller: AppController = controller

        self.setWindowTitle("Robotics Hardware Laboratory — Inventory & BOM Estimator [Phase 4]")
        self.resize(1280, 840)
        self.setMinimumSize(980, 680)

        # Apply Global Dark Stylesheet
        self.setStyleSheet(DARK_STYLESHEET)

        self._init_ui()
        self._setup_telemetry_clock()

        # Connect controller status notifications
        self.controller.status_notification.connect(self._show_status_message)

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(14, 12, 14, 10)
        root_layout.setSpacing(10)

        # -------------------------------------------------------------
        # App Header Banner
        # -------------------------------------------------------------
        header_card = QFrame()
        header_card.setProperty("class", "CardWidget")
        header_card.setStyleSheet("background-color: #0b0f19; border: 1px solid #1e293b; padding: 10px 16px;")
        header_layout = QHBoxLayout(header_card)
        header_layout.setContentsMargins(0, 0, 0, 0)

        # Brand / Logo
        title_box = QVBoxLayout()
        title_box.setSpacing(2)

        lbl_app_name = QLabel("ROBOTICS LABORATORY ERP & BOM ESTIMATOR")
        lbl_app_name.setStyleSheet(
            "font-size: 17px; font-weight: 800; color: #38bdf8; letter-spacing: 1px;"
        )

        lbl_app_desc = QLabel("Object-Oriented Hardware Subsystem • Phase 4 GUI Architecture")
        lbl_app_desc.setStyleSheet("font-size: 11px; color: #94a3b8; font-weight: 500;")

        title_box.addWidget(lbl_app_name)
        title_box.addWidget(lbl_app_desc)
        header_layout.addLayout(title_box)

        header_layout.addStretch()

        # Telemetry Clock and Engine Status
        telemetry_box = QHBoxLayout()
        telemetry_box.setSpacing(12)

        self.lbl_clock = QLabel()
        self.lbl_clock.setStyleSheet("color: #94a3b8; font-size: 12px; font-family: monospace;")
        telemetry_box.addWidget(self.lbl_clock)

        lbl_badge = QLabel("OOP C++ COMPLIANT")
        lbl_badge.setStyleSheet(
            "background-color: #0c4a6e; color: #38bdf8; border: 1px solid #0284c7; "
            "border-radius: 4px; padding: 4px 10px; font-size: 11px; font-weight: 700;"
        )
        telemetry_box.addWidget(lbl_badge)

        header_layout.addLayout(telemetry_box)
        root_layout.addWidget(header_card)

        # -------------------------------------------------------------
        # Tabbed Workspace
        # -------------------------------------------------------------
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.tab_dashboard = TabDashboard(self.controller)
        self.tab_catalog = TabCatalog(self.controller)
        self.tab_bom = TabBOM(self.controller)
        self.tab_persistence = TabPersistence(self.controller)

        self.tabs.addTab(self.tab_dashboard, "📊  Dashboard & Analytics")
        self.tabs.addTab(self.tab_catalog, "📦  Inventory Catalog")
        self.tabs.addTab(self.tab_bom, "🤖  Robotics Project BOM")
        self.tabs.addTab(self.tab_persistence, "💾  Persistence & File Transfer")

        root_layout.addWidget(self.tabs)

        # -------------------------------------------------------------
        # Status Bar
        # -------------------------------------------------------------
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Engine ready. Loaded inventory from CSV.")

    def _setup_telemetry_clock(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_clock)
        self.timer.start(1000)
        self._update_clock()

    def _update_clock(self):
        now_str = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        self.lbl_clock.setText(f"🕒 {now_str}")

    def _show_status_message(self, message: str, is_error: bool):
        color = "#f43f5e" if is_error else "#34d399"
        prefix = "❌ " if is_error else "✓ "
        self.status_bar.setStyleSheet(f"color: {color}; font-weight: 600;")
        self.status_bar.showMessage(f"{prefix}{message}", 7000)
