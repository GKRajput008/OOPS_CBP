"""
Robotics Hardware Component Domain Models (OOP Hierarchy)
Implements Base Component, Derived Specializations, Polymorphic Methods, and Data Contracts.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class Component:
    """
    Abstract Base Class for hardware inventory components.
    Demonstrates:
      - Encapsulation: private attributes with controlled accessors/mutators.
      - Abstraction & Polymorphism: virtual display(), getType(), toCSV(), and getSpecsDict().
    """

    def __init__(self, name: str, component_id: str, price: float, quantity: int):
        self._name: str = str(name).strip()
        self._id: str = str(component_id).strip()
        self._price: float = max(0.0, float(price))
        self._quantity: int = max(0, int(quantity))

    # Accessors (Getters)
    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> str:
        return self._id

    @property
    def price(self) -> float:
        return self._price

    @property
    def quantity(self) -> int:
        return self._quantity

    # Mutators (Setters)
    def set_quantity(self, q: int) -> None:
        if q < 0:
            raise ValueError(f"Quantity cannot be negative (attempted: {q})")
        self._quantity = int(q)

    def set_price(self, p: float) -> None:
        if p < 0.0:
            raise ValueError(f"Price cannot be negative (attempted: {p})")
        self._price = float(p)

    def set_name(self, name: str) -> None:
        if not name or not name.strip():
            raise ValueError("Component name cannot be empty")
        self._name = name.strip()

    def get_total_value(self) -> float:
        """Computes current asset valuation: unit price * in-stock quantity."""
        return self._price * self._quantity

    def get_type(self) -> str:
        """Polymorphic category identifier."""
        return "Generic"

    def display(self) -> str:
        """Polymorphic formatted string representation matching C++ backend display()."""
        return (
            f"Type: {self.get_type()} | Name: {self._name} | ID: {self._id} "
            f"| Price: ${self._price:.2f} | Stock: {self._quantity} "
            f"| Total: ${self.get_total_value():.2f}"
        )

    def to_csv(self) -> str:
        """Polymorphic serialization compatible with C++ backend CSV parser."""
        return f"{self.get_type()},{self._name},{self._id},{self._price:.6f},{self._quantity}"

    def get_specs_dict(self) -> Dict[str, str]:
        """Returns structured dictionary of specialized specs for GUI table display."""
        return {"Base Type": "Mechanical / Structure / Generic"}

    def get_specs_summary(self) -> str:
        """One-line string summary of specialized hardware parameters."""
        specs = self.get_specs_dict()
        return " | ".join(f"{k}: {v}" for k, v in specs.items())

    def __repr__(self) -> str:
        return f"<{self.get_type()} id={self._id} name='{self._name}'>"


class Motor(Component):
    """
    Derived hardware class: Motor (DC, Stepper, Servo, Brushless).
    Specialized Attributes: Operating Voltage (V), Max RPM.
    """

    def __init__(
        self,
        name: str,
        component_id: str,
        price: float,
        quantity: int,
        operating_voltage: int,
        rpm: int,
    ):
        super().__init__(name, component_id, price, quantity)
        self._operating_voltage: int = int(operating_voltage)
        self._rpm: int = int(rpm)

    @property
    def operating_voltage(self) -> int:
        return self._operating_voltage

    @property
    def rpm(self) -> int:
        return self._rpm

    def get_type(self) -> str:
        return "Motor"

    def display(self) -> str:
        base_str = super().display()
        return f"{base_str}\n  [Specs] Voltage: {self._operating_voltage}V | Max RPM: {self._rpm}"

    def to_csv(self) -> str:
        return f"{super().to_csv()},{self._operating_voltage},{self._rpm}"

    def get_specs_dict(self) -> Dict[str, str]:
        return {
            "Voltage": f"{self._operating_voltage} V",
            "Max RPM": f"{self._rpm} RPM",
        }


class Sensor(Component):
    """
    Derived hardware class: Sensor (Ultrasonic, LiDAR, IMU, Optical, etc.).
    Specialized Attributes: Sensor Category, Detection Range (meters).
    """

    def __init__(
        self,
        name: str,
        component_id: str,
        price: float,
        quantity: int,
        sensor_type: str,
        range_m: float,
    ):
        super().__init__(name, component_id, price, quantity)
        self._sensor_type: str = str(sensor_type).strip()
        self._range_m: float = float(range_m)

    @property
    def sensor_type(self) -> str:
        return self._sensor_type

    @property
    def range_m(self) -> float:
        return self._range_m

    def get_type(self) -> str:
        return "Sensor"

    def display(self) -> str:
        base_str = super().display()
        return f"{base_str}\n  [Specs] Category: {self._sensor_type} | Range: {self._range_m:.2f} m"

    def to_csv(self) -> str:
        return f"{super().to_csv()},{self._sensor_type},{self._range_m:.6f}"

    def get_specs_dict(self) -> Dict[str, str]:
        return {
            "Category": self._sensor_type,
            "Range": f"{self._range_m:.2f} m",
        }


class Controller(Component):
    """
    Derived hardware class: Controller (Microcontroller, SBC, Motor Driver).
    Specialized Attributes: Architecture Type, GPIO/Port Count.
    """

    def __init__(
        self,
        name: str,
        component_id: str,
        price: float,
        quantity: int,
        controller_type: str,
        num_ports: int,
    ):
        super().__init__(name, component_id, price, quantity)
        self._controller_type: str = str(controller_type).strip()
        self._num_ports: int = int(num_ports)

    @property
    def controller_type(self) -> str:
        return self._controller_type

    @property
    def num_ports(self) -> int:
        return self._num_ports

    def get_type(self) -> str:
        return "Controller"

    def display(self) -> str:
        base_str = super().display()
        return f"{base_str}\n  [Specs] Arch: {self._controller_type} | Ports: {self._num_ports}"

    def to_csv(self) -> str:
        return f"{super().to_csv()},{self._controller_type},{self._num_ports}"

    def get_specs_dict(self) -> Dict[str, str]:
        return {
            "Architecture": self._controller_type,
            "Ports": f"{self._num_ports} I/O",
        }


class Battery(Component):
    """
    Derived hardware class: Battery / Energy Storage.
    Specialized Attributes: Capacity (mAh), Chemistry Type (LiPo, Li-Ion, LiFePO4, NiMH).
    """

    def __init__(
        self,
        name: str,
        component_id: str,
        price: float,
        quantity: int,
        capacity: int,
        battery_type: str,
    ):
        super().__init__(name, component_id, price, quantity)
        self._capacity: int = int(capacity)
        self._battery_type: str = str(battery_type).strip()

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def battery_type(self) -> str:
        return self._battery_type

    def get_type(self) -> str:
        return "Battery"

    def display(self) -> str:
        base_str = super().display()
        return f"{base_str}\n  [Specs] Capacity: {self._capacity} mAh | Chem: {self._battery_type}"

    def to_csv(self) -> str:
        return f"{super().to_csv()},{self._capacity},{self._battery_type}"

    def get_specs_dict(self) -> Dict[str, str]:
        return {
            "Capacity": f"{self._capacity} mAh",
            "Chemistry": self._battery_type,
        }


class Converter(Component):
    """
    Derived hardware class: DC-DC Voltage Converter / Regulator.
    Specialized Attributes: Input Voltage (V), Output Voltage (V).
    """

    def __init__(
        self,
        name: str,
        component_id: str,
        price: float,
        quantity: int,
        input_voltage: float,
        output_voltage: float,
    ):
        super().__init__(name, component_id, price, quantity)
        self._input_voltage: float = float(input_voltage)
        self._output_voltage: float = float(output_voltage)

    @property
    def input_voltage(self) -> float:
        return self._input_voltage

    @property
    def output_voltage(self) -> float:
        return self._output_voltage

    def get_type(self) -> str:
        return "Converter"

    def display(self) -> str:
        base_str = super().display()
        return f"{base_str}\n  [Specs] Input: {self._input_voltage:.2f}V | Output: {self._output_voltage:.2f}V"

    def to_csv(self) -> str:
        return f"{super().to_csv()},{self._input_voltage:.6f},{self._output_voltage:.6f}"

    def get_specs_dict(self) -> Dict[str, str]:
        return {
            "Input Voltage": f"{self._input_voltage:.1f} V",
            "Output Voltage": f"{self._output_voltage:.1f} V",
        }
