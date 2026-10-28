// ============================================================================
// PROJECT TITLE: Robotics Components Inventory Management & Cost Estimator
// COURSE BASED PROJECT (CBP) - Object-Oriented Programming (OOPS) in C++
// ============================================================================
// This project demonstrates the 4 fundamental pillars of OOP:
//   1. ENCAPSULATION: Data hiding with private members, public getters/setters,
//                     and input validation.
//   2. INHERITANCE: Base class 'Component' inherited by 'Motor', 'Sensor',
//                   'Controller', 'Battery', and 'Converter'.
//   3. POLYMORPHISM: Virtual functions (getType, display, toCSV), runtime
//                    dispatch using base-class pointers (std::shared_ptr).
//   4. ABSTRACTION: Clean interfaces hiding CSV parsing and invoice math.
// ============================================================================

#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <algorithm>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <cctype>

// ----------------------------------------------------------------------------
// HELPER FUNCTIONS FOR SAFE USER INPUT (Prevents infinite loops on bad input)
// ----------------------------------------------------------------------------
int readInt(const std::string& prompt) {
    int val;
    while (true) {
        std::cout << prompt;
        if (std::cin >> val) {
            std::cin.ignore(10000, '\n'); // clear rest of line
            return val;
        }
        std::cout << "  [!] Invalid integer. Please enter a valid number.\n";
        std::cin.clear();
        std::cin.ignore(10000, '\n');
    }
}

double readDouble(const std::string& prompt) {
    double val;
    while (true) {
        std::cout << prompt;
        if (std::cin >> val) {
            std::cin.ignore(10000, '\n');
            return val;
        }
        std::cout << "  [!] Invalid number. Please enter a valid decimal or integer.\n";
        std::cin.clear();
        std::cin.ignore(10000, '\n');
    }
}

std::string readLine(const std::string& prompt) {
    std::string line;
    std::cout << prompt;
    std::getline(std::cin >> std::ws, line);
    return line;
}

std::string toLowerStr(std::string str) {
    std::transform(str.begin(), str.end(), str.begin(), [](unsigned char c) {
        return std::tolower(c);
    });
    return str;
}

// ============================================================================
// OOP PILLAR 1: BASE CLASS & ENCAPSULATION
// ============================================================================
class Component {
protected:
    std::string name;
    std::string id;
    double price;
    int quantity;

public:
    Component(const std::string& n, const std::string& i, double p, int q)
        : name(n), id(i), price(p >= 0.0 ? p : 0.0), quantity(q >= 0 ? q : 0) {}

    virtual ~Component() = default;

    // Getters
    std::string getName() const { return name; }
    std::string getId() const { return id; }
    double getPrice() const { return price; }
    int getQuantity() const { return quantity; }

    // Setters with validation
    void setQuantity(int q) {
        if (q >= 0) quantity = q;
    }
    void setPrice(double p) {
        if (p >= 0.0) price = p;
    }

    double getTotalValue() const {
        return price * quantity;
    }

    // OOP PILLAR 3: POLYMORPHIC VIRTUAL FUNCTIONS
    virtual std::string getType() const {
        return "Generic";
    }

    virtual void display() const {
        std::cout << std::left << std::setw(11) << getType()
                  << " | " << std::setw(28) << name
                  << " | " << std::setw(8)  << id
                  << " | $" << std::right << std::fixed << std::setprecision(2) << std::setw(8) << price
                  << " | " << std::setw(5)  << quantity
                  << " | $" << std::setw(9) << getTotalValue() << std::endl;
    }

    virtual void displayDetailed() const {
        std::cout << "Type: " << getType()
                  << " | Name: " << name
                  << " | ID: " << id
                  << " | Price: $" << std::fixed << std::setprecision(2) << price
                  << " | In-Stock: " << quantity
                  << " | Valuation: $" << getTotalValue() << std::endl;
    }

    virtual std::string toCSV() const {
        return getType() + "," + name + "," + id + "," + std::to_string(price) + "," + std::to_string(quantity);
    }
};

