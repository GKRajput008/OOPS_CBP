#ifndef CONTROLLER_HPP
#define CONTROLLER_HPP

#include "Component.hpp"

/**
 * @brief Derived Class: Controller
 * Specialization for processing architectures, microcontrollers, and embedded computers.
 */
class Controller : public Component {
private:
    std::string controllerType; 
    int numPorts;

public:
    Controller(const std::string& n, const std::string& i, double p, int q, const std::string& type, int ports) 
        : Component(n, i, p, q), controllerType(type), numPorts(ports) {}

    [[nodiscard]] std::string getControllerType() const { return controllerType; }
    [[nodiscard]] int getNumPorts() const { return numPorts; }

    [[nodiscard]] std::string getType() const override { return "Controller"; }

    void display() const override {
        Component::display();
        std::cout << "  └─ [Specs] Architecture: " << controllerType << " | GPIO/Ports: " << numPorts << std::endl;
    }

    [[nodiscard]] std::string toCSV() const override {
        return Component::toCSV() + "," + controllerType + "," + std::to_string(numPorts);
    }
};

#endif // CONTROLLER_HPP
