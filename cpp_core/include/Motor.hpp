#ifndef MOTOR_HPP
#define MOTOR_HPP

#include "Component.hpp"

/**
 * @brief Derived Class: Motor
 * Specialization for electric actuators with operating voltage and RPM specifications.
 */
class Motor : public Component {
private:
    int operatingVoltage; 
    int rpm;

public:
    Motor(const std::string& n, const std::string& i, double p, int q, int voltage, int r) 
        : Component(n, i, p, q), operatingVoltage(voltage), rpm(r) {}

    [[nodiscard]] int getVoltage() const { return operatingVoltage; }
    [[nodiscard]] int getRpm() const { return rpm; }

    [[nodiscard]] std::string getType() const override { return "Motor"; }

    void display() const override {
        Component::display();
        std::cout << "  └─ [Specs] Voltage: " << operatingVoltage << "V | Max RPM: " << rpm << std::endl;
    }

    [[nodiscard]] std::string toCSV() const override {
        return Component::toCSV() + "," + std::to_string(operatingVoltage) + "," + std::to_string(rpm);
    }
};

#endif // MOTOR_HPP
