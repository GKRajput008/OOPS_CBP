"""
Application Controller (Model-View-Presenter / MVC Coordination)
Decouples domain models from presentation layer and manages business logic, signals, and validation.
"""

from typing import Dict, Any, List, Optional, Tuple
from PyQt6.QtCore import QObject, pyqtSignal

from gui.models.component import Component
from gui.models.inventory import Inventory
from gui.models.robotics_project import RoboticsProject, ProjectItem


class AppController(QObject):
    """
    Central Controller orchestrating state transitions between the Inventory model,
    the RoboticsProject BOM model, and Qt views.
    """

    # Qt Signals for event-driven reactive UI updates
    inventory_changed = pyqtSignal()
    bom_changed = pyqtSignal()
    status_notification = pyqtSignal(str, bool)  # message, is_error

    def __init__(self, default_csv_path: str = "inventory.csv"):
        super().__init__()
        self.inventory: Inventory = Inventory()
        self.project: RoboticsProject = RoboticsProject("Autonomous Mobile Robot (AMR-01)")
        self.current_csv_path: str = default_csv_path

        # Initial load if file exists
        self.load_inventory_csv(self.current_csv_path)

    # -------------------------------------------------------------
    # Inventory Domain Operations
    # -------------------------------------------------------------
    def add_component(self, component: Component) -> Tuple[bool, str]:
        """Adds component to inventory model and emits update signals."""
        success, msg = self.inventory.add_component(component)
        if success:
            self.inventory_changed.emit()
            self.status_notification.emit(msg, False)
        else:
            self.status_notification.emit(msg, True)
        return success, msg

    def update_stock(self, component_id: str, new_quantity: int) -> Tuple[bool, str]:
        """Updates component stock level and synchronizes views."""
        success, msg = self.inventory.update_quantity(component_id, new_quantity)
        if success:
            self.inventory_changed.emit()
            # If item is in project BOM and new_quantity is now lower than BOM alloc, alert
            bom_item = self.project.get_item_by_id(component_id)
            if bom_item and new_quantity < bom_item.required_quantity:
                self.project.update_item_quantity(component_id, new_quantity)
                self.bom_changed.emit()
            self.status_notification.emit(msg, False)
        else:
            self.status_notification.emit(msg, True)
        return success, msg

    def remove_component(self, component_id: str) -> Tuple[bool, str]:
        """Removes component from inventory and removes any allocation in BOM."""
        # Check if in project
        if self.project.get_item_by_id(component_id):
            self.project.remove_item(component_id)
            self.bom_changed.emit()

        success, msg = self.inventory.remove_component(component_id)
        if success:
            self.inventory_changed.emit()
            self.status_notification.emit(msg, False)
        else:
            self.status_notification.emit(msg, True)
        return success, msg

    def load_inventory_csv(self, filepath: str) -> Tuple[bool, str]:
        """Loads inventory data from CSV file."""
        success, msg, count = self.inventory.load_from_csv(filepath)
        if success:
            self.current_csv_path = filepath
            self.inventory_changed.emit()
            self.status_notification.emit(msg, False)
        else:
            self.status_notification.emit(msg, True)
        return success, msg

    def save_inventory_csv(self, filepath: Optional[str] = None) -> Tuple[bool, str]:
        """Saves current inventory state to CSV."""
        target_path = filepath if filepath else self.current_csv_path
        success, msg = self.inventory.save_to_csv(target_path)
        if success:
            self.current_csv_path = target_path
            self.status_notification.emit(msg, False)
        else:
            self.status_notification.emit(msg, True)
        return success, msg

    # -------------------------------------------------------------
    # Robotics Project BOM Operations
    # -------------------------------------------------------------
    def add_to_bom(self, component_id: str, quantity: int) -> Tuple[bool, str]:
        """Allocates specified quantity of an inventory component to project BOM."""
        comp = self.inventory.find_by_id(component_id)
        if not comp:
            msg = f"Component '{component_id}' not found in inventory."
            self.status_notification.emit(msg, True)
            return False, msg

        success, msg = self.project.add_item(comp, quantity)
        if success:
            self.bom_changed.emit()
            self.status_notification.emit(msg, False)
        else:
            self.status_notification.emit(msg, True)
        return success, msg

    def update_bom_quantity(self, component_id: str, new_quantity: int) -> Tuple[bool, str]:
        """Modifies allocation quantity in BOM."""
        success, msg = self.project.update_item_quantity(component_id, new_quantity)
        if success:
            self.bom_changed.emit()
            self.status_notification.emit(msg, False)
        else:
            self.status_notification.emit(msg, True)
        return success, msg

    def remove_from_bom(self, component_id: str) -> Tuple[bool, str]:
        """Removes component from BOM."""
        success, msg = self.project.remove_item(component_id)
        if success:
            self.bom_changed.emit()
            self.status_notification.emit(msg, False)
        else:
            self.status_notification.emit(msg, True)
        return success, msg

    def clear_bom(self) -> None:
        """Empties BOM."""
        self.project.clear()
        self.bom_changed.emit()
        self.status_notification.emit("Project BOM cleared.", False)

    def set_project_config(self, name: str, tax_rate: float, shipping: float) -> None:
        """Updates project metadata and parameters."""
        self.project.set_project_name(name)
        self.project.set_tax_rate(tax_rate)
        self.project.set_shipping_cost(shipping)
        self.bom_changed.emit()

    def export_project_receipt(self, filepath: str) -> Tuple[bool, str]:
        """Exports formal quotation/receipt to disk."""
        success, msg = self.project.export_receipt_txt(filepath)
        if success:
            self.status_notification.emit(msg, False)
        else:
            self.status_notification.emit(msg, True)
        return success, msg

    # -------------------------------------------------------------
    # State Inspection & Metric Accessors
    # -------------------------------------------------------------
    def get_dashboard_kpis(self) -> Dict[str, Any]:
        """Aggregates real-time KPIs for Dashboard widgets."""
        components = self.inventory.get_all_components()
        total_valuation = self.inventory.calculate_total_inventory_value()
        unique_count = len(components)
        total_units = sum(c.quantity for c in components)
        low_stock_items = self.inventory.get_low_stock_items(threshold=10)
        category_counts = self.inventory.get_category_counts()
        category_valuations = self.inventory.get_category_valuations()

        return {
            "total_valuation": total_valuation,
            "unique_count": unique_count,
            "total_units": total_units,
            "low_stock_count": len(low_stock_items),
            "low_stock_items": low_stock_items,
            "category_counts": category_counts,
            "category_valuations": category_valuations,
        }

    def get_filtered_inventory(
        self, search_text: str = "", category_filter: str = "All"
    ) -> List[Component]:
        """Returns filtered inventory slice."""
        return self.inventory.filter_components(search_text, category_filter)

    def get_bom_details(self) -> Dict[str, Any]:
        """Returns itemized BOM items and financial breakdown."""
        return {
            "project_name": self.project.project_name,
            "items": self.project.get_items(),
            "subtotal": self.project.calculate_subtotal(),
            "tax_rate": self.project.tax_rate,
            "tax": self.project.calculate_tax(),
            "shipping": self.project.shipping_cost,
            "grand_total": self.project.calculate_grand_total(),
            "parts_count": self.project.get_total_parts_count(),
        }
