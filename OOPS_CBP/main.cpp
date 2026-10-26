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

// Command-Line Interface Driver
int main() {
    Inventory inventory;
    int choice = 0;

    do {
        std::cout << "\n=== ROBOTICS COMPONENT INVENTORY MANAGEMENT SYSTEM ===" << std::endl;
        std::cout << "1. Add Component" << std::endl;
        std::cout << "2. Display All Components" << std::endl;  
        std::cout << "3. Search Component by ID" << std::endl;
        std::cout << "4. Search Component by Name" << std::endl;
        std::cout << "5. Calculate Total Inventory Valuation" << std::endl;
        std::cout << "6. Exit" << std::endl;
        std::cout << "Enter your choice (1-6): ";
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
                    case 1: {
                        newComponent = std::make_shared<Component>(name, id, price, quantity);
                        break;
                    }
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
            case 5:
                std::cout << "\nTotal Valuation of Current Stock: $" 
                          << std::fixed << std::setprecision(2) 
                          << inventory.calculateTotalInventoryValue() << std::endl;
                break;

            case 6:
                std::cout << "Exiting system. Goodbye!" << std::endl;
                return 0;

            default:
                std::cout << "Invalid option selected. Please choose between 1 and 6." << std::endl;
                break;
        }
    } while (choice != 6);

    return 0;
}