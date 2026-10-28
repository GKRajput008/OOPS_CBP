"""
Tab 3: Robotics Project Bill of Materials (BOM) & Cost Estimator View.
Features live inventory selection, dynamic stock-cap bounding, itemized line totals,
and real-time financial margins (Subtotal, Tax, Shipping, Grand Total).
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFrame,
    QMessageBox,
    QFileDialog,
)
from PyQt6.QtCore import Qt

from gui.controllers.app_controller import AppController
from gui.views.styles import get_badge_stylesheet


class TabBOM(QWidget):
    """
    Robotics Project BOM & Financial Estimation Studio.
    """

    def __init__(self, controller: AppController, parent=None):
        super().__init__(parent)
        self.controller: AppController = controller
        self._init_ui()

        # Connect signals
        self.controller.inventory_changed.connect(self._sync_inventory_dropdown)
        self.controller.bom_changed.connect(self.refresh_bom_view)

        self._sync_inventory_dropdown()
        self.refresh_bom_view()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # -------------------------------------------------------------
        # 1. Project Configuration Header Card
        # -------------------------------------------------------------
        proj_config_card = QFrame()
        proj_config_card.setProperty("class", "CardWidget")
        config_layout = QHBoxLayout(proj_config_card)
        config_layout.setSpacing(16)
        config_layout.setContentsMargins(16, 12, 16, 12)

        # Project Name
        lbl_pname = QLabel("Robotics Build Project:")
        lbl_pname.setStyleSheet("font-weight: 700; color: #38bdf8;")
        config_layout.addWidget(lbl_pname)

        self.edit_project_name = QLineEdit(self.controller.project.project_name)
        self.edit_project_name.setPlaceholderText("Enter robot build or project name...")
        self.edit_project_name.textChanged.connect(self._on_project_config_changed)
        config_layout.addWidget(self.edit_project_name, stretch=3)

        # Tax Margin
        lbl_tax = QLabel("Tax Rate:")
        lbl_tax.setStyleSheet("font-weight: 600; color: #94a3b8;")
        config_layout.addWidget(lbl_tax)

        self.spin_tax_rate = QDoubleSpinBox()
        self.spin_tax_rate.setRange(0.0, 50.0)
        self.spin_tax_rate.setValue(self.controller.project.tax_rate * 100.0)
        self.spin_tax_rate.setSuffix(" %")
        self.spin_tax_rate.setDecimals(2)
        self.spin_tax_rate.valueChanged.connect(self._on_project_config_changed)
        config_layout.addWidget(self.spin_tax_rate)

        # Shipping & Logistics
        lbl_shipping = QLabel("Shipping / Logistics:")
        lbl_shipping.setStyleSheet("font-weight: 600; color: #94a3b8;")
        config_layout.addWidget(lbl_shipping)

        self.spin_shipping = QDoubleSpinBox()
        self.spin_shipping.setRange(0.0, 10000.0)
        self.spin_shipping.setValue(self.controller.project.shipping_cost)
        self.spin_shipping.setPrefix("$ ")
        self.spin_shipping.setDecimals(2)
        self.spin_shipping.valueChanged.connect(self._on_project_config_changed)
        config_layout.addWidget(self.spin_shipping)

        main_layout.addWidget(proj_config_card)

        # -------------------------------------------------------------
        # 2. Allocation Toolbar (Component Selector + Stock Cap Capable Spinbox)
        # -------------------------------------------------------------
        alloc_card = QFrame()
        alloc_card.setProperty("class", "CardWidget")
        alloc_layout = QHBoxLayout(alloc_card)
        alloc_layout.setSpacing(12)
        alloc_layout.setContentsMargins(16, 12, 16, 12)

        lbl_select = QLabel("Select Hardware:")
        lbl_select.setStyleSheet("font-weight: 600; color: #f8fafc;")
        alloc_layout.addWidget(lbl_select)

        self.combo_components = QComboBox()
        self.combo_components.currentIndexChanged.connect(self._on_selected_component_changed)
        alloc_layout.addWidget(self.combo_components, stretch=4)

        # Live Stock Cap Indicator Badge
        self.lbl_stock_cap = QLabel("Available: 0 units")
        self.lbl_stock_cap.setStyleSheet(
            "background-color: #0f172a; color: #38bdf8; border: 1px solid #334155; "
            "border-radius: 4px; padding: 6px 12px; font-weight: 600;"
        )
        alloc_layout.addWidget(self.lbl_stock_cap)

        lbl_qty = QLabel("Quantity:")
        lbl_qty.setStyleSheet("font-weight: 600; color: #f8fafc;")
        alloc_layout.addWidget(lbl_qty)

        self.spin_alloc_qty = QSpinBox()
        self.spin_alloc_qty.setRange(1, 1)
        self.spin_alloc_qty.setValue(1)
        alloc_layout.addWidget(self.spin_alloc_qty)

        btn_add_to_bom = QPushButton("+ Allocate to BOM")
        btn_add_to_bom.setProperty("class", "SuccessButton")
        btn_add_to_bom.clicked.connect(self._on_add_to_bom_clicked)
        alloc_layout.addWidget(btn_add_to_bom)

        main_layout.addWidget(alloc_card)

        # -------------------------------------------------------------
        # 3. Main Workspace: BOM Table (Left) + Cost Quote Preview Card (Right)
        # -------------------------------------------------------------
        split_layout = QHBoxLayout()
        split_layout.setSpacing(16)

        # BOM Itemized Table
        table_container = QFrame()
        table_container.setProperty("class", "CardWidget")
        table_layout = QVBoxLayout(table_container)
        table_layout.setSpacing(8)

        lbl_bom_table_title = QLabel("Itemized Bill of Materials (Active Build)")
        lbl_bom_table_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #f8fafc;")
        table_layout.addWidget(lbl_bom_table_title)

        self.table_bom = QTableWidget()
        self.table_bom.setColumnCount(7)
        self.table_bom.setHorizontalHeaderLabels([
            "ID",
            "Component Name",
            "Category",
            "Unit Price",
            "Allocated Qty",
            "Line Total ($)",
            "Action",
        ])
        self.table_bom.setAlternatingRowColors(True)
        self.table_bom.verticalHeader().setVisible(False)
        self.table_bom.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table_bom.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table_bom.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table_bom.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table_bom.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table_bom.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.table_bom.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        table_layout.addWidget(self.table_bom)

        split_layout.addWidget(table_container, stretch=7)

        # Dynamic Cost Quote Preview Panel (Right)
        quote_panel = QFrame()
        quote_panel.setProperty("class", "KPICard")
        quote_layout = QVBoxLayout(quote_panel)
        quote_layout.setSpacing(14)
        quote_layout.setContentsMargins(20, 20, 20, 20)

        lbl_quote_title = QLabel("ESTIMATED COST SUMMARY")
        lbl_quote_title.setStyleSheet("font-size: 13px; font-weight: 800; color: #38bdf8; letter-spacing: 0.5px;")
        quote_layout.addWidget(lbl_quote_title)

        self.lbl_quote_pname = QLabel("Autonomous Mobile Robot (AMR-01)")
        self.lbl_quote_pname.setStyleSheet("font-size: 16px; font-weight: 700; color: #ffffff;")
        quote_layout.addWidget(self.lbl_quote_pname)

        divider1 = QFrame()
        divider1.setFrameShape(QFrame.Shape.HLine)
        divider1.setStyleSheet("color: #334155; margin: 4px 0;")
        quote_layout.addWidget(divider1)

        # Financial Breakdown Rows
        grid_costs = QGridLayout()
        grid_costs.setVerticalSpacing(10)

        grid_costs.addWidget(self._make_cost_label("Allocated Items:"), 0, 0)
        self.lbl_bom_line_count = QLabel("0 components (0 units)")
        self.lbl_bom_line_count.setStyleSheet("color: #e2e8f0; font-weight: 600;")
        grid_costs.addWidget(self.lbl_bom_line_count, 0, 1, Qt.AlignmentFlag.AlignRight)

        grid_costs.addWidget(self._make_cost_label("Hardware Subtotal:"), 1, 0)
        self.lbl_subtotal = QLabel("$0.00")
        self.lbl_subtotal.setStyleSheet("color: #ffffff; font-weight: 700; font-size: 14px;")
        grid_costs.addWidget(self.lbl_subtotal, 1, 1, Qt.AlignmentFlag.AlignRight)

        grid_costs.addWidget(self._make_cost_label("Estimated Tax:"), 2, 0)
        self.lbl_tax_val = QLabel("$0.00")
        self.lbl_tax_val.setStyleSheet("color: #94a3b8;")
        grid_costs.addWidget(self.lbl_tax_val, 2, 1, Qt.AlignmentFlag.AlignRight)

        grid_costs.addWidget(self._make_cost_label("Shipping & Logistics:"), 3, 0)
        self.lbl_shipping_val = QLabel("$15.00")
        self.lbl_shipping_val.setStyleSheet("color: #94a3b8;")
        grid_costs.addWidget(self.lbl_shipping_val, 3, 1, Qt.AlignmentFlag.AlignRight)

        quote_layout.addLayout(grid_costs)

        divider2 = QFrame()
        divider2.setFrameShape(QFrame.Shape.HLine)
        divider2.setStyleSheet("color: #38bdf8; margin: 6px 0;")
        quote_layout.addWidget(divider2)

        # Grand Total Display
        lbl_grand_title = QLabel("GRAND TOTAL QUOTE")
        lbl_grand_title.setStyleSheet("font-size: 11px; font-weight: 800; color: #34d399; letter-spacing: 0.5px;")
        quote_layout.addWidget(lbl_grand_title)

        self.lbl_grand_total = QLabel("$0.00")
        self.lbl_grand_total.setStyleSheet("font-size: 30px; font-weight: 900; color: #34d399;")
        quote_layout.addWidget(self.lbl_grand_total)

        quote_layout.addStretch()

        # Quote Actions
        btn_export_receipt = QPushButton("📄 Export TXT Receipt")
        btn_export_receipt.setProperty("class", "SuccessButton")
        btn_export_receipt.clicked.connect(self._on_export_receipt)
        quote_layout.addWidget(btn_export_receipt)

        btn_clear_bom = QPushButton("Clear Build BOM")
        btn_clear_bom.setProperty("class", "DangerButton")
        btn_clear_bom.clicked.connect(self._on_clear_bom)
        quote_layout.addWidget(btn_clear_bom)

        split_layout.addWidget(quote_panel, stretch=4)
        main_layout.addLayout(split_layout)

    def _make_cost_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet("color: #94a3b8; font-size: 13px;")
        return lbl

    def _sync_inventory_dropdown(self):
        """Populates component selector from active inventory with real-time stock cap."""
        current_data = self.combo_components.currentData()
        self.combo_components.blockSignals(True)
        self.combo_components.clear()

        components = self.controller.inventory.get_all_components()
        for comp in components:
            if comp.quantity > 0:
                display_label = f"[{comp.id}] {comp.name} ({comp.get_type()}) — In Stock: {comp.quantity}"
                self.combo_components.addItem(display_label, comp.id)

        # Restore previous selection if still available
        index = self.combo_components.findData(current_data)
        if index >= 0:
            self.combo_components.setCurrentIndex(index)
        elif self.combo_components.count() > 0:
            self.combo_components.setCurrentIndex(0)

        self.combo_components.blockSignals(False)
        self._on_selected_component_changed()

    def _on_selected_component_changed(self):
        """Enforces real-time stock cap on the quantity spinbox."""
        cid = self.combo_components.currentData()
        if not cid:
            self.lbl_stock_cap.setText("No hardware selected")
            self.spin_alloc_qty.setRange(0, 0)
            self.spin_alloc_qty.setValue(0)
            return

        comp = self.controller.inventory.find_by_id(cid)
        if comp:
            # Check how much is already allocated in current project
            existing_item = self.controller.project.get_item_by_id(cid)
            already_alloc = existing_item.required_quantity if existing_item else 0
            available_to_alloc = max(0, comp.quantity - already_alloc)

            self.lbl_stock_cap.setText(
                f"Available: {comp.quantity} (Unallocated: {available_to_alloc})"
            )
            if available_to_alloc > 0:
                self.spin_alloc_qty.setRange(1, available_to_alloc)
                self.spin_alloc_qty.setValue(min(1, available_to_alloc))
                self.spin_alloc_qty.setEnabled(True)
            else:
                self.spin_alloc_qty.setRange(0, 0)
                self.spin_alloc_qty.setValue(0)
                self.spin_alloc_qty.setEnabled(False)

    def _on_project_config_changed(self):
        name = self.edit_project_name.text()
        tax_rate = self.spin_tax_rate.value() / 100.0
        shipping = self.spin_shipping.value()
        self.controller.set_project_config(name, tax_rate, shipping)

    def _on_add_to_bom_clicked(self):
        cid = self.combo_components.currentData()
        if not cid:
            QMessageBox.warning(self, "Selection Required", "Please select a component to allocate.")
            return

        qty = self.spin_alloc_qty.value()
        if qty <= 0:
            QMessageBox.warning(
                self, "Stock Unavailable", "Selected component has no remaining unallocated stock."
            )
            return

        self.controller.add_to_bom(cid, qty)
        self._on_selected_component_changed()

    def refresh_bom_view(self):
        """Refreshes the itemized table and recalculates cost quote preview."""
        bom = self.controller.get_bom_details()

        # Update Quote Header
        self.lbl_quote_pname.setText(bom["project_name"])

        # Populate Table
        items = bom["items"]
        self.table_bom.setRowCount(len(items))

        for row, item in enumerate(items):
            comp = item.component

            # ID
            item_id = QTableWidgetItem(comp.id)
            item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_bom.setItem(row, 0, item_id)

            # Name
            self.table_bom.setItem(row, 1, QTableWidgetItem(comp.name))

            # Category
            lbl_cat = QLabel(comp.get_type())
            lbl_cat.setStyleSheet(get_badge_stylesheet("category"))
            lbl_cat.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_bom.setCellWidget(row, 2, lbl_cat)

            # Unit Price
            item_price = QTableWidgetItem(f"${comp.price:,.2f}")
            item_price.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table_bom.setItem(row, 3, item_price)

            # Qty
            item_qty = QTableWidgetItem(f"{item.required_quantity}")
            item_qty.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_bom.setItem(row, 4, item_qty)

            # Line Total
            line_tot = item.get_line_total()
            item_total = QTableWidgetItem(f"${line_tot:,.2f}")
            item_total.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table_bom.setItem(row, 5, item_total)

            # Action: Remove Button
            btn_remove = QPushButton("Remove")
            btn_remove.setProperty("class", "DangerButton")
            btn_remove.setStyleSheet("padding: 3px 8px; font-size: 11px;")
            cid = comp.id
            btn_remove.clicked.connect(lambda checked, target_id=cid: self.controller.remove_from_bom(target_id))
            self.table_bom.setCellWidget(row, 6, btn_remove)

        # Update Cost Quote Preview
        self.lbl_bom_line_count.setText(f"{len(items)} components ({bom['parts_count']} total units)")
        self.lbl_subtotal.setText(f"${bom['subtotal']:,.2f}")
        self.lbl_tax_val.setText(f"${bom['tax']:,.2f} ({bom['tax_rate']*100:.1f}%)")
        self.lbl_shipping_val.setText(f"${bom['shipping']:,.2f}")
        self.lbl_grand_total.setText(f"${bom['grand_total']:,.2f}")

    def _on_export_receipt(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Export Project Receipt TXT",
            "project_receipt.txt",
            "Text Files (*.txt);;All Files (*)",
        )
        if filepath:
            self.controller.export_project_receipt(filepath)

    def _on_clear_bom(self):
        if not self.controller.project.get_items():
            return
        reply = QMessageBox.question(
            self,
            "Clear Bill of Materials",
            "Are you sure you want to clear all component allocations from this build?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.clear_bom()
            self._on_selected_component_changed()
