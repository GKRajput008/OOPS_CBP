"""
Inventory Management Domain Model
Maintains hardware component catalog with duplicate detection, aggregation, search, and CSV persistence.
"""

import os
from typing import List, Optional, Dict, Tuple
from .component import Component, Motor, Sensor, Controller, Battery, Converter


class Inventory:
    """
    Inventory aggregate class maintaining a collection of Component pointers/references.
    Mirrors the C++ Inventory class while adding high-performance filtering and analytics for the GUI.
    """

    def __init__(self):
        self._components: List[Component] = []

    def get_all_components(self) -> List[Component]:
        """Returns a copy of all managed components."""
        return list(self._components)

    def count(self) -> int:
        """Returns total unique components count."""
        return len(self._components)

    def add_component(self, component: Optional[Component]) -> Tuple[bool, str]:
        """
        Adds a new component to inventory after enforcing uniqueness constraints.
        Returns: (success: bool, message: str)
        """
        if component is None:
            return False, "Null component pointer provided."

        if not component.id:
            return False, "Component ID cannot be empty."

        if self.find_by_id(component.id) is not None:
            return False, f"Duplicate ID: Component with ID '{component.id}' already exists."

        self._components.append(component)
        return True, f"Component '{component.name}' ({component.id}) added successfully."

    def find_by_id(self, component_id: str) -> Optional[Component]:
        """Performs exact match lookup by Component ID."""
        target_id = str(component_id).strip()
        for comp in self._components:
            if comp.id == target_id:
                return comp
        return None

    def find_by_name(self, name: str) -> Optional[Component]:
        """Performs case-insensitive lookup by Component Name."""
        target_name = str(name).strip().lower()
        for comp in self._components:
            if comp.name.lower() == target_name:
                return comp
        return None

    def update_quantity(self, component_id: str, new_quantity: int) -> Tuple[bool, str]:
        """
        Updates available stock quantity for an item with non-negative validation.
        """
        if new_quantity < 0:
            return False, f"Invalid stock quantity {new_quantity}. Quantity cannot be negative."

        comp = self.find_by_id(component_id)
        if comp is None:
            return False, f"Component with ID '{component_id}' not found."

        old_qty = comp.quantity
        comp.set_quantity(new_quantity)
        return True, f"Stock updated for {comp.name} ({comp.id}): {old_qty} -> {new_quantity} units."

    def remove_component(self, component_id: str) -> Tuple[bool, str]:
        """Removes a component by ID from inventory."""
        comp = self.find_by_id(component_id)
        if comp is None:
            return False, f"Component with ID '{component_id}' not found in inventory."

        self._components.remove(comp)
        return True, f"Component '{comp.name}' (ID: {comp.id}) removed from inventory."

    def calculate_total_inventory_value(self) -> float:
        """Aggregates total asset valuation across all in-stock hardware."""
        return sum(comp.get_total_value() for comp in self._components)

    def get_category_counts(self) -> Dict[str, int]:
        """Returns distribution count of components by category."""
        counts: Dict[str, int] = {
            "Motor": 0,
            "Sensor": 0,
            "Controller": 0,
            "Battery": 0,
            "Converter": 0,
            "Generic": 0,
        }
        for comp in self._components:
            cat = comp.get_type()
            counts[cat] = counts.get(cat, 0) + 1
        return counts

    def get_category_valuations(self) -> Dict[str, float]:
        """Returns valuation breakdown ($) by hardware category."""
        valuations: Dict[str, float] = {
            "Motor": 0.0,
            "Sensor": 0.0,
            "Controller": 0.0,
            "Battery": 0.0,
            "Converter": 0.0,
            "Generic": 0.0,
        }
        for comp in self._components:
            cat = comp.get_type()
            valuations[cat] = valuations.get(cat, 0.0) + comp.get_total_value()
        return valuations

    def get_low_stock_items(self, threshold: int = 10) -> List[Component]:
        """Returns items where available quantity is at or below critical threshold."""
        return [c for c in self._components if c.quantity <= threshold]

    def filter_components(
        self, search_text: str = "", category_filter: str = "All"
    ) -> List[Component]:
        """
        Multicriteria live filter matching ID, Name, or Specs across optional category slice.
        """
        query = search_text.strip().lower()
        results: List[Component] = []

        for comp in self._components:
            # Check Category filter
            if category_filter != "All" and comp.get_type() != category_filter:
                continue

            # Check query string in ID, Name, Category, or Specs
            if not query:
                results.append(comp)
            else:
                match_id = query in comp.id.lower()
                match_name = query in comp.name.lower()
                match_cat = query in comp.get_type().lower()
                match_specs = query in comp.get_specs_summary().lower()
                if match_id or match_name or match_cat or match_specs:
                    results.append(comp)

        return results

    def save_to_csv(self, filename: str) -> Tuple[bool, str]:
        """
        Serializes entire inventory state to CSV matching the C++ backend format.
        """
        try:
            with open(filename, "w", encoding="utf-8") as f:
                for comp in self._components:
                    f.write(comp.to_csv() + "\n")
            return True, f"Successfully saved {len(self._components)} components to '{filename}'."
        except Exception as e:
            return False, f"Failed to save CSV to '{filename}': {str(e)}"

    def load_from_csv(self, filename: str, clear_existing: bool = True) -> Tuple[bool, str, int]:
        """
        Parses CSV and dynamically reconstructs polymorphic Component objects.
        Handles edge cases such as missing files, malformed rows, and duplicate IDs.
        Returns: (success: bool, message: str, loaded_count: int)
        """
        if not os.path.exists(filename):
            return False, f"File not found: '{filename}'", 0

        if clear_existing:
            self._components.clear()

        loaded_count = 0
        error_lines = 0

        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, start=1):
                    line = line.strip()
                    if not line:
                        continue

                    tokens = [t.strip() for t in line.split(",")]
                    if len(tokens) < 5:
                        error_lines += 1
                        continue

                    comp_type = tokens[0]
                    name = tokens[1]
                    cid = tokens[2]

                    try:
                        price = float(tokens[3])
                        quantity = int(tokens[4])
                    except ValueError:
                        error_lines += 1
                        continue

                    comp: Optional[Component] = None

                    try:
                        if comp_type == "Generic":
                            comp = Component(name, cid, price, quantity)
                        elif comp_type == "Motor" and len(tokens) >= 7:
                            comp = Motor(name, cid, price, quantity, int(tokens[5]), int(tokens[6]))
                        elif comp_type == "Sensor" and len(tokens) >= 7:
                            comp = Sensor(name, cid, price, quantity, tokens[5], float(tokens[6]))
                        elif comp_type == "Controller" and len(tokens) >= 7:
                            comp = Controller(name, cid, price, quantity, tokens[5], int(tokens[6]))
                        elif comp_type == "Battery" and len(tokens) >= 7:
                            comp = Battery(name, cid, price, quantity, int(tokens[5]), tokens[6])
                        elif comp_type == "Converter" and len(tokens) >= 7:
                            comp = Converter(name, cid, price, quantity, float(tokens[5]), float(tokens[6]))
                        else:
                            # Fallback to Generic if extra tokens are missing
                            comp = Component(name, cid, price, quantity)
                    except Exception:
                        error_lines += 1
                        continue

                    if comp:
                        success, _ = self.add_component(comp)
                        if success:
                            loaded_count += 1
                        else:
                            error_lines += 1

            msg = f"Loaded {loaded_count} components from '{filename}'."
            if error_lines > 0:
                msg += f" (Skipped {error_lines} invalid/duplicate entries)"
            return True, msg, loaded_count

        except Exception as e:
            return False, f"Error reading '{filename}': {str(e)}", loaded_count
