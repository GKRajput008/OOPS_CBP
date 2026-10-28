"""
Tab 2: Inventory Catalog View
Features interactive hardware table with polymorphic specifications, live multicriteria search filter,
and CRUD action toolbars (Add, Edit Stock, Remove).
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QInputDialog,
    QMenu,
    QFrame,
)
from PyQt6.QtCore import Qt, QPoint

from gui.controllers.app_controller import AppController
from gui.views.dialog_add_component import AddComponentDialog
from gui.views.styles import get_badge_stylesheet


class NumericTableWidgetItem(QTableWidgetItem):
    """Custom TableWidgetItem supporting correct numeric sorting for currencies and quantities."""

    def __init__(self, value: float, display_text: str):
        super().__init__(display_text)
        self.numeric_value = value

    def __lt__(self, other):
        if isinstance(other, NumericTableWidgetItem):
            return self.numeric_value < other.numeric_value
        return super().__lt__(other)


class TabCatalog(QWidget):
    """
    Hardware Inventory Catalog table view with real-time polymorphic display,
    live searching, and stock management.
    """

    def __init__(self, controller: AppController, parent=None):
        super().__init__(parent)
        self.controller: AppController = controller
        self._init_ui()

        # Connect controller signals
        self.controller.inventory_changed.connect(self.populate_table)
        self.populate_table()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        # -------------------------------------------------------------
        # Filter & Action Toolbar Frame
        # -------------------------------------------------------------
        toolbar_frame = QFrame()
        toolbar_frame.setProperty("class", "CardWidget")
        toolbar_layout = QHBoxLayout(toolbar_frame)
        toolbar_layout.setContentsMargins(14, 12, 14, 12)
        toolbar_layout.setSpacing(12)

        # Search Input
        lbl_search = QLabel("Search:")
        lbl_search.setStyleSheet("font-weight: 600; color: #94a3b8;")
        toolbar_layout.addWidget(lbl_search)

        self.edit_search = QLineEdit()
        self.edit_search.setPlaceholderText("Filter by Name, ID, Category, or Specs...")
        self.edit_search.setClearButtonEnabled(True)
        self.edit_search.textChanged.connect(self.populate_table)
        toolbar_layout.addWidget(self.edit_search, stretch=3)

        # Category Filter Dropdown
        lbl_cat = QLabel("Category:")
        lbl_cat.setStyleSheet("font-weight: 600; color: #94a3b8;")
        toolbar_layout.addWidget(lbl_cat)

        self.combo_filter_cat = QComboBox()
        self.combo_filter_cat.addItems([
            "All",
            "Motor",
            "Sensor",
            "Controller",
            "Battery",
            "Converter",
            "Generic",
        ])
        self.combo_filter_cat.currentTextChanged.connect(self.populate_table)
        toolbar_layout.addWidget(self.combo_filter_cat, stretch=1)

        # Action Buttons
        toolbar_layout.addSpacing(16)

        btn_add = QPushButton("+ Add Component")
        btn_add.setProperty("class", "SuccessButton")
        btn_add.clicked.connect(self._on_add_component)
        toolbar_layout.addWidget(btn_add)

        btn_edit_stock = QPushButton("✏ Edit Stock")
        btn_edit_stock.setProperty("class", "SecondaryButton")
        btn_edit_stock.clicked.connect(self._on_edit_selected_stock)
        toolbar_layout.addWidget(btn_edit_stock)

        btn_remove = QPushButton("🗑 Remove")
        btn_remove.setProperty("class", "DangerButton")
        btn_remove.clicked.connect(self._on_remove_selected)
        toolbar_layout.addWidget(btn_remove)

        layout.addWidget(toolbar_frame)

        # -------------------------------------------------------------
        # Interactive Table Widget
        # -------------------------------------------------------------
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Hardware Name",
            "Category",
            "Unit Price ($)",
            "Stock Qty",
            "Valuation ($)",
            "Specialized Technical Specifications",
        ])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)

        # Context menu for right-click on table rows
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        self.table.doubleClicked.connect(self._on_edit_selected_stock)

        # Configure Header Resizing
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(1, 240)

        layout.addWidget(self.table)

        # Footer counter
        self.lbl_footer = QLabel("Showing 0 components")
        self.lbl_footer.setStyleSheet("color: #94a3b8; font-size: 12px; margin-top: 4px;")
        layout.addWidget(self.lbl_footer)

    def populate_table(self):
        """Re-populates table items matching active search filters."""
        search_query = self.edit_search.text()
        category_filter = self.combo_filter_cat.currentText()

        components = self.controller.get_filtered_inventory(search_query, category_filter)

        # Disable sorting temporarily during population to avoid row scramble
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(components))

        for row, comp in enumerate(components):
            # 0: ID
            item_id = QTableWidgetItem(comp.id)
            item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, item_id)

            # 1: Name
            item_name = QTableWidgetItem(comp.name)
            self.table.setItem(row, 1, item_name)

            # 2: Category Badge
            lbl_cat = QLabel(comp.get_type())
            lbl_cat.setStyleSheet(get_badge_stylesheet("category"))
            lbl_cat.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setCellWidget(row, 2, lbl_cat)

            # 3: Unit Price ($)
            item_price = NumericTableWidgetItem(comp.price, f"${comp.price:,.2f}")
            item_price.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 3, item_price)

            # 4: Stock Qty Badge
            badge_type = "in_stock"
            if comp.quantity == 0:
                badge_type = "out_of_stock"
            elif comp.quantity <= 10:
                badge_type = "low_stock"

            lbl_stock = QLabel(f"{comp.quantity} units")
            lbl_stock.setStyleSheet(get_badge_stylesheet(badge_type))
            lbl_stock.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setCellWidget(row, 4, lbl_stock)

            # 5: Valuation ($)
            total_val = comp.get_total_value()
            item_val = NumericTableWidgetItem(total_val, f"${total_val:,.2f}")
            item_val.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 5, item_val)

            # 6: Polymorphic Specs
            specs_summary = comp.get_specs_summary()
            item_specs = QTableWidgetItem(specs_summary)
            self.table.setItem(row, 6, item_specs)

        self.table.setSortingEnabled(True)
        self.lbl_footer.setText(
            f"Displaying {len(components)} of {self.controller.inventory.count()} total hardware components"
        )

    def _get_selected_component_id(self) -> str:
        row = self.table.currentRow()
        if row < 0:
            return ""
        id_item = self.table.item(row, 0)
        return id_item.text() if id_item else ""

    def _on_add_component(self):
        dialog = AddComponentDialog(self.controller, self)
        if dialog.exec():
            if dialog.created_component:
                self.controller.add_component(dialog.created_component)

    def _on_edit_selected_stock(self):
        cid = self._get_selected_component_id()
        if not cid:
            QMessageBox.information(self, "Select Component", "Please select a component row to edit its stock.")
            return

        comp = self.controller.inventory.find_by_id(cid)
        if not comp:
            return

        new_qty, ok = QInputDialog.getInt(
            self,
            "Edit Hardware Stock",
            f"Modify available inventory quantity for '{comp.name}' ({comp.id}):",
            comp.quantity,
            0,
            1000000,
        )
        if ok:
            self.controller.update_stock(cid, new_qty)

    def _on_remove_selected(self):
        cid = self._get_selected_component_id()
        if not cid:
            QMessageBox.information(self, "Select Component", "Please select a component row to remove.")
            return

        comp = self.controller.inventory.find_by_id(cid)
        if not comp:
            return

        reply = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Are you sure you want to delete '{comp.name}' (ID: {comp.id}) from inventory?\n"
            f"This will also remove any allocation in active Robotics Builds.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.remove_component(cid)

    def _show_context_menu(self, pos: QPoint):
        item = self.table.itemAt(pos)
        if not item:
            return

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background-color: #1e293b; color: #f8fafc; border: 1px solid #38bdf8; padding: 4px; }
            QMenu::item:selected { background-color: #0284c7; }
        """)

        action_edit = menu.addAction("✏ Edit Stock Quantity")
        action_edit.triggered.connect(self._on_edit_selected_stock)

        action_remove = menu.addAction("🗑 Delete Component")
        action_remove.triggered.connect(self._on_remove_selected)

        menu.exec(self.table.viewport().mapToGlobal(pos))