// ============================================================================
// OOP PILLAR 2: INHERITANCE (DERIVED HARDWARE CLASSES)
// ============================================================================

// Derived Class 1: Motor
class Motor : public Component {
    int operatingVoltage;
    int rpm;

public:
    Motor(const std::string& n, const std::string& i, double p, int q, int voltage, int r)
        : Component(n, i, p, q), operatingVoltage(voltage), rpm(r) {}

    int getVoltage() const { return operatingVoltage; }
    int getRpm() const { return rpm; }

    std::string getType() const override { return "Motor"; }

    void displayDetailed() const override {
        Component::displayDetailed();
        std::cout << "  └─ [Motor Specs] Voltage: " << operatingVoltage << "V | Max RPM: " << rpm << std::endl;
    }

    std::string toCSV() const override {
        return Component::toCSV() + "," + std::to_string(operatingVoltage) + "," + std::to_string(rpm);
    }
};

// Derived Class 2: Sensor
class Sensor : public Component {
    std::string sensorType;
    double range;

public:
    Sensor(const std::string& n, const std::string& i, double p, int q, const std::string& type, double r)
        : Component(n, i, p, q), sensorType(type), range(r) {}

    std::string getSensorType() const { return sensorType; }
    double getRange() const { return range; }

    std::string getType() const override { return "Sensor"; }

    void displayDetailed() const override {
        Component::displayDetailed();
        std::cout << "  └─ [Sensor Specs] Category: " << sensorType << " | Sensing Range: " << range << " m" << std::endl;
    }

    std::string toCSV() const override {
        return Component::toCSV() + "," + sensorType + "," + std::to_string(range);
    }
};

// Derived Class 3: Controller
class Controller : public Component {
    std::string controllerType;
    int numPorts;

public:
    Controller(const std::string& n, const std::string& i, double p, int q, const std::string& type, int ports)
        : Component(n, i, p, q), controllerType(type), numPorts(ports) {}

    std::string getControllerType() const { return controllerType; }
    int getNumPorts() const { return numPorts; }

    std::string getType() const override { return "Controller"; }

    void displayDetailed() const override {
        Component::displayDetailed();
        std::cout << "  └─ [Controller Specs] Architecture: " << controllerType << " | I/O Ports: " << numPorts << std::endl;
    }

    std::string toCSV() const override {
        return Component::toCSV() + "," + controllerType + "," + std::to_string(numPorts);
    }
};

// Derived Class 4: Battery
class Battery : public Component {
    int capacity;
    std::string batteryType;

public:
    Battery(const std::string& n, const std::string& i, double p, int q, int cap, const std::string& type)
        : Component(n, i, p, q), capacity(cap), batteryType(type) {}

    int getCapacity() const { return capacity; }
    std::string getBatteryType() const { return batteryType; }

    std::string getType() const override { return "Battery"; }

    void displayDetailed() const override {
        Component::displayDetailed();
        std::cout << "  └─ [Battery Specs] Capacity: " << capacity << " mAh | Chemistry: " << batteryType << std::endl;
    }

    std::string toCSV() const override {
        return Component::toCSV() + "," + std::to_string(capacity) + "," + batteryType;
    }
};

// Derived Class 5: Converter
class Converter : public Component {
    double inputVoltage;
    double outputVoltage;

public:
    Converter(const std::string& n, const std::string& i, double p, int q, double inV, double outV)
        : Component(n, i, p, q), inputVoltage(inV), outputVoltage(outV) {}

    double getInputVoltage() const { return inputVoltage; }
    double getOutputVoltage() const { return outputVoltage; }

    std::string getType() const override { return "Converter"; }

    void displayDetailed() const override {
        Component::displayDetailed();
        std::cout << "  └─ [Converter Specs] Input: " << inputVoltage << "V | Regulated Output: " << outputVoltage << "V" << std::endl;
    }

    std::string toCSV() const override {
        return Component::toCSV() + "," + std::to_string(inputVoltage) + "," + std::to_string(outputVoltage);
    }
};

