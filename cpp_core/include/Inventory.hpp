#ifndef INVENTORY_HPP
#define INVENTORY_HPP

#include <vector>
#include <memory>
#include <string>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <cctype>

#include "Component.hpp"
#include "Motor.hpp"
#include "Sensor.hpp"
#include "Controller.hpp"
#include "Battery.hpp"
#include "Converter.hpp"

/**
 * @brief Inventory Management Class
 * Encapsulates dynamic collection of polymorphic Component pointers with CSV persistence.
 */
class Inventory {
private:
    std::vector<std::shared_ptr<Component>> components;

    static std::string toLower(std::string s) {
        std::transform(s.begin(), s.end(), s.begin(), [](unsigned char c) {
            return std::tolower(c);
        });
        return s;
    }

public:
    bool addComponent(std::shared_ptr<Component> component) {
        if (!component) return false;
        if (findById(component->getId()) != nullptr) {
            std::cout << "  [!] Error: Component ID '" << component->getId() << "' already exists.\n";
            return false;
        }
        components.push_back(component);
        return true;
    }

    void displayAllComponents() const {
        if (components.empty()) {
            std::cout << "\nInventory is currently empty.\n";
            return;
        }

        std::cout << "\n" << std::string(82, '-') << "\n";
        std::cout << std::left << std::setw(11) << "Category"
                  << " | " << std::setw(28) << "Component Name"
                  << " | " << std::setw(8)  << "ID"
                  << " | " << std::setw(9)  << "Price"
                  << " | " << std::setw(5)  << "Stock"
                  << " | " << std::setw(10) << "Total Val" << "\n";
        std::cout << std::string(82, '-') << "\n";

        for (const auto& comp : components) {
            comp->display();
        }
        std::cout << std::string(82, '-') << "\n";
        std::cout << "Total SKUs: " << components.size()
                  << " | Gross Valuation: $" << std::fixed << std::setprecision(2)
                  << calculateTotalInventoryValue() << "\n\n";
    }

    void displayByCategory(const std::string& category) const {
        std::string query = toLower(category);
        bool found = false;
        for (const auto& comp : components) {
            if (toLower(comp->getType()) == query) {
                if (!found) {
                    std::cout << "\n--- CATEGORY: " << category << " ---\n";
                    found = true;
                }
                comp->display();
            }
        }
        if (!found) {
            std::cout << "  [!] No components found in category: '" << category << "'\n";
        }
    }

    void displayLowStock(int threshold = 10) const {
        std::cout << "\n--- LOW STOCK SHORTAGE ALERT (<= " << threshold << " units) ---\n";
        bool alert = false;
        for (const auto& comp : components) {
            if (comp->getQuantity() <= threshold) {
                comp->display();
                alert = true;
            }
        }
        if (!alert) {
            std::cout << "  [OK] All components have sufficient stock levels (> " << threshold << ").\n";
        }
    }

    bool updateQuantity(const std::string& id, int newQuantity) {
        if (newQuantity < 0) return false;
        auto comp = findById(id);
        if (!comp) return false;
        comp->setQuantity(newQuantity);
        return true;
    }

    bool removeComponent(const std::string& id) {
        auto it = std::remove_if(components.begin(), components.end(),
            [&id](const std::shared_ptr<Component>& c) { return c->getId() == id; });
        if (it == components.end()) return false;
        components.erase(it, components.end());
        return true;
    }

    std::shared_ptr<Component> findById(const std::string& id) const {
        for (const auto& c : components) {
            if (c->getId() == id) return c;
        }
        return nullptr;
    }

    std::shared_ptr<Component> findByName(const std::string& name) const {
        std::string query = toLower(name);
        for (const auto& c : components) {
            if (toLower(c->getName()).find(query) != std::string::npos) return c;
        }
        return nullptr;
    }

    double calculateTotalInventoryValue() const {
        double total = 0.0;
        for (const auto& c : components) total += c->getTotalValue();
        return total;
    }

    const std::vector<std::shared_ptr<Component>>& getComponents() const {
        return components;
    }

    bool saveToCSV(const std::string& filename) const {
        std::ofstream file(filename);
        if (!file.is_open()) return false;
        for (const auto& comp : components) {
            file << comp->toCSV() << "\n";
        }
        file.close();
        return true;
    }

    bool loadFromCSV(const std::string& filename) {
        std::ifstream file(filename);
        if (!file.is_open()) return false;

        std::string line;
        int count = 0;
        while (std::getline(file, line)) {
            if (line.empty()) continue;
            std::stringstream ss(line);
            std::vector<std::string> tokens;
            std::string token;
            while (std::getline(ss, token, ',')) tokens.push_back(token);
            if (tokens.size() < 5) continue;

            std::string type = tokens[0];
            std::string name = tokens[1];
            std::string id = tokens[2];
            double price = 0.0;
            int qty = 0;
            try {
                price = std::stod(tokens[3]);
                qty = std::stoi(tokens[4]);
            } catch (...) { continue; }

            std::shared_ptr<Component> comp = nullptr;
            try {
                if (type == "Generic") {
                    comp = std::make_shared<Component>(name, id, price, qty);
                } else if (type == "Motor" && tokens.size() >= 7) {
                    comp = std::make_shared<Motor>(name, id, price, qty, std::stoi(tokens[5]), std::stoi(tokens[6]));
                } else if (type == "Sensor" && tokens.size() >= 7) {
                    comp = std::make_shared<Sensor>(name, id, price, qty, tokens[5], std::stod(tokens[6]));
                } else if (type == "Controller" && tokens.size() >= 7) {
                    comp = std::make_shared<Controller>(name, id, price, qty, tokens[5], std::stoi(tokens[6]));
                } else if (type == "Battery" && tokens.size() >= 7) {
                    comp = std::make_shared<Battery>(name, id, price, qty, std::stoi(tokens[5]), tokens[6]);
                } else if (type == "Converter" && tokens.size() >= 7) {
                    comp = std::make_shared<Converter>(name, id, price, qty, std::stod(tokens[5]), std::stod(tokens[6]));
                }
            } catch (...) { continue; }

            if (comp) {
                addComponent(comp);
                count++;
            }
        }
        file.close();
        return count > 0;
    }
};

#endif // INVENTORY_HPP
