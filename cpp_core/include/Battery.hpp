#ifndef BATTERY_HPP
#define BATTERY_HPP

#include "Component.hpp"

/**
 * @brief Derived Class: Battery
 * Specialization for energy storage systems, chemical cells, and battery packs.
 */
class Battery : public Component {
private:
    int capacity; 
    std::string batteryType;

public:
    Battery(const std::string& n, const std::string& i, double p, int q, int cap, const std::string& type) 
        : Component(n, i, p, q), capacity(cap >= 0 ? cap : 0), batteryType(type) {}

    [[nodiscard]] int getCapacity() const { return capacity; }
    [[nodiscard]] std::string getBatteryType() const { return batteryType; }

    [[nodiscard]] std::string getType() const override { return "Battery"; }

    void display() const override {
        Component::display();
        std::cout << "  └─ [Specs] Capacity: " << capacity << " mAh | Chemistry: " << batteryType << std::endl;
    }

    [[nodiscard]] std::string toCSV() const override {
        return Component::toCSV() + "," + std::to_string(capacity) + "," + batteryType;
    }
};

#endif // BATTERY_HPP
