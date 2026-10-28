#ifndef ROBOTICSPROJECT_HPP
#define ROBOTICSPROJECT_HPP

#include <vector>
#include <memory>
#include <string>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <algorithm>

#include "Component.hpp"

struct ProjectItem {
    std::shared_ptr<Component> component;
    int requiredQuantity;

    double getLineTotal() const {
        return component->getPrice() * requiredQuantity;
    }
};

class RoboticsProject {
private:
    std::string projectName;
    std::vector<ProjectItem> items;
    double taxRate;
    double shippingCost;

public:
    RoboticsProject(const std::string& name = "Autonomous Mobile Robot (AMR-01)")
        : projectName(name), taxRate(0.0825), shippingCost(15.00) {}

    void setProjectName(const std::string& name) { projectName = name; }
    std::string getProjectName() const { return projectName; }

    bool addItem(std::shared_ptr<Component> component, int requiredQty) {
        if (!component || requiredQty <= 0) return false;

        for (auto& item : items) {
            if (item.component->getId() == component->getId()) {
                int total = item.requiredQuantity + requiredQty;
                if (total > component->getQuantity()) return false;
                item.requiredQuantity = total;
                return true;
            }
        }

        if (requiredQty > component->getQuantity()) return false;
        items.push_back({component, requiredQty});
        return true;
    }

    bool removeItem(const std::string& id) {
        auto it = std::remove_if(items.begin(), items.end(),
            [&id](const ProjectItem& i) { return i.component->getId() == id; });
        if (it == items.end()) return false;
        items.erase(it, items.end());
        return true;
    }

    void clear() { items.clear(); }

    double calculateSubtotal() const {
        double total = 0.0;
        for (const auto& item : items) total += item.getLineTotal();
        return total;
    }

    double calculateTax() const { return calculateSubtotal() * taxRate; }

    double calculateGrandTotal() const {
        return calculateSubtotal() + calculateTax() + (items.empty() ? 0.0 : shippingCost);
    }

    void displayProjectSummary() const {
        if (items.empty()) {
            std::cout << "\nProject '" << projectName << "' has no components added.\n";
            return;
        }

        std::cout << "\n=======================================================\n";
        std::cout << " PROJECT BOM & COST ESTIMATE: " << projectName << "\n";
        std::cout << "=======================================================\n";
        for (const auto& item : items) {
            std::cout << "  • " << std::left << std::setw(30) << item.component->getName()
                      << " | ID: " << std::setw(8) << item.component->getId()
                      << " | Qty: " << std::setw(3) << item.requiredQuantity
                      << " | Total: $" << std::fixed << std::setprecision(2) << item.getLineTotal() << "\n";
        }
        std::cout << "-------------------------------------------------------\n";
        std::cout << "  Subtotal: $" << std::fixed << std::setprecision(2) << calculateSubtotal() << "\n";
        std::cout << "  Tax (" << (taxRate * 100.0) << "%): $" << calculateTax() << "\n";
        std::cout << "  Shipping: $" << shippingCost << "\n";
        std::cout << "  GRAND TOTAL: $" << calculateGrandTotal() << "\n";
        std::cout << "=======================================================\n\n";
    }

    bool exportReceiptTXT(const std::string& filename) const {
        if (items.empty()) return false;
        std::ofstream file(filename);
        if (!file.is_open()) return false;

        file << "=======================================================\n";
        file << "         ROBOTICS HARDWARE ESTIMATION RECEIPT          \n";
        file << "=======================================================\n";
        file << "Project: " << projectName << "\n";
        file << "-------------------------------------------------------\n";
        for (const auto& item : items) {
            file << item.component->getName() << " (" << item.component->getId() << ")"
                 << " x " << item.requiredQuantity << " @ $" << std::fixed << std::setprecision(2) << item.component->getPrice()
                 << " = $" << item.getLineTotal() << "\n";
        }
        file << "-------------------------------------------------------\n";
        file << "Subtotal    : $" << calculateSubtotal() << "\n";
        file << "Estimated Tax: $" << calculateTax() << "\n";
        file << "Shipping    : $" << shippingCost << "\n";
        file << "GRAND TOTAL : $" << calculateGrandTotal() << "\n";
        file << "=======================================================\n";
        file.close();
        return true;
    }
};

#endif // ROBOTICSPROJECT_HPP
