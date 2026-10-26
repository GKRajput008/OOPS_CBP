// Robotics Components Inventory Management System
#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <algorithm>
#include <iomanip>

// Base Component Class
class Component {
    std::string name;
    std::string id;
    double price;
    int quantity;

public:
    Component(const std::string& n, const std::string& i, double p, int q) 
        : name(n), id(i), price(p), quantity(q) {}

    std::string getName() const { return name; }
    std::string getId() const { return id; }
    double getPrice() const { return price; }
    int getQuantity() const { return quantity; }
    void setQuantity(int q) { quantity = q; }
    double getTotalValue() const { return price * quantity; }

    virtual void display() const {
        std::cout << "Component Name: " << name 
                  << " | ID: " << id 
                  << " | Unit Price: $" << std::fixed << std::setprecision(2) << price 
                  << " | Stock Quantity: " << quantity 
                  << " | Total Value: $" << getTotalValue() << std::endl;
    }

    virtual ~Component() = default;
};

// Derived Class: Motor
class Motor : public Component {
    int operatingVoltage; 
    int rpm;

public:
    Motor(const std::string& n, const std::string& i, double p, int q, int voltage, int r) 
        : Component(n, i, p, q), operatingVoltage(voltage), rpm(r) {}

    void display() const override {
        Component::display();
        std::cout << "  [Motor Specs] Operating Voltage: " << operatingVoltage << "V | Max RPM: " << rpm << std::endl;
    }
};

// Derived Class: Sensor
class Sensor : public Component {
    std::string sensorType; 
    double range;

public:
    Sensor(const std::string& n, const std::string& i, double p, int q, const std::string& type, double r) 
        : Component(n, i, p, q), sensorType(type), range(r) {}

    void display() const override {
        Component::display();
        std::cout << "  [Sensor Specs] Type: " << sensorType << " | Sensing Range: " << range << " meters" << std::endl;
    }   
};

// Derived Class: Controller
class Controller : public Component {
    std::string controllerType; 
    int numPorts;

public:
    Controller(const std::string& n, const std::string& i, double p, int q, const std::string& type, int ports) 
        : Component(n, i, p, q), controllerType(type), numPorts(ports) {}

    void display() const override {
        Component::display();
        std::cout << "  [Controller Specs] Architecture: " << controllerType << " | GPIO/IO Ports: " << numPorts << std::endl;
    }
};

// Derived Class: Battery
class Battery : public Component {
    int capacity; 
    std::string batteryType;

public:
    Battery(const std::string& n, const std::string& i, double p, int q, int cap, const std::string& type) 
        : Component(n, i, p, q), capacity(cap), batteryType(type) {}

    void display() const override {
        Component::display();
        std::cout << "  [Battery Specs] Capacity: " << capacity << " mAh | Chemistry: " << batteryType << std::endl;
    }
};

// Derived Class: Converter
class Converter : public Component {
    double inputVoltage; 
    double outputVoltage;

public:
    Converter(const std::string& n, const std::string& i, double p, int q, double inputV, double outputV) 
        : Component(n, i, p, q), inputVoltage(inputV), outputVoltage(outputV) {}    

    void display() const override {
        Component::display();
        std::cout << "  [Converter Specs] Input Voltage: " << inputVoltage << "V | Output Voltage: " << outputVoltage << "V" << std::endl;
    }
};

// Inventory Management Class
class Inventory {
    std::vector<std::shared_ptr<Component>> components;

public:
    bool addComponent(std::shared_ptr<Component> component) {
        if (!component) return false;

        if (findById(component->getId()) != nullptr) {
            std::cout << "Error: Component with ID '" << component->getId() << "' already exists in inventory." << std::endl;
            return false;
        }

        components.push_back(component);
        return true;
    }   

    void displayAllComponents() const {
        if (components.empty()) {
            std::cout << "Inventory is currently empty." << std::endl;
            return;
        }

        std::cout << "\n------------------- CURRENT INVENTORY -------------------" << std::endl;
        for (const auto& component : components) {
            component->display();
            std::cout << "---------------------------------------------------------" << std::endl;
        }
    }

    bool updateQuantity(const std::string& id, int newQuantity) {
        if (newQuantity < 0) {
            std::cout << "Error: Quantity cannot be negative." << std::endl;
            return false;
        }

        auto component = findById(id);
        if (!component) {
            std::cout << "Error: Component with ID '" << id << "' not found." << std::endl;
            return false;
        }

        component->setQuantity(newQuantity);
        std::cout << "Successfully updated stock quantity for component ID '" << id << "' to " << newQuantity << "." << std::endl;
        return true;
    }

    bool removeComponent(const std::string& id) {
        auto it = std::remove_if(components.begin(), components.end(),
            [&id](const std::shared_ptr<Component>& component) {
                return component->getId() == id;
            });

        if (it == components.end()) {
            std::cout << "Error: Component with ID '" << id << "' not found." << std::endl;
            return false;
        }

        components.erase(it, components.end());
        std::cout << "Successfully removed component with ID '" << id << "' from inventory." << std::endl;
        return true;
    }

