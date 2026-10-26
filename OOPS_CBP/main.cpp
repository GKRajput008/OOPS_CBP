// Robotics Components Inventory Management System & Cost Estimator
#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <algorithm>
#include <iomanip>
#include <fstream>
#include <sstream>

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

    virtual std::string getType() const { return "Generic"; }

    virtual void display() const {
        std::cout << "Type: " << getType()
                  << " | Name: " << name 
                  << " | ID: " << id 
                  << " | Price: $" << std::fixed << std::setprecision(2) << price 
                  << " | Stock: " << quantity 
                  << " | Total: $" << getTotalValue() << std::endl;
    }

    virtual std::string toCSV() const {
        return getType() + "," + name + "," + id + "," + std::to_string(price) + "," + std::to_string(quantity);
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

    std::string getType() const override { return "Motor"; }

    void display() const override {
        Component::display();
        std::cout << "  [Specs] Voltage: " << operatingVoltage << "V | Max RPM: " << rpm << std::endl;
    }

    std::string toCSV() const override {
        return Component::toCSV() + "," + std::to_string(operatingVoltage) + "," + std::to_string(rpm);
    }
};

// Derived Class: Sensor
class Sensor : public Component {
    std::string sensorType; 
    double range;

public:
    Sensor(const std::string& n, const std::string& i, double p, int q, const std::string& type, double r) 
        : Component(n, i, p, q), sensorType(type), range(r) {}

    std::string getType() const override { return "Sensor"; }

    void display() const override {
        Component::display();
        std::cout << "  [Specs] Category: " << sensorType << " | Range: " << range << " m" << std::endl;
    }   

    std::string toCSV() const override {
        return Component::toCSV() + "," + sensorType + "," + std::to_string(range);
    }
};

// Derived Class: Controller
class Controller : public Component {
    std::string controllerType; 
    int numPorts;

public:
    Controller(const std::string& n, const std::string& i, double p, int q, const std::string& type, int ports) 
        : Component(n, i, p, q), controllerType(type), numPorts(ports) {}

    std::string getType() const override { return "Controller"; }

    void display() const override {
        Component::display();
        std::cout << "  [Specs] Arch: " << controllerType << " | Ports: " << numPorts << std::endl;
    }

    std::string toCSV() const override {
        return Component::toCSV() + "," + controllerType + "," + std::to_string(numPorts);
    }
};

// Derived Class: Battery
class Battery : public Component {
    int capacity; 
    std::string batteryType;

public:
    Battery(const std::string& n, const std::string& i, double p, int q, int cap, const std::string& type) 
        : Component(n, i, p, q), capacity(cap), batteryType(type) {}

    std::string getType() const override { return "Battery"; }

    void display() const override {
        Component::display();
        std::cout << "  [Specs] Capacity: " << capacity << " mAh | Chem: " << batteryType << std::endl;
    }

    std::string toCSV() const override {
        return Component::toCSV() + "," + std::to_string(capacity) + "," + batteryType;
    }
};

// Derived Class: Converter
class Converter : public Component {
    double inputVoltage; 
    double outputVoltage;

public:
    Converter(const std::string& n, const std::string& i, double p, int q, double inputV, double outputV) 
        : Component(n, i, p, q), inputVoltage(inputV), outputVoltage(outputV) {}    

    std::string getType() const override { return "Converter"; }

    void display() const override {
        Component::display();
        std::cout << "  [Specs] Input: " << inputVoltage << "V | Output: " << outputVoltage << "V" << std::endl;
    }

    std::string toCSV() const override {
        return Component::toCSV() + "," + std::to_string(inputVoltage) + "," + std::to_string(outputVoltage);
    }
};

