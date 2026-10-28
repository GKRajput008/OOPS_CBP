"""
Dynamic Modal Dialog for Adding Components with Polymorphic Parameter Binding.
"""

from typing import Optional
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QStackedWidget,
    QWidget,
    QMessageBox,
    QFrame,
)
from PyQt6.QtCore import Qt

from gui.models.component import (
    Component,
    Motor,
    Sensor,
    Controller,
    Battery,
    Converter,
)
from gui.controllers.app_controller import AppController


class AddComponentDialog(QDialog):
    """
    Modal dialog that dynamically reconfigures input fields based on the
    selected hardware component category.
    """

    def __init__(self, controller: AppController, parent=None):
        super().__init__(parent)
        self.controller: AppController = controller
        self.created_component: Optional[Component] = None

        self.setWindowTitle("Add New Robotics Hardware Component")
        self.setMinimumWidth(500)
        self.setModal(True)
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # Header Title
        title_label = QLabel("Component Specification Registry")
        title_label.setStyleSheet("font-size: 18px; font-weight: 700; color: #38bdf8;")
        subtitle = QLabel("Select hardware classification and specify physical parameters.")
        subtitle.setStyleSheet("color: #94a3b8; font-size: 12px; margin-bottom: 8px;")
        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle)

        # Base Attributes Card
        base_frame = QFrame()
        base_frame.setProperty("class", "CardWidget")
        base_layout = QFormLayout(base_frame)
        base_layout.setSpacing(12)

        # Category Selector
        self.combo_category = QComboBox()
        self.combo_category.addItems([
            "Motor",
            "Sensor",
            "Controller",
            "Battery",
            "Converter",
            "Generic",
        ])
        self.combo_category.currentTextChanged.connect(self._on_category_changed)
        base_layout.addRow("Category:", self.combo_category)

        # Name
        self.edit_name = QLineEdit()
        self.edit_name.setPlaceholderText("e.g. NEMA 17 High Torque Stepper")
        base_layout.addRow("Hardware Name *:", self.edit_name)

        # Component ID
        self.edit_id = QLineEdit()
        self.edit_id.setPlaceholderText("e.g. MOT-004")
        base_layout.addRow("Component ID *:", self.edit_id)

        # Unit Price
        self.spin_price = QDoubleSpinBox()
        self.spin_price.setRange(0.01, 99999.99)
        self.spin_price.setValue(19.99)
        self.spin_price.setPrefix("$ ")
        self.spin_price.setDecimals(2)
        base_layout.addRow("Unit Price ($):", self.spin_price)

        # Quantity
        self.spin_quantity = QSpinBox()
        self.spin_quantity.setRange(0, 1000000)
        self.spin_quantity.setValue(10)
        base_layout.addRow("Initial Stock:", self.spin_quantity)

        main_layout.addWidget(base_frame)

        # Category-Specific Attributes Stacked Widget
        self.stacked_specs = QStackedWidget()

        # Page 0: Motor Specs
        page_motor = QWidget()
        layout_motor = QFormLayout(page_motor)
        self.spin_motor_voltage = QSpinBox()
        self.spin_motor_voltage.setRange(1, 240)
        self.spin_motor_voltage.setValue(12)
        self.spin_motor_voltage.setSuffix(" V")
        self.spin_motor_rpm = QSpinBox()
        self.spin_motor_rpm.setRange(1, 100000)
        self.spin_motor_rpm.setValue(3000)
        self.spin_motor_rpm.setSuffix(" RPM")
        layout_motor.addRow("Operating Voltage:", self.spin_motor_voltage)
        layout_motor.addRow("Max Velocity (RPM):", self.spin_motor_rpm)
        self.stacked_specs.addWidget(page_motor)

        # Page 1: Sensor Specs
        page_sensor = QWidget()
        layout_sensor = QFormLayout(page_sensor)
        self.combo_sensor_type = QComboBox()
        self.combo_sensor_type.setEditable(True)
        self.combo_sensor_type.addItems([
            "Optical/Laser",
            "Ultrasonic",
            "Inertial (IMU)",
            "Infrared",
            "Tactile / Force",
            "Environmental",
        ])
        self.spin_sensor_range = QDoubleSpinBox()
        self.spin_sensor_range.setRange(0.01, 500.0)
        self.spin_sensor_range.setValue(4.0)
        self.spin_sensor_range.setSuffix(" m")
        layout_sensor.addRow("Transducer Category:", self.combo_sensor_type)
        layout_sensor.addRow("Operational Range:", self.spin_sensor_range)
        self.stacked_specs.addWidget(page_sensor)

        # Page 2: Controller Specs
        page_controller = QWidget()
        layout_controller = QFormLayout(page_controller)
        self.combo_controller_arch = QComboBox()
        self.combo_controller_arch.setEditable(True)
        self.combo_controller_arch.addItems([
            "ARM Cortex-M4",
            "ARM Cortex-A72",
            "AVR RISC",
            "ESP32 Xtensa Dual-Core",
            "RISC-V 64-bit",
            "FPGA Xilinx Artix-7",
        ])
        self.spin_controller_ports = QSpinBox()
        self.spin_controller_ports.setRange(1, 256)
        self.spin_controller_ports.setValue(16)
        self.spin_controller_ports.setSuffix(" GPIO Ports")
        layout_controller.addRow("Microarchitecture:", self.combo_controller_arch)
        layout_controller.addRow("I/O Port Channels:", self.spin_controller_ports)
        self.stacked_specs.addWidget(page_controller)

        # Page 3: Battery Specs
        page_battery = QWidget()
        layout_battery = QFormLayout(page_battery)
        self.spin_battery_cap = QSpinBox()
        self.spin_battery_cap.setRange(10, 500000)
        self.spin_battery_cap.setValue(5000)
        self.spin_battery_cap.setSuffix(" mAh")
        self.combo_battery_chem = QComboBox()
        self.combo_battery_chem.addItems(["LiPo", "Li-Ion", "LiFePO4", "NiMH", "SLA"])
        layout_battery.addRow("Charge Capacity:", self.spin_battery_cap)
        layout_battery.addRow("Cell Chemistry:", self.combo_battery_chem)
        self.stacked_specs.addWidget(page_battery)

        # Page 4: Converter Specs
        page_converter = QWidget()
        layout_converter = QFormLayout(page_converter)
        self.spin_converter_vin = QDoubleSpinBox()
        self.spin_converter_vin.setRange(0.5, 500.0)
        self.spin_converter_vin.setValue(24.0)
        self.spin_converter_vin.setSuffix(" V")
        self.spin_converter_vout = QDoubleSpinBox()
        self.spin_converter_vout.setRange(0.5, 500.0)
        self.spin_converter_vout.setValue(5.0)
        self.spin_converter_vout.setSuffix(" V")
        layout_converter.addRow("Input Rating (Vin):", self.spin_converter_vin)
        layout_converter.addRow("Output Regulated (Vout):", self.spin_converter_vout)
        self.stacked_specs.addWidget(page_converter)

        # Page 5: Generic Specs
        page_generic = QWidget()
        layout_generic = QVBoxLayout(page_generic)
        lbl_generic = QLabel("Standard mechanical / electrical hardware (No category-specific parameters required).")
        lbl_generic.setStyleSheet("color: #94a3b8; font-style: italic;")
        layout_generic.addWidget(lbl_generic)
        self.stacked_specs.addWidget(page_generic)

        specs_card = QFrame()
        specs_card.setProperty("class", "CardWidget")
        specs_card_layout = QVBoxLayout(specs_card)
        specs_title = QLabel("Specialized Hardware Parameters")
        specs_title.setStyleSheet("font-weight: 600; color: #38bdf8; font-size: 13px;")
        specs_card_layout.addWidget(specs_title)
        specs_card_layout.addWidget(self.stacked_specs)
        main_layout.addWidget(specs_card)

        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setProperty("class", "SecondaryButton")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)

        btn_save = QPushButton("Register Component")
        btn_save.setProperty("class", "SuccessButton")
        btn_save.clicked.connect(self._validate_and_save)
        btn_layout.addWidget(btn_save)

        main_layout.addLayout(btn_layout)

    def _on_category_changed(self, text: str):
        mapping = {
            "Motor": 0,
            "Sensor": 1,
            "Controller": 2,
            "Battery": 3,
            "Converter": 4,
            "Generic": 5,
        }
        self.stacked_specs.setCurrentIndex(mapping.get(text, 5))

    def _validate_and_save(self):
        name = self.edit_name.text().strip()
        cid = self.edit_id.text().strip().upper()
        price = self.spin_price.value()
        qty = self.spin_quantity.value()
        category = self.combo_category.currentText()

        # Validation Checks
        if not name:
            QMessageBox.warning(self, "Validation Error", "Component Name cannot be empty.")
            self.edit_name.setFocus()
            return

        if not cid:
            QMessageBox.warning(self, "Validation Error", "Component ID cannot be empty.")
            self.edit_id.setFocus()
            return

        # Check for duplicate ID in existing inventory
        if self.controller.inventory.find_by_id(cid) is not None:
            QMessageBox.critical(
                self,
                "Duplicate ID Conflict",
                f"A component with ID '{cid}' already exists in inventory.\nPlease assign a unique hardware identifier.",
            )
            self.edit_id.setFocus()
            return

        # Construct derived polymorphic object
        try:
            if category == "Motor":
                v = self.spin_motor_voltage.value()
                rpm = self.spin_motor_rpm.value()
                self.created_component = Motor(name, cid, price, qty, v, rpm)
            elif category == "Sensor":
                stype = self.combo_sensor_type.currentText().strip()
                rng = self.spin_sensor_range.value()
                self.created_component = Sensor(name, cid, price, qty, stype, rng)
            elif category == "Controller":
                arch = self.combo_controller_arch.currentText().strip()
                ports = self.spin_controller_ports.value()
                self.created_component = Controller(name, cid, price, qty, arch, ports)
            elif category == "Battery":
                cap = self.spin_battery_cap.value()
                chem = self.combo_battery_chem.currentText().strip()
                self.created_component = Battery(name, cid, price, qty, cap, chem)
            elif category == "Converter":
                vin = self.spin_converter_vin.value()
                vout = self.spin_converter_vout.value()
                self.created_component = Converter(name, cid, price, qty, vin, vout)
            else:
                self.created_component = Component(name, cid, price, qty)

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Instantiation Error", f"Failed to instantiate component: {str(e)}")
