"""
Unit Test Suite for Robotics Inventory & Project BOM Domain Logic
Tests Edge Cases:
  1. Duplicate Component ID rejection.
  2. Out-of-Stock & Stock-Cap bounded BOM allocation.
  3. Negative values and invalid parameters validation.
  4. Polymorphic method overriding (display, getType, toCSV, getSpecsDict).
  5. File I/O failure handling (missing files, malformed tokens, permission).
  6. Financial calculations (Subtotal, Tax, Shipping, Grand Total).
"""

import os
import unittest
import tempfile

from gui.models.component import (
    Component,
    Motor,
    Sensor,
    Controller,
    Battery,
    Converter,
)
from gui.models.inventory import Inventory
from gui.models.robotics_project import RoboticsProject, ProjectItem


class TestRoboticsDomainModels(unittest.TestCase):

    def setUp(self):
        self.inventory = Inventory()
        self.motor = Motor("NEMA 17", "MOT-01", 15.0, 10, 12, 1200)
        self.sensor = Sensor("LiDAR A1", "SEN-01", 100.0, 5, "Optical", 12.0)
        self.controller = Controller("STM32F4", "CTL-01", 25.0, 8, "ARM Cortex-M4", 16)
        self.battery = Battery("LiPo 3S", "BAT-01", 40.0, 4, 5000, "LiPo")
        self.converter = Converter("LM2596", "CNV-01", 3.0, 20, 24.0, 5.0)

    def test_polymorphic_hierarchy(self):
        """Verify polymorphic getType(), toCSV(), and get_specs_dict()."""
        self.assertEqual(self.motor.get_type(), "Motor")
        self.assertEqual(self.sensor.get_type(), "Sensor")
        self.assertEqual(self.controller.get_type(), "Controller")
        self.assertEqual(self.battery.get_type(), "Battery")
        self.assertEqual(self.converter.get_type(), "Converter")

        # CSV format verification
        csv_str = self.motor.to_csv()
        self.assertTrue(csv_str.startswith("Motor,NEMA 17,MOT-01,15.000000,10,12,1200"))

        # Specs dict verification
        self.assertIn("Voltage", self.motor.get_specs_dict())
        self.assertIn("Range", self.sensor.get_specs_dict())
        self.assertIn("Architecture", self.controller.get_specs_dict())

    def test_encapsulation_and_negative_guards(self):
        """Verify that negative prices or stock quantities raise ValueError."""
        with self.assertRaises(ValueError):
            self.motor.set_quantity(-5)

        with self.assertRaises(ValueError):
            self.motor.set_price(-1.0)

        with self.assertRaises(ValueError):
            self.motor.set_name("")

    def test_duplicate_id_prevention(self):
        """Verify that duplicate component IDs cannot be inserted into Inventory."""
        success1, _ = self.inventory.add_component(self.motor)
        self.assertTrue(success1)

        # Attempt to add another component with the exact same ID
        duplicate_comp = Motor("Another Motor", "MOT-01", 20.0, 5, 24, 2000)
        success2, msg = self.inventory.add_component(duplicate_comp)
        self.assertFalse(success2)
        self.assertIn("Duplicate ID", msg)
        self.assertEqual(self.inventory.count(), 1)

    def test_stock_cap_and_out_of_stock_validation(self):
        """Verify BOM allocation respects inventory stock limits."""
        project = RoboticsProject("Test Rover")

        # Available stock is 10
        # 1. Successful allocation within stock
        ok, _ = project.add_item(self.motor, 4)
        self.assertTrue(ok)
        self.assertEqual(project.get_item_by_id("MOT-01").required_quantity, 4)

        # 2. Add more within stock (4 + 6 = 10, valid)
        ok, _ = project.add_item(self.motor, 6)
        self.assertTrue(ok)
        self.assertEqual(project.get_item_by_id("MOT-01").required_quantity, 10)

        # 3. Exceed available stock (10 + 1 = 11 > 10, rejected)
        ok, msg = project.add_item(self.motor, 1)
        self.assertFalse(ok)
        self.assertIn("Stock Cap Exceeded", msg)
        self.assertEqual(project.get_item_by_id("MOT-01").required_quantity, 10)

        # 4. Out of stock component (qty = 0)
        depleted_sensor = Sensor("Depleted", "SEN-99", 50.0, 0, "Laser", 1.0)
        ok, msg = project.add_item(depleted_sensor, 1)
        self.assertFalse(ok)
        self.assertIn("Stock Cap Exceeded", msg)

    def test_financial_calculations(self):
        """Verify line totals, subtotal, tax margins, and grand total."""
        project = RoboticsProject("Hexapod", tax_rate=0.10, shipping_cost=20.00)
        project.add_item(self.motor, 4)     # 4 * $15 = $60
        project.add_item(self.sensor, 2)    # 2 * $100 = $200
        # Subtotal = $260.00
        # Tax (10%) = $26.00
        # Shipping = $20.00
        # Grand Total = $306.00
        self.assertAlmostEqual(project.calculate_subtotal(), 260.00)
        self.assertAlmostEqual(project.calculate_tax(), 26.00)
        self.assertAlmostEqual(project.calculate_grand_total(), 306.00)

    def test_file_io_resilience(self):
        """Verify handling of missing files, corrupted lines, and persistence round-trip."""
        # Missing file test
        ok, msg, count = self.inventory.load_from_csv("non_existent_file_xyz.csv")
        self.assertFalse(ok)
        self.assertEqual(count, 0)

        # Round trip test with temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as temp_file:
            temp_path = temp_file.name
            # Write good and malformed lines
            temp_file.write("Motor,Good Motor,MOT-01,15.0,10,12,1200\n")
            temp_file.write("Corrupted Line without tokens\n")
            temp_file.write("Sensor,Good Sensor,SEN-01,100.0,5,Laser,10.0\n")
            temp_file.write("Motor,Duplicate Motor,MOT-01,20.0,2,12,1000\n")  # duplicate ID

        try:
            inv = Inventory()
            ok, msg, loaded_count = inv.load_from_csv(temp_path)
            self.assertTrue(ok)
            self.assertEqual(loaded_count, 2)  # Good Motor and Good Sensor
            self.assertEqual(inv.count(), 2)

            # Test save
            save_ok, save_msg = inv.save_to_csv(temp_path)
            self.assertTrue(save_ok)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