// Inventory Management System
class Inventory {
    std::vector<std::shared_ptr<Component>> components;

public:
    bool addComponent(std::shared_ptr<Component> component) {
        if (!component) return false;

        if (findById(component->getId()) != nullptr) {
            std::cout << "Error: Component with ID '" << component->getId() << "' already exists." << std::endl;
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
            std::cout << "Error: Component ID '" << id << "' not found." << std::endl;
            return false;
        }

        component->setQuantity(newQuantity);
        std::cout << "Updated stock for ID '" << id << "' to " << newQuantity << "." << std::endl;
        return true;
    }

    bool removeComponent(const std::string& id) {
        auto it = std::remove_if(components.begin(), components.end(),
            [&id](const std::shared_ptr<Component>& component) {
                return component->getId() == id;
            });

        if (it == components.end()) {
            std::cout << "Error: Component ID '" << id << "' not found." << std::endl;
            return false;
        }

        components.erase(it, components.end());
        std::cout << "Removed component ID '" << id << "' from inventory." << std::endl;
        return true;
    }

    [[nodiscard]] std::shared_ptr<Component> findById(const std::string& id) const {
        for (const auto& component : components) {
            if (component->getId() == id) return component;
        }
        return nullptr;
    }

    [[nodiscard]] std::shared_ptr<Component> findByName(const std::string& name) const {
        for (const auto& component : components) {
            if (component->getName() == name) return component;
        }
        return nullptr;
    }

    [[nodiscard]] double calculateTotalInventoryValue() const {
        double totalValue = 0.0;
        for (const auto& component : components) {
            totalValue += component->getTotalValue();
        }
        return totalValue;
    }

    // CSV File Operations
    bool saveToCSV(const std::string& filename) const {
        std::ofstream file(filename);
        if (!file.is_open()) {
            std::cout << "Error opening file for writing: " << filename << std::endl;
            return false;
        }

        for (const auto& comp : components) {
            file << comp->toCSV() << "\n";
        }

        file.close();
        std::cout << "Successfully saved inventory to " << filename << std::endl;
        return true;
    }

    bool loadFromCSV(const std::string& filename) {
        std::ifstream file(filename);
        if (!file.is_open()) {
            std::cout << "No existing file found or error opening: " << filename << std::endl;
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
            double price = std::stod(tokens[3]);
            int quantity = std::stoi(tokens[4]);

            std::shared_ptr<Component> comp = nullptr;

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

            if (comp) {
                addComponent(comp);
                loadedCount++;
            }
        }

        file.close();
        std::cout << "Loaded " << loadedCount << " components from " << filename << std::endl;
        return true;
    }
};

// Structure representing an item inside a project bill of materials
struct ProjectItem {
    std::shared_ptr<Component> component;
    int requiredQuantity;

    double getLineTotal() const {
        return component->getPrice() * requiredQuantity;
    }
};

// Robotics Project / Cost Estimator Class
class RoboticsProject {
    std::string projectName;
    std::vector<ProjectItem> items;

public:
    RoboticsProject(const std::string& name = "Robotics Build") : projectName(name) {}

    void setProjectName(const std::string& name) { projectName = name; }
    std::string getProjectName() const { return projectName; }

    bool addItem(std::shared_ptr<Component> component, int requiredQty) {
        if (!component || requiredQty <= 0) return false;

        if (requiredQty > component->getQuantity()) {
            std::cout << "Error: Insufficient stock for '" << component->getName() 
                      << "'. Requested: " << requiredQty << ", Available: " << component->getQuantity() << std::endl;
            return false;
        }

        items.push_back({component, requiredQty});
        std::cout << "Added " << requiredQty << "x '" << component->getName() << "' to project build." << std::endl;
        return true;
    }

    [[nodiscard]] double calculateEstimatedCost() const {
        double total = 0.0;
        for (const auto& item : items) total += item.getLineTotal();
        return total;
    }