    [[nodiscard]] std::shared_ptr<Component> findById(const std::string& id) const {
        for (const auto& component : components) {
            if (component->getId() == id) {
                return component;
            }
        }
        return nullptr;
    }

    [[nodiscard]] std::shared_ptr<Component> findByName(const std::string& name) const {
        for (const auto& component : components) {
            if (component->getName() == name) {
                return component;
            }
        }
        return nullptr;
    }

    [[nodiscard]] std::vector<std::shared_ptr<Component>> getAllComponents() const {
        return components;
    }

    [[nodiscard]] double calculateTotalInventoryValue() const {
        double totalValue = 0.0;
        for (const auto& component : components) {
            totalValue += component->getTotalValue();
        }
        return totalValue;
    }
};

// Structure representing an item inside a specific project bill of materials
struct ProjectItem {
    std::shared_ptr<Component> component;
    int requiredQuantity;

    double getLineTotal() const {
        return component->getPrice() * requiredQuantity;
    }
};

// Robotics Project / Cost Estimator Class (Phase 1 Sub-step 4 & 5)
class RoboticsProject {
    std::string projectName;
    std::vector<ProjectItem> items;

public:
    RoboticsProject(const std::string& name = "Custom Robot Build") : projectName(name) {}

    void setProjectName(const std::string& name) { projectName = name; }
    std::string getProjectName() const { return projectName; }

    bool addItem(std::shared_ptr<Component> component, int requiredQty) {
        if (!component) return false;

        if (requiredQty <= 0) {
            std::cout << "Error: Required quantity must be greater than 0." << std::endl;
            return false;
        }

        if (requiredQty > component->getQuantity()) {
            std::cout << "Error: Insufficient inventory stock for '" << component->getName() 
                      << "'. Requested: " << requiredQty 
                      << ", Available Stock: " << component->getQuantity() << std::endl;
            return false;
        }

        items.push_back({component, requiredQty});
        std::cout << "Added " << requiredQty << "x '" << component->getName() 
                  << "' to project '" << projectName << "'." << std::endl;
        return true;
    }

    [[nodiscard]] double calculateEstimatedCost() const {
        double total = 0.0;
        for (const auto& item : items) {
            total += item.getLineTotal();
        }
        return total;
    }

    void displayProjectSummary() const {
        if (items.empty()) {
            std::cout << "\nProject '" << projectName << "' currently has no components assigned." << std::endl;
            return;
        }

        std::cout << "\n=========================================================" << std::endl;
        std::cout << " PROJECT BILL OF MATERIALS & COST QUOTE: " << projectName << std::endl;
        std::cout << "=========================================================" << std::endl;
        for (const auto& item : items) {
            std::cout << "Item: " << item.component->getName()
                      << " (ID: " << item.component->getId() << ")"
                      << " | Unit Price: $" << std::fixed << std::setprecision(2) << item.component->getPrice()
                      << " | Required Qty: " << item.requiredQuantity
                      << " | Line Total: $" << item.getLineTotal() << std::endl;
        }
        std::cout << "---------------------------------------------------------" << std::endl;
        std::cout << "ESTIMATED TOTAL BUILD COST: $" << std::fixed << std::setprecision(2) << calculateEstimatedCost() << std::endl;
        std::cout << "=========================================================\n" << std::endl;
    }
};

