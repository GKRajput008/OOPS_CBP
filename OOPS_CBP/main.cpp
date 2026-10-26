//Robotics components inventory management system
#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <algorithm>
#include <iomanip>

class Component {
    std::string name;
    std::string id;
    double price;
    int quantity;
public:
    Component(const std::string& n, const std::string& i, double p, int q) : name(n), id(i), price(p), quantity(q) {}
    std::string getName() const { return name; }
    std::string getId() const { return id; }
    double getPrice() const { return price; }
    int getQuantity() const { return quantity; }
    void setQuantity(int q) { quantity = q; }
    double getTotalValue() const { return price * quantity; }
    virtual void display() const {
        std::cout << "Component Name: " << name << ", ID: " << id << ", Price: $" << price << ", Quantity: " << quantity << std::endl;
    }
    virtual ~Component() = default;
};

class Inventory {
    std::vector<std::shared_ptr<Component>> components;
public:
    bool addComponent(std::shared_ptr<Component> component) {
        if(!component) return false;
        if(findById(component->getId()) != nullptr) {
            std::cout << "Component with ID " << component->getId() << " already exists." << std::endl;
            return false;
        }

        components.push_back(component);
        return true;
    }   
    void displayAllComponents() const {
        for(const auto& component : components) {
            component->display();
        }
    }
    [[nodiscard]] std::shared_ptr<Component> findById(const std::string& id) const {
        for(const auto& component : components) {
            if(component->getId() == id) {
                return component;
            }
        }
        return nullptr;
    }

    [[nodiscard]] std::shared_ptr<Component> findByName(const std::string& name) const {
        for(const auto& component : components) {
            if(component->getName() == name) {
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
        for(const auto& component : components) {
            totalValue += component->getTotalValue();
        }
        return totalValue;
    }
};

class Motor : public Component {
    int operatingVoltage; 
    int rpm;
public:
    Motor(const std::string& n, const std::string& i, double p, int q, int voltage, int r) 
        : Component(n, i, p, q), operatingVoltage(voltage), rpm(r) {}
    void display() const override {
        Component::display();
        std::cout << "Operating Voltage: " << operatingVoltage << "V, RPM: " << rpm << std::endl;
    }
};

class Sensor : public Component {
    std::string sensorType; 
    double range;
public:
    Sensor(const std::string& n, const std::string& i, double p, int q, const std::string& type, double r) 
        : Component(n, i, p, q), sensorType(type), range(r) {}
    void display() const override {
        Component::display();
        std::cout << "Sensor Type: " << sensorType << ", Range: " << range << " meters" << std::endl;
    }   
};

class Controller : public Component {
    std::string controllerType; 
    int numPorts;
public:
    Controller(const std::string& n, const std::string& i, double p, int q, const std::string& type, int ports) 
        : Component(n, i, p, q), controllerType(type), numPorts(ports) {}
    void display() const override {
        Component::display();
        std::cout << "Controller Type: " << controllerType << ", Number of Ports: " << numPorts << std::endl;
    }
};

class Battery : public Component {
    int capacity; 
    std::string batteryType;
public:
    Battery(const std::string& n, const std::string& i, double p, int q, int cap, const std::string& type) 
        : Component(n, i, p, q), capacity(cap), batteryType(type) {}
    void display() const override {
        Component::display();
        std::cout << "Battery Capacity: " << capacity << "mAh, Battery Type: " << batteryType << std::endl;
    }
};

class converter : public Component {
    double inputVoltage; 
    double outputVoltage;
public:
    converter(const std::string& n, const std::string& i, double p, int q, double inputV, double outputV) 
        : Component(n, i, p, q), inputVoltage(inputV), outputVoltage(outputV) {}    
    void display() const override {
        Component::display();
        std::cout << "Input Voltage: " << inputVoltage << "V, Output Voltage: " << outputVoltage << "V" << std::endl;
    }
};


int main() {
    Inventory inventory;
    int choice = 0;
    do{
        std::cout << "Robotics Components Inventory Management System" << std::endl;
        std::cout << "1. Add Component" << std::endl;
        std::cout << "2. Display All Components" << std::endl;  
        std::cout << "3. Search Component by ID" << std::endl;
        std::cout << "4. Search Component by Name" << std::endl;
        std::cout << "5. Calculate Total Inventory Value" << std::endl;
        std::cout << "6. Exit" << std::endl;
        std::cout << "Enter your choice: ";
        std::cin >> choice;
        std::cin.ignore(); // Clear the input buffer

        switch(choice) {
            case 1: {
                std::string name, id;
                double price;
                int quantity;
                std::cout << "Enter Component Name: ";
                std::getline(std::cin >> std::ws, name); // Use std::ws to consume any leading whitespace
                std::cout << "Enter Component ID: ";
                std::cin >> id;
                std::cout << "Enter Component Price: ";
                std::cin >> price;
                std::cout << "Enter Component Quantity: ";
                std::cin >> quantity;

                auto component = std::make_shared<Component>(name, id, price, quantity);
                if(inventory.addComponent(component)) {
                    std::cout << "Component added successfully." << std::endl;
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
                if(component) {
                    component->display();
                } else {
                    std::cout << "Component not found." << std::endl;
                }
                break;
            }
            case 4: {
                std::string name;
                std::cout << "Enter Component Name to search: ";
                std::cin >> name;
                auto component = inventory.findByName(name);
                if(component) {
                    component->display();
                } else {
                    std::cout << "Component not found." << std::endl;
                }
                break;
            }
            case 5:
                std::cout << "Total Inventory Value: $" << inventory.calculateTotalInventoryValue() << std::endl;
                break;
            case 6:
                return 0; // Exit the program
            default:
                std::cout << "Invalid choice. Please try again." << std::endl;
        }
    }
    while(choice != 6);
    return 0;
}