    void displayProjectSummary() const {
        if (items.empty()) {
            std::cout << "\nProject '" << projectName << "' has no components added yet." << std::endl;
            return;
        }

        std::cout << "\n=========================================================" << std::endl;
        std::cout << " PROJECT BILL OF MATERIALS & QUOTE: " << projectName << std::endl;
        std::cout << "=========================================================" << std::endl;
        for (const auto& item : items) {
            std::cout << "Item: " << item.component->getName()
                      << " (ID: " << item.component->getId() << ")"
                      << " | Unit: $" << std::fixed << std::setprecision(2) << item.component->getPrice()
                      << " | Qty: " << item.requiredQuantity
                      << " | Total: $" << item.getLineTotal() << std::endl;
        }
        std::cout << "---------------------------------------------------------" << std::endl;
        std::cout << "TOTAL ESTIMATED BUILD COST: $" << std::fixed << std::setprecision(2) << calculateEstimatedCost() << std::endl;
        std::cout << "=========================================================\n" << std::endl;
    }

    bool exportReceiptTXT(const std::string& filename) const {
        std::ofstream file(filename);
        if (!file.is_open()) {
            std::cout << "Error opening file for invoice export: " << filename << std::endl;
            return false;
        }

        file << "=========================================================\n";
        file << "            OFFICIAL ROBOTICS BUILD RECEIPT             \n";
        file << "=========================================================\n";
        file << "Project Name: " << projectName << "\n";
        file << "---------------------------------------------------------\n";

        for (const auto& item : items) {
            file << "Item: " << item.component->getName()
                 << " | ID: " << item.component->getId()
                 << " | Unit Price: $" << std::fixed << std::setprecision(2) << item.component->getPrice()
                 << " | Qty: " << item.requiredQuantity
                 << " | Subtotal: $" << item.getLineTotal() << "\n";
        }

        file << "---------------------------------------------------------\n";
        file << "TOTAL PROJECT COST: $" << std::fixed << std::setprecision(2) << calculateEstimatedCost() << "\n";
        file << "=========================================================\n";

        file.close();
        std::cout << "Successfully exported invoice receipt to " << filename << std::endl;
        return true;
    }
};