// ============================================================================
// OOP PILLAR 4: ABSTRACTION & DATA PERSISTENCE (INVENTORY MANAGEMENT)
// ============================================================================
class Inventory {
    std::vector<std::shared_ptr<Component>> components;

public:
    bool addComponent(std::shared_ptr<Component> component) {
        if (!component) return false;

        if (findById(component->getId()) != nullptr) {
            std::cout << "  [!] Error: Component with ID '" << component->getId() << "' already exists." << std::endl;
            return false;
        }

        components.push_back(component);
        return true;
    }

    void printTableHeader() const {
        std::cout << "\n" << std::string(82, '-') << std::endl;
        std::cout << std::left << std::setw(11) << "Category"
                  << " | " << std::setw(28) << "Component Name"
                  << " | " << std::setw(8)  << "ID"
                  << " | " << std::setw(9)  << "Price"
                  << " | " << std::setw(5)  << "Stock"
                  << " | " << std::setw(10) << "Total Val" << std::endl;
        std::cout << std::string(82, '-') << std::endl;
    }

    void displayAllComponents() const {
        if (components.empty()) {
            std::cout << "\nInventory is currently empty.\n";
            return;
        }

        std::cout << "\n======================== CURRENT HARDWARE INVENTORY ========================";
        printTableHeader();
        for (const auto& comp : components) {
            comp->display();
        }
        std::cout << std::string(82, '-') << std::endl;
        std::cout << "Total Components: " << components.size()
                  << " | Total Inventory Valuation: $" << std::fixed << std::setprecision(2)
                  << calculateTotalInventoryValue() << "\n" << std::endl;
    }

    void displayByCategory(const std::string& category) const {
        std::string catLower = toLowerStr(category);
        std::vector<std::shared_ptr<Component>> filtered;
        for (const auto& c : components) {
            if (toLowerStr(c->getType()) == catLower) {
                filtered.push_back(c);
            }
        }

        if (filtered.empty()) {
            std::cout << "\nNo components found under category: '" << category << "'\n";
            return;
        }

        std::cout << "\n================= CATEGORY: " << category << " =================";
        printTableHeader();
        for (const auto& comp : filtered) {
            comp->display();
        }
        std::cout << std::string(82, '-') << std::endl;
    }

    void displayLowStock(int threshold = 10) const {
        std::vector<std::shared_ptr<Component>> lowStock;
        for (const auto& c : components) {
            if (c->getQuantity() <= threshold) {
                lowStock.push_back(c);
            }
        }

        std::cout << "\n================ CRITICAL LOW STOCK ALERT (<= " << threshold << " units) ================";
        if (lowStock.empty()) {
            std::cout << "\n[OK] All components have sufficient stock levels (> " << threshold << " units).\n";
            return;
        }

        printTableHeader();
        for (const auto& comp : lowStock) {
            comp->display();
        }
        std::cout << std::string(82, '-') << std::endl;
        std::cout << "Warning: " << lowStock.size() << " item(s) require immediate replenishment.\n";
    }

    void displayStatistics() const {
        if (components.empty()) {
            std::cout << "\nNo statistics available. Inventory is empty.\n";
            return;
        }

        int totalUnits = 0;
        double totalVal = 0.0;
        for (const auto& c : components) {
            totalUnits += c->getQuantity();
            totalVal += c->getTotalValue();
        }

        double avgPrice = totalVal / (totalUnits > 0 ? totalUnits : 1);

        std::cout << "\n================== INVENTORY TELEMETRY & STATS ==================\n";
        std::cout << "  • Unique Hardware SKUs  : " << components.size() << "\n";
        std::cout << "  • Total Physical Units  : " << totalUnits << "\n";
        std::cout << "  • Gross Valuation       : $" << std::fixed << std::setprecision(2) << totalVal << "\n";
        std::cout << "  • Average Unit Value    : $" << std::fixed << std::setprecision(2) << avgPrice << "\n";
        std::cout << "=================================================================\n";
    }

