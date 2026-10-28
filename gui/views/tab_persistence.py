"""
Tab 4: Persistence & File Transfer View.
Provides one-click Load CSV, Save CSV, Export TXT/Invoice, and a live bidirectional file inspection viewer.
"""

import os
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QFrame,
    QMessageBox,
    QTabWidget,
    QApplication,
)
from PyQt6.QtCore import Qt
from gui.controllers.app_controller import AppController


class TabPersistence(QWidget):
    """
    Persistence & File Transfer Studio handling CSV sync, file I/O operations,
    and live preview rendering.
    """

    def __init__(self, controller: AppController, parent=None):
        super().__init__(parent)
        self.controller: AppController = controller
        self._init_ui()

        # Connect signals
        self.controller.inventory_changed.connect(self.refresh_previews)
        self.controller.bom_changed.connect(self.refresh_previews)
        self.refresh_previews()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # -------------------------------------------------------------
        # Action Toolbar Frame
        # -------------------------------------------------------------
        action_card = QFrame()
        action_card.setProperty("class", "CardWidget")
        action_layout = QHBoxLayout(action_card)
        action_layout.setSpacing(12)
        action_layout.setContentsMargins(16, 14, 16, 14)

        btn_load_csv = QPushButton("📥 Load CSV File")
        btn_load_csv.setProperty("class", "SecondaryButton")
        btn_load_csv.clicked.connect(self._on_load_csv)
        action_layout.addWidget(btn_load_csv)

        btn_save_csv = QPushButton("💾 Save Inventory CSV")
        btn_save_csv.setProperty("class", "SuccessButton")
        btn_save_csv.clicked.connect(self._on_save_csv)
        action_layout.addWidget(btn_save_csv)

        btn_export_receipt = QPushButton("📄 Export Project TXT Invoice")
        btn_export_receipt.clicked.connect(self._on_export_receipt)
        action_layout.addWidget(btn_export_receipt)

        btn_copy = QPushButton("📋 Copy Invoice to Clipboard")
        btn_copy.setProperty("class", "SecondaryButton")
        btn_copy.clicked.connect(self._on_copy_invoice)
        action_layout.addWidget(btn_copy)

        action_layout.addStretch()

        self.lbl_active_file = QLabel(f"Active File: {os.path.abspath(self.controller.current_csv_path)}")
        self.lbl_active_file.setStyleSheet("color: #38bdf8; font-size: 11px; font-family: monospace;")
        action_layout.addWidget(self.lbl_active_file)

        main_layout.addWidget(action_card)

        # -------------------------------------------------------------
        # Preview Pane with Tabs: CSV Stream vs Formatted Build Receipt
        # -------------------------------------------------------------
        preview_container = QFrame()
        preview_container.setProperty("class", "CardWidget")
        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setSpacing(10)

        lbl_pane_title = QLabel("Live File Streams & Invoice Inspector")
        lbl_pane_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #f8fafc;")
        preview_layout.addWidget(lbl_pane_title)

        self.tab_previews = QTabWidget()

        # Subtab 1: Formatted TXT Invoice Preview
        tab_invoice = QWidget()
        layout_inv = QVBoxLayout(tab_invoice)
        self.text_invoice_preview = QTextEdit()
        self.text_invoice_preview.setReadOnly(True)
        self.text_invoice_preview.setStyleSheet("""
            QTextEdit {
                background-color: #0b0f19;
                color: #38bdf8;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
                border: 1px solid #1e293b;
                padding: 12px;
            }
        """)
        layout_inv.addWidget(self.text_invoice_preview)
        self.tab_previews.addTab(tab_invoice, "📄 Active Project Build Receipt (TXT)")

        # Subtab 2: Raw CSV Serialization Preview
        tab_csv = QWidget()
        layout_csv = QVBoxLayout(tab_csv)
        self.text_csv_preview = QTextEdit()
        self.text_csv_preview.setReadOnly(True)
        self.text_csv_preview.setStyleSheet("""
            QTextEdit {
                background-color: #0b0f19;
                color: #34d399;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
                border: 1px solid #1e293b;
                padding: 12px;
            }
        """)
        layout_csv.addWidget(self.text_csv_preview)
        self.tab_previews.addTab(tab_csv, "🗄 Serialized CSV Inventory Stream")

        preview_layout.addWidget(self.tab_previews)
        main_layout.addWidget(preview_container)

    def refresh_previews(self):
        """Generates live serialized text representations for instant inspection."""
        # Update Invoice preview
        receipt_text = self.controller.project.generate_receipt_text()
        self.text_invoice_preview.setPlainText(receipt_text)

        # Update CSV preview
        components = self.controller.inventory.get_all_components()
        csv_lines = [comp.to_csv() for comp in components]
        self.text_csv_preview.setPlainText("\n".join(csv_lines))

        self.lbl_active_file.setText(f"Active File: {os.path.abspath(self.controller.current_csv_path)}")

    def _on_load_csv(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Select Inventory CSV File",
            self.controller.current_csv_path,
            "CSV Files (*.csv);;All Files (*)",
        )
        if filepath:
            self.controller.load_inventory_csv(filepath)

    def _on_save_csv(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Save Inventory to CSV",
            self.controller.current_csv_path,
            "CSV Files (*.csv);;All Files (*)",
        )
        if filepath:
            self.controller.save_inventory_csv(filepath)

    def _on_export_receipt(self):
        default_name = f"{self.controller.project.project_name.replace(' ', '_').lower()}_receipt.txt"
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Export Project Receipt TXT",
            default_name,
            "Text Files (*.txt);;All Files (*)",
        )
        if filepath:
            self.controller.export_project_receipt(filepath)

    def _on_copy_invoice(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_invoice_preview.toPlainText())
        QMessageBox.information(
            self, "Copied to Clipboard", "Official Project Invoice receipt copied to clipboard!"
        )
