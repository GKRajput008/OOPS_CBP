# Robotics Components Inventory Management System & Cost Estimator
### Object-Oriented Programming (OOPS) — Course Based Project (CBP)

---

## 📌 Project Overview
This project is an **Object-Oriented Hardware Inventory Management & Bill of Materials (BOM) Cost Estimator** tailored for robotics laboratories. It demonstrates the real-world application of C++ Object-Oriented Programming principles integrated with modern UI options:
1. **Student-Friendly C++ Console Core (`main.cpp`)**: A clean, single-file, highly-readable C++17 implementation specifically formatted for lab evaluations and viva.
2. **Desktop GUI Application (`main.py`)**: A native Python PyQt6 desktop application featuring tabbed dashboards, polymorphic tables, and BOM builders.
3. **Modern Web UI Dashboard (`index.html`)**: A glassmorphic web interface that runs instantly in any browser without requiring any software installations.

---

## 🏛️ Core OOPS Concepts Demonstrated in `main.cpp`

| OOPS Pillar | Implementation in Project | Code Reference |
| :--- | :--- | :--- |
| **Encapsulation** | Private & protected state attributes (`name`, `id`, `price`, `quantity`), exposed via validated public getters and setters (e.g., preventing negative inventory). | `Component::setQuantity()`, `Component::getTotalValue()` |
| **Inheritance** | Base class `Component` inherited by 5 specialized hardware subclasses: `Motor`, `Sensor`, `Controller`, `Battery`, `Converter`. | `class Motor : public Component`, `class Sensor : public Component` |
| **Polymorphism** | Dynamic dispatch at runtime via virtual methods (`display()`, `getType()`, `toCSV()`, virtual destructor `~Component()`) using base-class smart pointers (`std::shared_ptr<Component>`). | `virtual std::string getType() const`, `virtual void display() const` |
| **Abstraction** | Complex tokenized CSV file persistence, stock bounds verification, and invoice calculations are cleanly abstracted behind the `Inventory` and `RoboticsProject` classes. | `inventory.loadFromCSV()`, `currentProject.calculateGrandTotal()` |

---

## 🚀 How to Run the Project

### Option 1: Run the Student-Friendly C++ Program
- **Quick 1-Click Launch**: Double-click `run_cpp.bat`
- **Manual Command Line**:
  ```bash
  # Compile main.cpp with g++
  g++ -std=c++17 -Wall main.cpp -o main.exe

  # Run the executable
  .\main.exe
  ```

### Option 2: Run the PyQt6 Desktop GUI
- **Quick 1-Click Launch**: Double-click `run_gui.bat`
- **Manual Command Line**:
  ```bash
  py main.py
  # or: python main.py
  ```

### Option 3: Run the Modern Web Dashboard
- **Quick 1-Click Launch**: Double-click `run_web.bat` or simply double-click `index.html` in your file explorer.
- **Optional Local Server**:
  ```bash
  py -m http.server 8000
  # Then open http://localhost:8000 in your browser
  ```

---

## 📋 Comprehensive Feature Checklist

### 1. Hardware Catalog & Polymorphic Classes
- **Polymorphic Hierarchy**:
  - `Motor`: Operating Voltage ($V$), Maximum RPM
  - `Sensor`: Sensor Category (Optical, Ultrasonic, IMU), Sensing Range ($m$)
  - `Controller`: Architecture (ARM Cortex, AVR RISC), I/O Port Count
  - `Battery`: Capacity ($mAh$), Chemistry Type (LiPo, Li-Ion, LiFePO4)
  - `Converter`: Input Voltage ($V$), Regulated Output Voltage ($V$)
  - `Generic`: Structural and mounting hardware
- **Interactive Search**: Real-time filtering by name, ID, or specification.
- **Category Filter**: Filter views specifically for Motors, Sensors, Controllers, Batteries, etc.
- **Stock Management**: Increase/decrease quantities with automatic validation.
- **Shortage Warning**: Highlight items with stock $\le 10$ units.

### 2. Robotics Project BOM & Cost Estimator
- **Custom Project Naming**: E.g., *"Autonomous Mobile Robot (AMR-01)"*.
- **Stock-Bounded Allocation**: You cannot allocate more units to a robot build than what physically exists in the inventory warehouse.
- **Itemized Pricing**: Line totals calculated as $\text{Unit Price} \times \text{Allocated Qty}$.
- **Margins & Taxes**: Configurable Tax Rate (%) and Logistics/Shipping ($).
- **Official Invoice Export**: 1-click export of an official build quote receipt to `project_receipt.txt`.

### 3. CSV File Persistence
- **Auto-Load on Start**: Automatically reads `inventory.csv` on launch.
- **Dual Directory Detection**: Seamlessly checks both `./inventory.csv` and `../inventory.csv`.
- **Auto-Save on Exit**: Saves updated inventory state to `inventory.csv`.

---

## 🎓 Viva & Lab Exam Q&A Guide

**Q1: Where is Polymorphism used in this project?**
> In `main.cpp`, the base class `Component` declares `virtual std::string getType() const` and `virtual void display() const`. In `Inventory`, we store a `std::vector<std::shared_ptr<Component>>`. When we loop through the vector and invoke `comp->display()`, C++ resolves the correct derived class method at runtime using the virtual method table (vtable).

**Q2: How does your code enforce Encapsulation?**
> The component's price and stock quantity are protected/private members. They cannot be modified directly from outside the class. The setter `setQuantity(int q)` checks `if (q >= 0)` to guarantee negative stock cannot enter the system.

**Q3: How are smart pointers used?**
> We use `std::shared_ptr<Component>` and `std::make_shared<DerivedClass>()`. This automatically manages heap memory and prevents memory leaks without needing manual `delete` calls.
