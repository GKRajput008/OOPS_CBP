"""
Robotics Project Bill of Materials (BOM) & Cost Estimator Domain Model
Handles itemized allocations, strict stock cap validation, margin/tax calculations, and TXT/Invoice generation.
"""

from typing import List, Optional, Tuple
from datetime import datetime
from .component import Component


class ProjectItem:
    """
    Itemized BOM entry representing an allocated quantity of a specific Component.
    """

    def __init__(self, component: Component, required_quantity: int):
        self.component: Component = component
        self.required_quantity: int = int(required_quantity)

    def get_line_total(self) -> float:
        """Calculates line total cost: unit price * allocated quantity."""
        return self.component.price * self.required_quantity

    def __repr__(self) -> str:
        return f"<ProjectItem {self.component.id}: {self.required_quantity}x @ ${self.component.price:.2f}>"


class RoboticsProject:
    """
    RoboticsProject Cost Estimator & BOM Engine.
    Enforces real-time stock availability bounds, itemized line costs,
    tax/shipping calculations, and formatted invoice export.
    """

    def __init__(
        self,
        name: str = "Autonomous Mobile Robot (AMR-01)",
        tax_rate: float = 0.0825,
        shipping_cost: float = 15.00,
    ):
        self._project_name: str = name
        self._items: List[ProjectItem] = []
        self._tax_rate: float = float(tax_rate)  # e.g., 8.25%
        self._shipping_cost: float = float(shipping_cost)

    @property
    def project_name(self) -> str:
        return self._project_name

    def set_project_name(self, name: str) -> None:
        self._project_name = name.strip() if name and name.strip() else "Unnamed Project"

    @property
    def tax_rate(self) -> float:
        return self._tax_rate

    def set_tax_rate(self, rate: float) -> None:
        self._tax_rate = max(0.0, float(rate))

    @property
    def shipping_cost(self) -> float:
        return self._shipping_cost

    def set_shipping_cost(self, cost: float) -> None:
        self._shipping_cost = max(0.0, float(cost))

    def get_items(self) -> List[ProjectItem]:
        """Returns shallow copy of project items."""
        return list(self._items)

    def get_item_by_id(self, component_id: str) -> Optional[ProjectItem]:
        for item in self._items:
            if item.component.id == component_id:
                return item
        return None

    def add_item(self, component: Optional[Component], required_qty: int) -> Tuple[bool, str]:
        """
        Allocates components to the project BOM with strict stock cap verification.
        If item is already present, increases its allocation up to available inventory stock.
        """
        if component is None:
            return False, "Invalid component pointer."

        if required_qty <= 0:
            return False, f"Allocated quantity must be greater than zero (given: {required_qty})."

        existing_item = self.get_item_by_id(component.id)
        current_alloc = existing_item.required_quantity if existing_item else 0
        new_total_alloc = current_alloc + required_qty

        if new_total_alloc > component.quantity:
            available_remaining = max(0, component.quantity - current_alloc)
            return (
                False,
                f"Stock Cap Exceeded for '{component.name}'. "
                f"Requested total: {new_total_alloc}, Available in Inventory: {component.quantity} "
                f"(Remaining allocatable: {available_remaining}).",
            )

        if existing_item:
            existing_item.required_quantity = new_total_alloc
            return (
                True,
                f"Updated '{component.name}' BOM allocation to {new_total_alloc} units.",
            )
        else:
            self._items.append(ProjectItem(component, required_qty))
            return (
                True,
                f"Added {required_qty}x '{component.name}' ({component.id}) to {self._project_name}.",
            )

    def update_item_quantity(self, component_id: str, new_qty: int) -> Tuple[bool, str]:
        """Updates exact allocation quantity with stock verification."""
        item = self.get_item_by_id(component_id)
        if not item:
            return False, f"Item '{component_id}' not found in current project build."

        if new_qty <= 0:
            return self.remove_item(component_id)

        if new_qty > item.component.quantity:
            return (
                False,
                f"Cannot allocate {new_qty} units. Only {item.component.quantity} available in inventory.",
            )

        item.required_quantity = new_qty
        return True, f"Updated '{item.component.name}' allocation to {new_qty} units."

    def remove_item(self, component_id: str) -> Tuple[bool, str]:
        """Removes an item completely from the project BOM."""
        item = self.get_item_by_id(component_id)
        if not item:
            return False, f"Item with ID '{component_id}' is not in project build."

        self._items.remove(item)
        return True, f"Removed '{item.component.name}' from project BOM."

    def clear(self) -> None:
        """Clears all BOM allocations."""
        self._items.clear()

    def calculate_subtotal(self) -> float:
        """Itemized line totals sum."""
        return sum(item.get_line_total() for item in self._items)

    def calculate_tax(self) -> float:
        """Calculates tax on hardware subtotal."""
        return self.calculate_subtotal() * self._tax_rate

    def calculate_grand_total(self) -> float:
        """Grand total = Subtotal + Tax + Shipping."""
        if not self._items:
            return 0.0
        return self.calculate_subtotal() + self.calculate_tax() + self._shipping_cost

    def get_total_parts_count(self) -> int:
        """Returns total discrete component count across all items."""
        return sum(item.required_quantity for item in self._items)

    def generate_receipt_text(self) -> str:
        """
        Generates formal ASCII invoice / build receipt matching C++ format with enhanced metadata.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subtotal = self.calculate_subtotal()
        tax = self.calculate_tax()
        shipping = self._shipping_cost if self._items else 0.0
        grand_total = self.calculate_grand_total()

        lines = [
            "=======================================================================",
            "             OFFICIAL ROBOTICS BUILD ESTIMATE & RECEIPT                ",
            "=======================================================================",
            f" Project Name : {self._project_name}",
            f" Generated On : {timestamp}",
            f" Total Lines  : {len(self._items)} item types ({self.get_total_parts_count()} total hardware units)",
            "-----------------------------------------------------------------------",
            f"{'Item Name':<30} {'ID':<10} {'Unit ($)':>10} {'Qty':>6} {'Total ($)':>12}",
            "-----------------------------------------------------------------------",
        ]

        if not self._items:
            lines.append("  [No components allocated to this project build]")
        else:
            for item in self._items:
                c = item.component
                name_trunc = c.name if len(c.name) <= 28 else c.name[:25] + "..."
                lines.append(
                    f"{name_trunc:<30} {c.id:<10} {c.price:>10.2f} {item.required_quantity:>6} {item.get_line_total():>12.2f}"
                )

        lines.extend([
            "-----------------------------------------------------------------------",
            f"{'HARDWARE SUBTOTAL:':<48} ${subtotal:>19.2f}",
            f"{'ESTIMATED TAX (' + f'{self._tax_rate*100:.2f}%):':<48} ${tax:>19.2f}",
            f"{'SHIPPING & HANDLING:':<48} ${shipping:>19.2f}",
            "=======================================================================",
            f"{'GRAND TOTAL ESTIMATED COST:':<48} ${grand_total:>19.2f}",
            "=======================================================================",
            " Verification Status: Stock verified against active warehouse inventory.",
            " Terms: Quotation valid for 30 calendar days from issue timestamp.",
            "=======================================================================",
        ])

        return "\n".join(lines)

    def export_receipt_txt(self, filename: str) -> Tuple[bool, str]:
        """Writes the receipt to a TXT file."""
        try:
            content = self.generate_receipt_text()
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content + "\n")
            return True, f"Successfully exported project receipt to '{filename}'."
        except Exception as e:
            return False, f"Failed to export invoice to '{filename}': {str(e)}"