    bool updateQuantity(const std::string& id, int newQuantity) {
        if (newQuantity < 0) {
            std::cout << "  [!] Error: Stock quantity cannot be negative.\n";
            return false;
        }

        auto component = findById(id);
        if (!component) {
            std::cout << "  [!] Error: Component ID '" << id << "' not found.\n";
            return false;
        }

        component->setQuantity(newQuantity);
        std::cout << "  [✓] Updated stock for [" << id << "] " << component->getName()
                  << " to " << newQuantity << " units.\n";
        return true;
    }

    bool removeComponent(const std::string& id) {
        auto it = std::remove_if(components.begin(), components.end(),
            [&id](const std::shared_ptr<Component>& component) {
                return component->getId() == id;
            });

        if (it == components.end()) {
            std::cout << "  [!] Error: Component ID '" << id << "' not found.\n";
            return false;
        }

        components.erase(it, components.end());
        std::cout << "  [✓] Removed component ID '" << id << "' from inventory.\n";
        return true;
    }

    std::shared_ptr<Component> findById(const std::string& id) const {
        for (const auto& component : components) {
            if (component->getId() == id) return component;
        }
        return nullptr;
    }

    std::shared_ptr<Component> findByName(const std::string& name) const {
        std::string query = toLowerStr(name);
        for (const auto& component : components) {
            if (toLowerStr(component->getName()).find(query) != std::string::npos) {
                return component;
            }
        }
        return nullptr;
    }

    double calculateTotalInventoryValue() const {
        double totalValue = 0.0;
        for (const auto& component : components) {
            totalValue += component->getTotalValue();
        }
        return totalValue;
    }

    const std::vector<std::shared_ptr<Component>>& getAll() const {
        return components;
    }

    // CSV File Operations
    bool saveToCSV(const std::string& filename) const {
        std::ofstream file(filename);
        if (!file.is_open()) {
            std::cout << "  [!] Error opening file for writing: " << filename << "\n";
            return false;
        }

        for (const auto& comp : components) {
            file << comp->toCSV() << "\n";
        }

        file.close();
        std::cout << "  [✓] Saved " << components.size() << " records to " << filename << "\n";
        return true;
    }

    bool loadFromCSV(const std::string& filename) {
        std::ifstream file(filename);
        if (!file.is_open()) {
            return false;
        }

        std::string line;
        int loadedCount = 0;
        while (std::getline(file, line)) {
            if (line.empty()) continue;

            std::stringstream ss(line);
            std::vector<std::string> tokens;
            std::string token;

            while (std::getline(ss, token, ',')) {
                tokens.push_back(token);
            }

            if (tokens.size() < 5) continue;

            std::string type = tokens[0];
            std::string name = tokens[1];
            std::string id = tokens[2];
            double price = 0.0;
            int quantity = 0;

            try {
                price = std::stod(tokens[3]);
                quantity = std::stoi(tokens[4]);
            } catch (...) {
                continue;
            }

            std::shared_ptr<Component> comp = nullptr;

            try {
                if (type == "Generic") {
                    comp = std::make_shared<Component>(name, id, price, quantity);
                } else if (type == "Motor" && tokens.size() >= 7) {
                    comp = std::make_shared<Motor>(name, id, price, quantity, std::stoi(tokens[5]), std::stoi(tokens[6]));
                } else if (type == "Sensor" && tokens.size() >= 7) {
                    comp = std::make_shared<Sensor>(name, id, price, quantity, tokens[5], std::stod(tokens[6]));
                } else if (type == "Controller" && tokens.size() >= 7) {
                    comp = std::make_shared<Controller>(name, id, price, quantity, tokens[5], std::stoi(tokens[6]));
                } else if (type == "Battery" && tokens.size() >= 7) {
                    comp = std::make_shared<Battery>(name, id, price, quantity, std::stoi(tokens[5]), tokens[6]);
                } else if (type == "Converter" && tokens.size() >= 7) {
                    comp = std::make_shared<Converter>(name, id, price, quantity, std::stod(tokens[5]), std::stod(tokens[6]));
                }
            } catch (...) {
                continue;
            }

            if (comp) {
                addComponent(comp);
                loadedCount++;
            }
        }

        file.close();
        std::cout << "  [✓] Loaded " << loadedCount << " components from " << filename << "\n";
        return true;
    }
};

