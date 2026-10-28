#ifndef SENSOR_HPP
#define SENSOR_HPP

#include "Component.hpp"

/**
 * @brief Derived Class: Sensor
 * Specialization for environmental & perceptual transducers with sensor category and range.
 */
class Sensor : public Component {
private:
    std::string sensorType; 
    double range;

public:
    Sensor(const std::string& n, const std::string& i, double p, int q, const std::string& type, double r) 
        : Component(n, i, p, q), sensorType(type), range(r >= 0.0 ? r : 0.0) {}

    [[nodiscard]] std::string getSensorType() const { return sensorType; }
    [[nodiscard]] double getRange() const { return range; }

    [[nodiscard]] std::string getType() const override { return "Sensor"; }

    void display() const override {
        Component::display();
        std::cout << "  └─ [Specs] Category: " << sensorType << " | Range: " << range << " m" << std::endl;
    }   

    [[nodiscard]] std::string toCSV() const override {
        return Component::toCSV() + "," + sensorType + "," + std::to_string(range);
    }
};

#endif // SENSOR_HPP