// Command-Line Interface Driver
int main() {
    Inventory inventory;
    RoboticsProject currentProject("Autonomous Mobile Robot (AMR)");
    int choice = 0;

    do {
        std::cout << "\n=== ROBOTICS COMPONENT INVENTORY MANAGEMENT SYSTEM ===" << std::endl;
        std::cout << "1. Add Component to Inventory" << std::endl;
        std::cout << "2. Display All Components" << std::endl;  
        std::cout << "3. Search Component by ID" << std::endl;
        std::cout << "4. Search Component by Name" << std::endl;
        std::cout << "5. Update Component Stock" << std::endl;
        std::cout << "6. Remove Component from Inventory" << std::endl;
        std::cout << "7. Calculate Total Inventory Valuation" << std::endl;
        std::cout << "8. Add Component to Robotics Project Build" << std::endl;
        std::cout << "9. Display Robotics Project Bill of Materials & Quote" << std::endl;
        std::cout << "10. Exit" << std::endl;
        std::cout << "Enter your choice (1-10): ";
        std::cin >> choice;

        switch (choice) {
            case 1: {
                int typeChoice = 0;
                std::cout << "\nSelect Component Category:" << std::endl;
                std::cout << "1. Base / Generic Component" << std::endl;
                std::cout << "2. Motor" << std::endl;
                std::cout << "3. Sensor" << std::endl;
                std::cout << "4. Controller" << std::endl;
                std::cout << "5. Battery" << std::endl;
                std::cout << "6. Converter" << std::endl;
                std::cout << "Select type (1-6): ";
                std::cin >> typeChoice;

                std::string name, id;
                double price = 0.0;
                int quantity = 0;

                std::cout << "Enter Component Name: ";
                std::getline(std::cin >> std::ws, name);
                std::cout << "Enter Component ID: ";
                std::cin >> id;
                std::cout << "Enter Component Price ($): ";
                std::cin >> price;
                std::cout << "Enter Stock Quantity: ";
                std::cin >> quantity;

                std::shared_ptr<Component> newComponent = nullptr;

                switch (typeChoice) {
                    case 1:
                        newComponent = std::make_shared<Component>(name, id, price, quantity);
                        break;
                    case 2: {
                        int voltage = 0, rpm = 0;
                        std::cout << "Enter Operating Voltage (V): ";
                        std::cin >> voltage;
                        std::cout << "Enter Max RPM: ";
                        std::cin >> rpm;
                        newComponent = std::make_shared<Motor>(name, id, price, quantity, voltage, rpm);
                        break;
                    }
                    case 3: {
                        std::string sensorType;
                        double range = 0.0;
                        std::cout << "Enter Sensor Type (e.g., LIDAR, IMU, Ultrasonic): ";
                        std::getline(std::cin >> std::ws, sensorType);
                        std::cout << "Enter Range (meters): ";
                        std::cin >> range;
                        newComponent = std::make_shared<Sensor>(name, id, price, quantity, sensorType, range);
                        break;
                    }
                    case 4: {
                        std::string controllerType;
                        int ports = 0;
                        std::cout << "Enter Controller Type (e.g., ARM Cortex, AVR, ESP32): ";
                        std::getline(std::cin >> std::ws, controllerType);
                        std::cout << "Enter Number of I/O Ports: ";
                        std::cin >> ports;
                        newComponent = std::make_shared<Controller>(name, id, price, quantity, controllerType, ports);
                        break;
                    }
                    case 5: {
                        int capacity = 0;
                        std::string batteryType;
                        std::cout << "Enter Capacity (mAh): ";
                        std::cin >> capacity;
                        std::cout << "Enter Battery Type/Chemistry (e.g., LiPo, LiFePO4): ";
                        std::getline(std::cin >> std::ws, batteryType);
                        newComponent = std::make_shared<Battery>(name, id, price, quantity, capacity, batteryType);
                        break;
                    }
                    case 6: {
                        double inputV = 0.0, outputV = 0.0;
                        std::cout << "Enter Input Voltage (V): ";
                        std::cin >> inputV;
                        std::cout << "Enter Output Voltage (V): ";
                        std::cin >> outputV;
                        newComponent = std::make_shared<Converter>(name, id, price, quantity, inputV, outputV);
                        break;
                    }
                    default:
                        std::cout << "Invalid category selected. Aborting component creation." << std::endl;
                        break;
                }

                if (newComponent && inventory.addComponent(newComponent)) {
                    std::cout << "Component added successfully!" << std::endl;
                }
                break;
            }
            case 2:
                inventory.displayAllComponents();
                break;

            case 3: {
                std::string id;
                std::cout << "Enter Component ID to search: ";
                std::cin >> id;
                auto component = inventory.findById(id);
                if (component) {
                    std::cout << "\nMatching Component Found:" << std::endl;
                    component->display();
                } else {
                    std::cout << "Component with ID '" << id << "' not found." << std::endl;
                }
                break;
            }
            case 4: {
                std::string name;
                std::cout << "Enter Component Name to search: ";
                std::getline(std::cin >> std::ws, name);
                auto component = inventory.findByName(name);
                if (component) {
                    std::cout << "\nMatching Component Found:" << std::endl;
                    component->display();
                } else {
                    std::cout << "Component with name '" << name << "' not found." << std::endl;
                }
                break;
            }
            case 5: {
                std::string id;
                int newQuantity = 0;
                std::cout << "Enter Component ID to update stock: ";
                std::cin >> id;
                std::cout << "Enter New Stock Quantity: ";
                std::cin >> newQuantity;
                inventory.updateQuantity(id, newQuantity);
                break;
            }
            case 6: {
                std::string id;
                std::cout << "Enter Component ID to remove: ";
                std::cin >> id;
                inventory.removeComponent(id);
                break;
            }
            case 7:
                std::cout << "\nTotal Valuation of Current Stock: $" 
                          << std::fixed << std::setprecision(2) 
                          << inventory.calculateTotalInventoryValue() << std::endl;
                break;

            case 8: {
                std::string id;
                int reqQty = 0;
                std::cout << "Enter Component ID to add to project build: ";
                std::cin >> id;
                auto comp = inventory.findById(id);
                if (!comp) {
                    std::cout << "Error: Component with ID '" << id << "' not found in inventory." << std::endl;
                } else {
                    std::cout << "Enter Required Quantity for Project: ";
                    std::cin >> reqQty;
                    currentProject.addItem(comp, reqQty);
                }
                break;
            }
            case 9:
                currentProject.displayProjectSummary();
                break;

            case 10:
                std::cout << "Exiting system. Goodbye!" << std::endl;
                return 0;

            default:
                std::cout << "Invalid option selected. Please choose between 1 and 10." << std::endl;
                break;
        }
    } while (choice != 10);

    return 0;
}