// ============================================================================
// ROBOTICS PROJECT BILL OF MATERIALS (BOM) & COST ESTIMATOR
// ============================================================================
struct ProjectItem {
    std::shared_ptr<Component> component;
    int requiredQuantity;

    double getLineTotal() const {
        return component->getPrice() * requiredQuantity;
    }
};

class RoboticsProject {
    std::string projectName;
    std::vector<ProjectItem> items;
    double taxRate;     // e.g., 0.0825 (8.25%)
    double shippingCost;// e.g., $15.00

public:
    RoboticsProject(const std::string& name = "Autonomous Mobile Robot (AMR-01)")
        : projectName(name), taxRate(0.0825), shippingCost(15.00) {}

    void setProjectName(const std::string& name) { projectName = name; }
    std::string getProjectName() const { return projectName; }

    bool addItem(std::shared_ptr<Component> component, int requiredQty) {
        if (!component) return false;

        if (requiredQty <= 0) {
            std::cout << "  [!] Quantity must be greater than 0.\n";
            return false;
        }

        // Check if item already exists in BOM
        for (auto& item : items) {
            if (item.component->getId() == component->getId()) {
                int combined = item.requiredQuantity + requiredQty;
                if (combined > component->getQuantity()) {
                    std::cout << "  [!] Insufficient inventory stock for '" << component->getName() << "'!\n";
                    std::cout << "      Requested total: " << combined
                              << " | Available in stock: " << component->getQuantity()
                              << " (Already allocated: " << item.requiredQuantity << ")\n";
                    return false;
                }
                item.requiredQuantity = combined;
                std::cout << "  [✓] Increased allocation for [" << component->getId() << "] to " << combined << " units.\n";
                return true;
            }
        }

        if (requiredQty > component->getQuantity()) {
            std::cout << "  [!] Stock Cap Exceeded: Requested " << requiredQty
                      << ", but only " << component->getQuantity() << " available in inventory.\n";
            return false;
        }

        items.push_back({component, requiredQty});
        std::cout << "  [✓] Added " << requiredQty << "x '" << component->getName() << "' to project BOM.\n";
        return true;
    }

    bool removeItem(const std::string& id) {
        auto it = std::remove_if(items.begin(), items.end(),
            [&id](const ProjectItem& item) {
                return item.component->getId() == id;
            });

        if (it == items.end()) {
            std::cout << "  [!] Component ID '" << id << "' not found in BOM.\n";
            return false;
        }

        items.erase(it, items.end());
        std::cout << "  [✓] Removed component ID '" << id << "' from project BOM.\n";
        return true;
    }

    void clear() {
        items.clear();
        std::cout << "  [✓] Project BOM cleared.\n";
    }

    int getItemCount() const {
        return static_cast<int>(items.size());
    }

    double calculateSubtotal() const {
        double subtotal = 0.0;
        for (const auto& item : items) subtotal += item.getLineTotal();
        return subtotal;
    }

    double calculateTax() const {
        return calculateSubtotal() * taxRate;
    }

    double calculateGrandTotal() const {
        return calculateSubtotal() + calculateTax() + (items.empty() ? 0.0 : shippingCost);
    }

