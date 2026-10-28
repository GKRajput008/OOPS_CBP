"""
Modern Dark Slate & Cyan Design System for Phase 4 Desktop GUI.
Provides comprehensive QSS stylesheets, palette tokens, and styling helpers.
"""

DARK_STYLESHEET = """
/* ====================================================================
   GLOBAL APPLICATION STYLES
   ==================================================================== */
QMainWindow, QDialog {
    background-color: #0b0f19;
    color: #f1f5f9;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    font-size: 13px;
}

QWidget {
    color: #e2e8f0;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    outline: none;
}

/* ====================================================================
   TAB WIDGET & NAVIGATION BAR
   ==================================================================== */
QTabWidget::pane {
    border: 1px solid #1e293b;
    background-color: #0f172a;
    border-radius: 8px;
    top: -1px;
}

QTabBar::tab {
    background-color: #1e293b;
    color: #94a3b8;
    padding: 10px 24px;
    font-weight: 600;
    font-size: 13px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 4px;
    border: 1px solid #334155;
    border-bottom: none;
    min-width: 140px;
}

QTabBar::tab:hover {
    background-color: #273549;
    color: #38bdf8;
}

QTabBar::tab:selected {
    background-color: #0f172a;
    color: #38bdf8;
    border: 1px solid #38bdf8;
    border-bottom: 2px solid #0f172a;
}

/* ====================================================================
   CARD CONTAINERS & PANELS
   ==================================================================== */
QFrame.CardWidget {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 16px;
}

QFrame.KPICard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e293b, stop:1 #172033);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 18px;
}

QFrame.KPICard:hover {
    border: 1px solid #38bdf8;
}

/* ====================================================================
   TABLES & LISTS
   ==================================================================== */
QTableWidget, QTableView {
    background-color: #131c2e;
    alternate-background-color: #172238;
    border: 1px solid #334155;
    border-radius: 8px;
    gridline-color: #1e293b;
    color: #f1f5f9;
    selection-background-color: #0284c7;
    selection-color: #ffffff;
    font-size: 13px;
}

QTableWidget::item {
    padding: 8px 10px;
    border-bottom: 1px solid #1e293b;
}

QTableWidget::item:hover {
    background-color: #1e2e4a;
}

QHeaderView::section {
    background-color: #1e293b;
    color: #94a3b8;
    font-weight: 700;
    font-size: 12px;
    text-transform: uppercase;
    padding: 10px 8px;
    border: none;
    border-right: 1px solid #334155;
    border-bottom: 2px solid #38bdf8;
}

QHeaderView::section:last {
    border-right: none;
}

/* ====================================================================
   BUTTONS
   ==================================================================== */
QPushButton {
    background-color: #2563eb;
    color: #ffffff;
    font-weight: 600;
    font-size: 13px;
    padding: 9px 18px;
    border-radius: 6px;
    border: 1px solid #3b82f6;
}

QPushButton:hover {
    background-color: #1d4ed8;
    border: 1px solid #60a5fa;
}

QPushButton:pressed {
    background-color: #1e40af;
}

QPushButton:disabled {
    background-color: #334155;
    color: #64748b;
    border: 1px solid #475569;
}

QPushButton.SecondaryButton {
    background-color: #334155;
    color: #e2e8f0;
    border: 1px solid #475569;
}

QPushButton.SecondaryButton:hover {
    background-color: #475569;
    border: 1px solid #64748b;
    color: #ffffff;
}

QPushButton.SuccessButton {
    background-color: #059669;
    color: #ffffff;
    border: 1px solid #10b981;
}

QPushButton.SuccessButton:hover {
    background-color: #047857;
    border: 1px solid #34d399;
}

QPushButton.DangerButton {
    background-color: #be123c;
    color: #ffffff;
    border: 1px solid #e11d48;
}

QPushButton.DangerButton:hover {
    background-color: #9f1239;
    border: 1px solid #f43f5e;
}

/* ====================================================================
   INPUT CONTROLS (QLineEdit, QComboBox, QSpinBox)
   ==================================================================== */
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {
    background-color: #0f172a;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
    selection-background-color: #38bdf8;
    selection-color: #0f172a;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus {
    border: 1px solid #38bdf8;
    background-color: #131d33;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border-left: 1px solid #334155;
}

QComboBox QAbstractItemView {
    background-color: #1e293b;
    border: 1px solid #38bdf8;
    color: #f1f5f9;
    selection-background-color: #0284c7;
    selection-color: #ffffff;
    padding: 4px;
}

/* ====================================================================
   PROGRESS BARS & METERS
   ==================================================================== */
QProgressBar {
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 5px;
    text-align: center;
    color: #f8fafc;
    font-size: 11px;
    font-weight: bold;
    height: 18px;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #38bdf8);
    border-radius: 4px;
}

/* ====================================================================
   SCROLL BARS
   ==================================================================== */
QScrollBar:vertical {
    border: none;
    background: #0f172a;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: #334155;
    min-height: 25px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #475569;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}

QScrollBar:horizontal {
    border: none;
    background: #0f172a;
    height: 10px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background: #334155;
    min-width: 25px;
    border-radius: 5px;
}

/* ====================================================================
   STATUS BAR
   ==================================================================== */
QStatusBar {
    background-color: #0b0f19;
    color: #94a3b8;
    border-top: 1px solid #1e293b;
    font-size: 12px;
}
"""


def get_badge_stylesheet(status_type: str) -> str:
    """Returns CSS badge for table stock status."""
    if status_type == "in_stock":
        return "background-color: #064e3b; color: #34d399; border: 1px solid #059669; border-radius: 4px; padding: 3px 8px; font-weight: 600;"
    elif status_type == "low_stock":
        return "background-color: #451a03; color: #fbbf24; border: 1px solid #d97706; border-radius: 4px; padding: 3px 8px; font-weight: 600;"
    elif status_type == "out_of_stock":
        return "background-color: #4c0519; color: #fb7185; border: 1px solid #e11d48; border-radius: 4px; padding: 3px 8px; font-weight: 600;"
    elif status_type == "category":
        return "background-color: #1e293b; color: #38bdf8; border: 1px solid #0284c7; border-radius: 4px; padding: 2px 6px; font-weight: 600;"
    return ""
