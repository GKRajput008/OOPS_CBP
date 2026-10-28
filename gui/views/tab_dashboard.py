"""
Tab 1: Dashboard & Analytics View
Features real-time KPI cards, category breakdown progress meters, and critical low-stock alert monitoring.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QFrame,
    QProgressBar,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QInputDialog,
    QScrollArea,
)
from PyQt6.QtCore import Qt
from gui.controllers.app_controller import AppController
from gui.views.styles import get_badge_stylesheet


class TabDashboard(QWidget):
    """
    Analytics Dashboard displaying real-time financial valuation,
    hardware catalog distribution, and supply-chain shortage warnings.
    """

    def __init__(self, controller: AppController, parent=None):
        super().__init__(parent)
        self.controller: AppController = controller
        self._init_ui()
        self.controller.inventory_changed.connect(self.refresh_metrics)
        self.refresh_metrics()

    def _init_ui(self):
        # Outer scroll area so all resolutions look great
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content_widget = QWidget()
        self.layout_content = QVBoxLayout(content_widget)
        self.layout_content.setSpacing(20)
        self.layout_content.setContentsMargins(20, 20, 20, 20)

        # -------------------------------------------------------------
        # 1. Header Banner
        # -------------------------------------------------------------
        header_frame = QFrame()
        header_frame.setProperty("class", "CardWidget")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(16, 12, 16, 12)

        header_text_layout = QVBoxLayout()
        lbl_dash_title = QLabel("Robotics Hardware Laboratory Analytics")
        lbl_dash_title.setStyleSheet("font-size: 20px; font-weight: 700; color: #38bdf8;")
        lbl_dash_sub = QLabel("Real-time telemetry, asset valuation, and stock replenishment metrics.")
        lbl_dash_sub.setStyleSheet("color: #94a3b8; font-size: 13px;")
        header_text_layout.addWidget(lbl_dash_title)
        header_text_layout.addWidget(lbl_dash_sub)
        header_layout.addLayout(header_text_layout)

        header_layout.addStretch()

        self.lbl_system_status = QLabel("● SYSTEM ACTIVE & SYNCED")
        self.lbl_system_status.setStyleSheet(
            "color: #34d399; font-weight: 700; font-size: 12px; background-color: #064e3b; "
            "padding: 6px 14px; border-radius: 6px; border: 1px solid #059669;"
        )
        header_layout.addWidget(self.lbl_system_status)

        self.layout_content.addWidget(header_frame)

        # -------------------------------------------------------------
        # 2. KPI Cards Grid (4 Key Indicators)
        # -------------------------------------------------------------
        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(16)

        # KPI 1: Valuation
        self.card_val, self.lbl_val_num, self.lbl_val_sub = self._create_kpi_card(
            "TOTAL INVENTORY VALUATION", "$0.00", "Capital invested across all components", "#38bdf8"
        )
        kpi_grid.addWidget(self.card_val, 0, 0)

        # KPI 2: Catalog SKUs
        self.card_sku, self.lbl_sku_num, self.lbl_sku_sub = self._create_kpi_card(
            "UNIQUE COMPONENT SKUs", "0", "Polymorphic hardware specifications", "#818cf8"
        )
        kpi_grid.addWidget(self.card_sku, 0, 1)

        # KPI 3: Total Physical Units
        self.card_units, self.lbl_units_num, self.lbl_units_sub = self._create_kpi_card(
            "TOTAL IN-STOCK UNITS", "0", "Discrete units available in lab warehouse", "#34d399"
        )
        kpi_grid.addWidget(self.card_units, 0, 2)

        # KPI 4: Shortage Alerts
        self.card_shortage, self.lbl_shortage_num, self.lbl_shortage_sub = self._create_kpi_card(
            "STOCK SHORTAGE ALERTS", "0", "Components with stock ≤ 10 units", "#f43f5e"
        )
        kpi_grid.addWidget(self.card_shortage, 0, 3)

        self.layout_content.addLayout(kpi_grid)

        # -------------------------------------------------------------
        # 3. Middle Section: Category Breakdown + Critical Alerts
        # -------------------------------------------------------------
        mid_layout = QHBoxLayout()
        mid_layout.setSpacing(16)

        # Left Column: Category Breakdown Chart / Progress Meters
        cat_card = QFrame()
        cat_card.setProperty("class", "CardWidget")
        self.layout_categories = QVBoxLayout(cat_card)
        self.layout_categories.setSpacing(14)

        cat_title_layout = QHBoxLayout()
        lbl_cat_title = QLabel("Hardware Category Allocation")
        lbl_cat_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #f8fafc;")
        cat_title_layout.addWidget(lbl_cat_title)
        cat_title_layout.addStretch()
        lbl_cat_sub = QLabel("Model Share & Capital Distribution")
        lbl_cat_sub.setStyleSheet("color: #94a3b8; font-size: 12px;")
        cat_title_layout.addWidget(lbl_cat_sub)
        self.layout_categories.addLayout(cat_title_layout)

        # Container for dynamic category progress rows
        self.container_cat_meters = QVBoxLayout()
        self.container_cat_meters.setSpacing(12)
        self.layout_categories.addLayout(self.container_cat_meters)
        self.layout_categories.addStretch()

        mid_layout.addWidget(cat_card, stretch=5)

        # Right Column: Critical Stock Shortage Monitor Table
        alert_card = QFrame()
        alert_card.setProperty("class", "CardWidget")
        layout_alerts = QVBoxLayout(alert_card)
        layout_alerts.setSpacing(10)

        alert_header = QHBoxLayout()
        lbl_alert_title = QLabel("Replenishment Action Feed (Low Stock)")
        lbl_alert_title.setStyleSheet("font-size: 15px; font-weight: 700; color: #fb7185;")
        alert_header.addWidget(lbl_alert_title)
        alert_header.addStretch()
        layout_alerts.addLayout(alert_header)

        self.table_alerts = QTableWidget()
        self.table_alerts.setColumnCount(5)
        self.table_alerts.setHorizontalHeaderLabels([
            "ID", "Component Name", "Category", "Stock", "Action"
        ])
        self.table_alerts.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table_alerts.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table_alerts.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table_alerts.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table_alerts.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table_alerts.verticalHeader().setVisible(False)
        self.table_alerts.setAlternatingRowColors(True)
        self.table_alerts.setStyleSheet("max-height: 280px;")
        layout_alerts.addWidget(self.table_alerts)

        mid_layout.addWidget(alert_card, stretch=6)

        self.layout_content.addLayout(mid_layout)

        scroll_area.setWidget(content_widget)
        outer_layout.addWidget(scroll_area)

    def _create_kpi_card(self, title: str, value: str, subtitle: str, color_hex: str):
        card = QFrame()
        card.setProperty("class", "KPICard")
        layout = QVBoxLayout(card)
        layout.setSpacing(6)
        layout.setContentsMargins(16, 16, 16, 16)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"font-size: 11px; font-weight: 700; color: {color_hex}; letter-spacing: 0.5px;")

        lbl_val = QLabel(value)
        lbl_val.setStyleSheet(f"font-size: 26px; font-weight: 800; color: #ffffff;")

        lbl_sub = QLabel(subtitle)
        lbl_sub.setStyleSheet("font-size: 11px; color: #94a3b8;")

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_val)
        layout.addWidget(lbl_sub)
        return card, lbl_val, lbl_sub

    def refresh_metrics(self):
        """Fetches fresh data from controller and updates KPI cards and meters."""
        kpis = self.controller.get_dashboard_kpis()

        # Update KPI Cards
        self.lbl_val_num.setText(f"${kpis['total_valuation']:,.2f}")
        self.lbl_sku_num.setText(f"{kpis['unique_count']}")
        self.lbl_units_num.setText(f"{kpis['total_units']:,}")
        self.lbl_shortage_num.setText(f"{kpis['low_stock_count']}")

        if kpis["low_stock_count"] > 0:
            self.card_shortage.setStyleSheet(
                "QFrame.KPICard { border: 1px solid #f43f5e; background-color: #2b111a; }"
            )
        else:
            self.card_shortage.setStyleSheet(
                "QFrame.KPICard { border: 1px solid #334155; }"
            )

        # Update Category Breakdown Meters
        # Clear existing rows in layout
        while self.container_cat_meters.count():
            item = self.container_cat_meters.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        cat_counts = kpis["category_counts"]
        cat_vals = kpis["category_valuations"]
        total_skus = max(1, kpis["unique_count"])

        categories = ["Motor", "Sensor", "Controller", "Battery", "Converter", "Generic"]
        for cat in categories:
            count = cat_counts.get(cat, 0)
            val = cat_vals.get(cat, 0.0)
            pct = int((count / total_skus) * 100)

            row_widget = QWidget()
            row_layout = QVBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(4)

            top_row = QHBoxLayout()
            lbl_name = QLabel(f"<b>{cat}</b>")
            lbl_name.setStyleSheet("color: #f1f5f9; font-size: 13px;")

            lbl_info = QLabel(f"{count} SKUs ({pct}%) • ${val:,.2f}")
            lbl_info.setStyleSheet("color: #94a3b8; font-size: 12px;")

            top_row.addWidget(lbl_name)
            top_row.addStretch()
            top_row.addWidget(lbl_info)
            row_layout.addLayout(top_row)

            prog_bar = QProgressBar()
            prog_bar.setRange(0, 100)
            prog_bar.setValue(pct)
            prog_bar.setTextVisible(False)
            prog_bar.setFixedHeight(8)

            # Palette highlights per category
            bar_color = "#38bdf8"
            if cat == "Motor":
                bar_color = "#38bdf8"
            elif cat == "Sensor":
                bar_color = "#818cf8"
            elif cat == "Controller":
                bar_color = "#a855f7"
            elif cat == "Battery":
                bar_color = "#34d399"
            elif cat == "Converter":
                bar_color = "#f59e0b"
            elif cat == "Generic":
                bar_color = "#94a3b8"

            prog_bar.setStyleSheet(f"""
                QProgressBar {{ background-color: #0f172a; border: none; border-radius: 4px; }}
                QProgressBar::chunk {{ background-color: {bar_color}; border-radius: 4px; }}
            """)
            row_layout.addWidget(prog_bar)

            self.container_cat_meters.addWidget(row_widget)

        # Update Low Stock Alerts Table
        low_items = kpis["low_stock_items"]
        self.table_alerts.setRowCount(len(low_items))

        for row, comp in enumerate(low_items):
            # ID
            item_id = QTableWidgetItem(comp.id)
            item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_alerts.setItem(row, 0, item_id)

            # Name
            item_name = QTableWidgetItem(comp.name)
            self.table_alerts.setItem(row, 1, item_name)

            # Category Badge
            lbl_cat_badge = QLabel(comp.get_type())
            lbl_cat_badge.setStyleSheet(get_badge_stylesheet("category"))
            lbl_cat_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_alerts.setCellWidget(row, 2, lbl_cat_badge)

            # Stock Badge
            stock_badge_type = "out_of_stock" if comp.quantity == 0 else "low_stock"
            lbl_stock = QLabel(f"{comp.quantity} units")
            lbl_stock.setStyleSheet(get_badge_stylesheet(stock_badge_type))
            lbl_stock.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table_alerts.setCellWidget(row, 3, lbl_stock)

            # Restock Button
            btn_restock = QPushButton("+ Restock")
            btn_restock.setProperty("class", "SecondaryButton")
            btn_restock.setStyleSheet("padding: 4px 8px; font-size: 11px;")
            # Capture comp.id with closure
            comp_id = comp.id
            btn_restock.clicked.connect(lambda checked, cid=comp_id: self._quick_restock(cid))
            self.table_alerts.setCellWidget(row, 4, btn_restock)

    def _quick_restock(self, component_id: str):
        comp = self.controller.inventory.find_by_id(component_id)
        if not comp:
            return

        new_qty, ok = QInputDialog.getInt(
            self,
            "Restock Component",
            f"Enter new stock quantity for '{comp.name}' (Current: {comp.quantity}):",
            comp.quantity + 20,
            0,
            1000000,
        )
        if ok:
            self.controller.update_stock(component_id, new_qty)