    void displayProjectSummary() const {
        if (items.empty()) {
            std::cout << "\nRobotics Project '" << projectName << "' currently has no components added.\n";
            return;
        }

        std::cout << "\n==========================================================================\n";
        std::cout << "           ROBOTICS PROJECT BILL OF MATERIALS & COST QUOTE               \n";
        std::cout << "==========================================================================\n";
        std::cout << "Project Name: " << projectName << "\n";
        std::cout << std::string(74, '-') << "\n";
        std::cout << std::left << std::setw(30) << "Hardware Item"
                  << " | " << std::setw(8)  << "ID"
                  << " | " << std::setw(9)  << "Unit Price"
                  << " | " << std::setw(5)  << "Qty"
                  << " | " << std::setw(10) << "Line Total" << "\n";
        std::cout << std::string(74, '-') << "\n";

        for (const auto& item : items) {
            std::cout << std::left << std::setw(30) << item.component->getName()
                      << " | " << std::setw(8)  << item.component->getId()
                      << " | $" << std::right << std::fixed << std::setprecision(2) << std::setw(8) << item.component->getPrice()
                      << " | " << std::setw(5)  << item.requiredQuantity
                      << " | $" << std::setw(9) << item.getLineTotal() << "\n";
        }

        std::cout << std::string(74, '=') << "\n";
        std::cout << "  Subtotal                  : $" << std::fixed << std::setprecision(2) << calculateSubtotal() << "\n";
        std::cout << "  Estimated Tax (" << std::fixed << std::setprecision(2) << (taxRate * 100.0) << "%)      : $" << calculateTax() << "\n";
        std::cout << "  Standard Shipping         : $" << shippingCost << "\n";
        std::cout << "  --------------------------------------------------------\n";
        std::cout << "  GRAND ESTIMATED BUILD COST: $" << calculateGrandTotal() << "\n";
        std::cout << "==========================================================================\n\n";
    }

    bool exportReceiptTXT(const std::string& filename) const {
        if (items.empty()) {
            std::cout << "  [!] Cannot export empty BOM. Add components to the project first.\n";
            return false;
        }

        std::ofstream file(filename);
        if (!file.is_open()) {
            std::cout << "  [!] Error opening file for receipt export: " << filename << "\n";
            return false;
        }

        file << "==========================================================================\n";
        file << "             OFFICIAL ROBOTICS HARDWARE QUOTE & RECEIPT                  \n";
        file << "==========================================================================\n";
        file << "Project Name      : " << projectName << "\n";
        file << "Generated Date    : 2026-10-27\n";
        file << "Inventory System  : Robotics Laboratory ERP [Phase 4 / OOPS CBP]\n";
        file << "--------------------------------------------------------------------------\n";
        file << std::left << std::setw(32) << "Hardware Component"
             << " | " << std::setw(9)  << "ID"
             << " | " << std::setw(10) << "Unit Price"
             << " | " << std::setw(5)  << "Qty"
             << " | " << std::setw(11) << "Line Total" << "\n";
        file << "--------------------------------------------------------------------------\n";

        for (const auto& item : items) {
            file << std::left << std::setw(32) << item.component->getName()
                 << " | " << std::setw(9)  << item.component->getId()
                 << " | $" << std::right << std::fixed << std::setprecision(2) << std::setw(9) << item.component->getPrice()
                 << " | " << std::setw(5)  << item.requiredQuantity
                 << " | $" << std::setw(10) << item.getLineTotal() << "\n";
        }

        file << "==========================================================================\n";
        file << "  Subtotal                  : $" << std::fixed << std::setprecision(2) << calculateSubtotal() << "\n";
        file << "  Estimated Tax (" << std::fixed << std::setprecision(2) << (taxRate * 100.0) << "%)      : $" << calculateTax() << "\n";
        file << "  Shipping & Logistics      : $" << shippingCost << "\n";
        file << "  ----------------------------------------------------------------------\n";
        file << "  FINAL TOTAL ESTIMATED COST: $" << calculateGrandTotal() << "\n";
        file << "==========================================================================\n";
        file << "Authorized Signature: __________________________   Date: _________________\n";

        file.close();
        std::cout << "  [✓] Official project invoice saved to: " << filename << "\n";
        return true;
    }
};

