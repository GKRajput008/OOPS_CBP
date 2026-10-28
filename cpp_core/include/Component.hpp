#ifndef COMPONENT_HPP
#define COMPONENT_HPP

#include <string>
#include <iostream>
#include <iomanip>

/**
 * @brief Base Component Class
 * Encapsulates core hardware properties: name, unique id, unit price, and in-stock quantity.
 * Declares polymorphic virtual interfaces for type classification, display, and serialization.
 */
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
    [[nodiscard]] std::string getName() const { return name; }
    [[nodiscard]] std::string getId() const { return id; }
    [[nodiscard]] double getPrice() const { return price; }
    [[nodiscard]] int getQuantity() const { return quantity; }

    // Setters
    void setQuantity(int q) { 
        if (q >= 0) quantity = q; 
    }
    
    void setPrice(double p) {
        if (p >= 0.0) price = p;
    }

    [[nodiscard]] double getTotalValue() const { 
        return price * quantity; 
    }

    // Polymorphic Virtual Methods
    [[nodiscard]] virtual std::string getType() const { 
        return "Generic"; 
    }

    virtual void display() const {
        std::cout << "Type: " << std::left << std::setw(11) << getType()
                  << " | Name: " << std::setw(28) << name 
                  << " | ID: " << std::setw(8) << id 
                  << " | Price: $" << std::right << std::fixed << std::setprecision(2) << std::setw(7) << price 
                  << " | Stock: " << std::setw(4) << quantity 
                  << " | Total: $" << std::setw(8) << getTotalValue() << std::endl;
    }

    [[nodiscard]] virtual std::string toCSV() const {
        return getType() + "," + name + "," + id + "," + std::to_string(price) + "," + std::to_string(quantity);
    }
};

#endif // COMPONENT_HPP
