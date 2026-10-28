#ifndef CONVERTER_HPP
#define CONVERTER_HPP

#include "Component.hpp"

/**
 * @brief Derived Class: Converter
 * Specialization for DC-DC power regulation stages.
 */
class Converter : public Component {
private:
    double inputVoltage; 
    double outputVoltage;

public:
    Converter(const std::string& n, const std::string& i, double p, int q, double inputV, double outputV) 
        : Component(n, i, p, q), inputVoltage(inputV), outputVoltage(outputV) {}    

    [[nodiscard]] double getInputVoltage() const { return inputVoltage; }
    [[nodiscard]] double getOutputVoltage() const { return outputVoltage; }

    [[nodiscard]] std::string getType() const override { return "Converter"; }

    void display() const override {
        Component::display();
        std::cout << "  └─ [Specs] Vin: " << inputVoltage << "V | Vout: " << outputVoltage << "V" << std::endl;
    }

    [[nodiscard]] std::string toCSV() const override {
        return Component::toCSV() + "," + std::to_string(inputVoltage) + "," + std::to_string(outputVoltage);
    }
};

#endif // CONVERTER_HPP