// ============================================================================
// STUDENT-FRIENDLY INTERACTIVE CONSOLE MENU
// ============================================================================
int main() {
    Inventory inventory;
    RoboticsProject currentProject("Autonomous Mobile Robot (AMR-01)");

    std::cout << "\n===============================================================\n";
    std::cout << "  ROBOTICS COMPONENT INVENTORY & COST ESTIMATOR (OOPS CBP)    \n";
    std::cout << "===============================================================\n";

    // Auto-detect and load sample data from local or parent directory
    std::string csvLoadedPath = "inventory.csv";
    if (!inventory.loadFromCSV("inventory.csv")) {
        if (inventory.loadFromCSV("../inventory.csv")) {
            csvLoadedPath = "../inventory.csv";
        } else {
            std::cout << "  [*] Notice: Starting with fresh blank inventory.\n";
        }
    }

    int choice = 0;

    do {
        std::cout << "\n----------------------- MAIN MENU -----------------------\n";
        std::cout << " [1]  Add New Component to Inventory\n";
        std::cout << " [2]  Display All Components\n";
        std::cout << " [3]  Search Component by ID\n";
        std::cout << " [4]  Search Component by Name\n";
        std::cout << " [5]  Filter Components by Category\n";
        std::cout << " [6]  View Critical Low-Stock Alerts (<= 10 units)\n";
        std::cout << " [7]  Update Component Stock Quantity\n";
        std::cout << " [8]  Remove Component from Inventory\n";
        std::cout << " [9]  View Inventory Telemetry & Statistics\n";
        std::cout << " [10] Add Component to Robotics Project Build (BOM)\n";
        std::cout << " [11] Display Project Bill of Materials & Cost Quote\n";
        std::cout << " [12] Remove Item / Clear Project BOM\n";
        std::cout << " [13] Save Inventory to CSV File\n";
        std::cout << " [14] Export Official Build Invoice (TXT)\n";
        std::cout << " [15] Exit System\n";
        std::cout << "---------------------------------------------------------\n";

        choice = readInt("Enter your selection (1-15): ");

        switch (choice) {
            case 1: {
                std::cout << "\nSelect Component Category:\n";
                std::cout << " 1. Generic Hardware\n";
                std::cout << " 2. Motor (Operating Voltage, Max RPM)\n";
                std::cout << " 3. Sensor (Sensor Category, Detection Range)\n";
                std::cout << " 4. Controller Board (Architecture, I/O Ports)\n";
                std::cout << " 5. Battery (Capacity mAh, Chemistry)\n";
                std::cout << " 6. Voltage Converter (Input V, Output V)\n";
                int cat = readInt("Select Category (1-6): ");

                std::string name = readLine("Enter Component Name: ");
                std::string id = readLine("Enter Component ID (e.g. MOT-004): ");
                double price = readDouble("Enter Unit Price ($): ");
                int qty = readInt("Enter In-Stock Quantity: ");

                std::shared_ptr<Component> comp = nullptr;

                if (cat == 1) {
                    comp = std::make_shared<Component>(name, id, price, qty);
                } else if (cat == 2) {
                    int v = readInt("Operating Voltage (V): ");
                    int rpm = readInt("Maximum RPM: ");
                    comp = std::make_shared<Motor>(name, id, price, qty, v, rpm);
                } else if (cat == 3) {
                    std::string stype = readLine("Sensor Type (e.g., Optical, Ultrasonic, IMU): ");
                    double r = readDouble("Detection Range (meters): ");
                    comp = std::make_shared<Sensor>(name, id, price, qty, stype, r);
                } else if (cat == 4) {
                    std::string arch = readLine("Controller Architecture (e.g., ARM Cortex-M4, AVR): ");
                    int ports = readInt("Total I/O Ports: ");
                    comp = std::make_shared<Controller>(name, id, price, qty, arch, ports);
                } else if (cat == 5) {
                    int cap = readInt("Battery Capacity (mAh): ");
                    std::string btype = readLine("Battery Chemistry (e.g., LiPo, Li-Ion, LiFePO4): ");
                    comp = std::make_shared<Battery>(name, id, price, qty, cap, btype);
                } else if (cat == 6) {
                    double inv = readDouble("Input Voltage (V): ");
                    double outv = readDouble("Output Voltage (V): ");
                    comp = std::make_shared<Converter>(name, id, price, qty, inv, outv);
                } else {
                    std::cout << "  [!] Invalid category selection.\n";
                }

                if (comp && inventory.addComponent(comp)) {
                    std::cout << "  [✓] Successfully added " << comp->getType() << " [" << id << "] to inventory!\n";
                }
                break;
            }

            case 2:
                inventory.displayAllComponents();
                break;

            case 3: {
                std::string id = readLine("Enter Component ID: ");
                auto comp = inventory.findById(id);
                if (comp) {
                    std::cout << "\n[Match Found]\n";
                    comp->displayDetailed();
                } else {
                    std::cout << "  [!] Component ID '" << id << "' not found.\n";
                }
                break;
            }

            case 4: {
                std::string name = readLine("Enter Component Name (or partial search): ");
                auto comp = inventory.findByName(name);
                if (comp) {
                    std::cout << "\n[Match Found]\n";
                    comp->displayDetailed();
                } else {
                    std::cout << "  [!] No component found matching '" << name << "'.\n";
                }
                break;
            }

            case 5: {
                std::cout << "Available Categories: Motor, Sensor, Controller, Battery, Converter, Generic\n";
                std::string cat = readLine("Enter Category name to filter: ");
                inventory.displayByCategory(cat);
                break;
            }

            case 6: {
                int threshold = readInt("Enter Stock Shortage Threshold (default 10): ");
                inventory.displayLowStock(threshold);
                break;
            }

            case 7: {
                std::string id = readLine("Enter Component ID to update: ");
                int newQty = readInt("Enter New Stock Quantity: ");
                inventory.updateQuantity(id, newQty);
                break;
            }

            case 8: {
                std::string id = readLine("Enter Component ID to remove: ");
                inventory.removeComponent(id);
                break;
            }

            case 9:
                inventory.displayStatistics();
                break;

            case 10: {
                std::string id = readLine("Enter Component ID for project build: ");
                auto comp = inventory.findById(id);
                if (comp) {
                    std::cout << "  Selected: " << comp->getName()
                              << " (Available Stock: " << comp->getQuantity() << ")\n";
                    int reqQty = readInt("Enter Required Quantity: ");
                    currentProject.addItem(comp, reqQty);
                } else {
                    std::cout << "  [!] Component ID '" << id << "' not found in inventory.\n";
                }
                break;
            }

            case 11:
                currentProject.displayProjectSummary();
                break;

            case 12: {
                std::cout << "\n 1. Remove specific component from BOM\n";
                std::cout << " 2. Clear entire BOM\n";
                int subChoice = readInt("Choice (1-2): ");
                if (subChoice == 1) {
                    std::string id = readLine("Enter Component ID to remove from BOM: ");
                    currentProject.removeItem(id);
                } else if (subChoice == 2) {
                    currentProject.clear();
                }
                break;
            }

            case 13: {
                std::string filename = readLine("Enter CSV filename (press Enter for 'inventory.csv'): ");
                if (filename.empty()) filename = "inventory.csv";
                inventory.saveToCSV(filename);
                break;
            }

            case 14: {
                std::string filename = readLine("Enter filename for Invoice TXT (press Enter for 'project_receipt.txt'): ");
                if (filename.empty()) filename = "project_receipt.txt";
                currentProject.exportReceiptTXT(filename);
                break;
            }

            case 15:
                inventory.saveToCSV(csvLoadedPath);
                std::cout << "\n  [✓] Auto-saved inventory state to " << csvLoadedPath << ".\n";
                std::cout << "  Thank you for using the Robotics ERP System. Goodbye!\n\n";
                break;

            default:
                std::cout << "  [!] Invalid choice. Please select an option between 1 and 15.\n";
                break;
        }

    } while (choice != 15);

    return 0;
}