// Command-Line Interface Driver
int main() {
    Inventory inventory;
    RoboticsProject currentProject("Autonomous Mobile Robot");
    
    // Auto-load inventory from CSV on start
    inventory.loadFromCSV("inventory.csv");

    int choice = 0;

    do {
        std::cout << "\n=== ROBOTICS COMPONENT INVENTORY & COST ESTIMATOR ===" << std::endl;
        std::cout << "1. Add Component to Inventory" << std::endl;
        std::cout << "2. Display All Components" << std::endl;  
        std::cout << "3. Search Component by ID" << std::endl;
        std::cout << "4. Search Component by Name" << std::endl;
        std::cout << "5. Update Component Stock" << std::endl;
        std::cout << "6. Remove Component from Inventory" << std::endl;
        std::cout << "7. Calculate Total Inventory Valuation" << std::endl;
        std::cout << "8. Add Component to Project Build" << std::endl;
        std::cout << "9. Display Project Bill of Materials & Quote" << std::endl;
        std::cout << "10. Save Inventory to CSV" << std::endl;
        std::cout << "11. Export Project Invoice to TXT" << std::endl;
        std::cout << "12. Exit" << std::endl;
        std::cout << "Enter choice (1-12): ";
        std::cin >> choice;

        switch (choice) {
            case 1: {
                int typeChoice = 0;
                std::cout << "\nSelect Category:\n1. Base\n2. Motor\n3. Sensor\n4. Controller\n5. Battery\n6. Converter\nChoice: ";
                std::cin >> typeChoice;

                std::string name, id;
                double price = 0.0;
                int quantity = 0;

                std::cout << "Enter Name: ";
                std::getline(std::cin >> std::ws, name);
                std::cout << "Enter ID: ";
                std::cin >> id;
                std::cout << "Enter Price ($): ";
                std::cin >> price;
                std::cout << "Enter Quantity: ";
                std::cin >> quantity;

                std::shared_ptr<Component> newComp = nullptr;

                switch (typeChoice) {
                    case 1: newComp = std::make_shared<Component>(name, id, price, quantity); break;
                    case 2: {
                        int v = 0, rpm = 0;
                        std::cout << "Voltage (V): "; std::cin >> v;
                        std::cout << "RPM: "; std::cin >> rpm;
                        newComp = std::make_shared<Motor>(name, id, price, quantity, v, rpm);
                        break;
                    }
                    case 3: {
                        std::string stype; double r = 0.0;
                        std::cout << "Sensor Type: "; std::getline(std::cin >> std::ws, stype);
                        std::cout << "Range (m): "; std::cin >> r;
                        newComp = std::make_shared<Sensor>(name, id, price, quantity, stype, r);
                        break;
                    }
                    case 4: {
                        std::string ctype; int p = 0;
                        std::cout << "Controller Type: "; std::getline(std::cin >> std::ws, ctype);
                        std::cout << "Ports: "; std::cin >> p;
                        newComp = std::make_shared<Controller>(name, id, price, quantity, ctype, p);
                        break;
                    }
                    case 5: {
                        int cap = 0; std::string btype;
                        std::cout << "Capacity (mAh): "; std::cin >> cap;
                        std::cout << "Battery Type: "; std::getline(std::cin >> std::ws, btype);
                        newComp = std::make_shared<Battery>(name, id, price, quantity, cap, btype);
                        break;
                    }
                    case 6: {
                        double inv = 0.0, outv = 0.0;
                        std::cout << "Input Voltage: "; std::cin >> inv;
                        std::cout << "Output Voltage: "; std::cin >> outv;
                        newComp = std::make_shared<Converter>(name, id, price, quantity, inv, outv);
                        break;
                    }
                }

                if (newComp && inventory.addComponent(newComp)) {
                    std::cout << "Component added successfully!" << std::endl;
                }
                break;
            }
            case 2: inventory.displayAllComponents(); break;
            case 3: {
                std::string id; std::cout << "Enter ID: "; std::cin >> id;
                auto comp = inventory.findById(id);
                if (comp) comp->display();
                else std::cout << "Not found." << std::endl;
                break;
            }
            case 4: {
                std::string name; std::cout << "Enter Name: "; std::getline(std::cin >> std::ws, name);
                auto comp = inventory.findByName(name);
                if (comp) comp->display();
                else std::cout << "Not found." << std::endl;
                break;
            }
            case 5: {
                std::string id; int q = 0;
                std::cout << "Enter ID: "; std::cin >> id;
                std::cout << "Enter New Stock: "; std::cin >> q;
                inventory.updateQuantity(id, q);
                break;
            }
            case 6: {
                std::string id; std::cout << "Enter ID: "; std::cin >> id;
                inventory.removeComponent(id);
                break;
            }
            case 7:
                std::cout << "Total Inventory Valuation: $" << std::fixed << std::setprecision(2) << inventory.calculateTotalInventoryValue() << std::endl;
                break;
            case 8: {
                std::string id; int q = 0;
                std::cout << "Enter Component ID for project: "; std::cin >> id;
                auto comp = inventory.findById(id);
                if (comp) {
                    std::cout << "Enter Required Quantity: "; std::cin >> q;
                    currentProject.addItem(comp, q);
                } else {
                    std::cout << "Component not found." << std::endl;
                }
                break;
            }
            case 9: currentProject.displayProjectSummary(); break;
            case 10: inventory.saveToCSV("inventory.csv"); break;
            case 11: currentProject.exportReceiptTXT("project_receipt.txt"); break;
            case 12:
                inventory.saveToCSV("inventory.csv");
                std::cout << "Saved data. Goodbye!" << std::endl;
                return 0;
            default:
                std::cout << "Invalid choice." << std::endl;
                break;
        }
    } while (choice != 12);

    return 0;
}