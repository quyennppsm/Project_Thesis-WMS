#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <fuzzylite/FuzzyLite.h>

using namespace fl;

// Define the membership functions for the input variables
void define_input_variables(Engine* engine) {
    // Define the membership function for the total_despatched variable
    InputVariable* total_despatched = new InputVariable;
    total_despatched->setName("total_despatched");
    total_despatched->setRange(0, 2000);
    total_despatched->addTerm(new Ramp("LOW", -1.0, 0.0));
    total_despatched->addTerm(new Ramp("MEDIUM", 0.0, 1.0));
    total_despatched->addTerm(new Ramp("HIGH", 1.0, 2.0));
    engine->addInputVariable(total_despatched);

    // Define the membership function for the total_age variable
    InputVariable* total_age = new InputVariable;
    total_age->setName("total_age");
    total_age->setRange(0, 1000000000000000);
    total_age->addTerm(new Ramp("LOW", -1.0, 0.0));
    total_age->addTerm(new Ramp("MEDIUM", 0.0, 1.0));
    total_age->addTerm(new Ramp("HIGH", 1.0, 2.0));
    engine->addInputVariable(total_age);

    // Define the membership function for the total_cost variable
    InputVariable* total_cost = new InputVariable;
    total_cost->setName("total_cost");
    total_cost->setRange(0, 20000000);
    total_cost->addTerm(new Ramp("LOW", -1.0, 0.0));
    total_cost->addTerm(new Ramp("MEDIUM", 0.0, 1.0));
    total_cost->addTerm(new Ramp("HIGH", 1.0, 2.0));
    engine->addInputVariable(total_cost);

    // Define the membership function for the total_wage variable
    InputVariable* total_wage = new InputVariable;
    total_wage->setName("total_wage");
    total_wage->setRange(0, 40000000);
    total_wage->addTerm(new Ramp("LOW", -1.0, 0.0));
    total_wage->addTerm(new Ramp("MEDIUM", 0.0, 1.0));
    total_wage->addTerm(new Ramp("HIGH", 1.0, 2.0));
    engine->addInputVariable(total_wage);

    // Define the membership function for the demand variable
    InputVariable* demand = new InputVariable;
    demand->setName("demand");
    demand->setRange(0, 10);
    demand->addTerm(new Ramp("LOW", -1.0, 0.0));
    demand->addTerm(new Ramp("MEDIUM", 0.0, 1.0));
    demand->addTerm(new Ramp("HIGH", 1.0, 2.0));
    engine->addInputVariable(demand);

    // Define the membership function for the flow variable
    InputVariable* flow = new InputVariable;
    flow->setName("flow");
    flow->setRange(0, 20);
    flow->addTerm(new Ramp("LOW", -1.0, 0.0));
    flow->addTerm(new Ramp("MEDIUM", 0.0, 1.0));
    flow->addTerm(new Ramp("HIGH", 1.0, 2.0));
    engine->addInputVariable(flow);

    // Define the membership function for the total_order variable
    InputVariable* total_order = new InputVariable;
    total_order->setName("total_order");
    total_order->setRange(0, 200);
    total_order->addTerm(new Ramp("LOW", -1.0, 0.0));
    total_order->addTerm(new Ramp("MEDIUM", 0.0, 1.0));
    total_order->addTerm(new Ramp("HIGH", 1.0, 2.0));
    engine->addInputVariable(total_order);
}

// Define the membership functions for the output variable
void define_output_variable(Engine* engine) {
    // Define the membership function for the fuzzy variable
    OutputVariable* fuzzy = new OutputVariable;
    fuzzy->setName("fuzzy");
    fuzzy->setRange(0, 100);
    fuzzy->setAggregation(new Maximum);
    fuzzy->setDefuzzifier(new Centroid(100));
    fuzzy->setDefaultValue(fl::nan);
    fuzzy->setLockPreviousValue(false);
    fuzzy->addTerm(new Ramp("LOW", 0.0, 20.0));
    fuzzy->addTerm(new Ramp("MEDIUM", 20.0, 40.0));
    fuzzy->addTerm(new Ramp("HIGH", 40.0, 60.0));
    fuzzy->addTerm(new Ramp("VERY_HIGH", 60.0, 100.0));
    engine->addOutputVariable(fuzzy);
}

// Define the fuzzy rules
void define_rules(Engine* engine) {
    // Define the fuzzy rule for LOW total_despatched, LOW total_age, and LOW total_cost
    RuleBlock* ruleblock1 = new RuleBlock;
    ruleblock1->addRule(Rule::parse("if total_despatched is LOW and total_age is LOW and total_cost is LOW then fuzzy is LOW", engine));
    engine->addRuleBlock(ruleblock1);

    // Define the fuzzy rule for HIGH total_wage and LOW demand
    RuleBlock* ruleblock2 = new RuleBlock;
    ruleblock2->addRule(Rule::parse("if total_wage is HIGH and demand is LOW then fuzzy is MEDIUM", engine));
    engine->addRuleBlock(ruleblock2);

    // Define the fuzzy rule for MEDIUM flow and MEDIUM total_order
    RuleBlock* ruleblock3 = new RuleBlock;
    ruleblock3->addRule(Rule::parse("if flow is MEDIUM and total_order is MEDIUM then fuzzy is HIGH", engine));
    engine->addRuleBlock(ruleblock3);
}

// Calculate the fuzzy value for a given row of data
double calculate_fuzzy_value(const std::vector<double>& data, Engine* engine) {
    // Set the input values
    engine->getInputVariable("total_despatched")->setValue(data[2]);
    engine->getInputVariable("total_age")->setValue(data[3]);
    engine->getInputVariable("total_cost")->setValue(data[4]);
    engine->getInputVariable("total_wage")->setValue(data[5]);
    engine->getInputVariable("demand")->setValue(data[6]);
    engine->getInputVariable("flow")->setValue(data[7]);
    engine->getInputVariable("total_order")->setValue(data[8]);

    // Calculate the output value
    engine->process();

    // Return the fuzzy value
    return engine->getOutputVariable("fuzzy")->getValue();
}

int main() {
    // Load the CSV file
    std::ifstream infile("input.csv");
    std::string line;
    std::vector<std::vector<double>> data;
    while (std::getline(infile, line)) {
        std::stringstream ss(line);
        std::vector<double> row;
        double value;
        char delimiter;
        while (ss >> value) {
            row.push_back(value);
            ss >> delimiter;
        }
        data.push_back(row);
    }

    // Create the fuzzy logic engine
    Engine* engine = new Engine;
    engine->setName("fuzzy_controller");
    engine->setDescription("");

    // Define the input and output variables
    define_input_variables(engine);
    define_output_variable(engine);

    // Define the fuzzy rules
    define_rules(engine);

    // Calculate the fuzzy values for each row of data
    std::vector<double> fuzzy_values;
    for (const auto& row : data) {
        double fuzzy_value = calculate_fuzzy_value(row, engine);
        fuzzy_values.push_back(fuzzy_value);
    }

    // Normalize the fuzzy values so that their sum is less than or equal to 16800
    double sum = 0;
    for (const auto& fuzzy_value : fuzzy_values) {
        sum += fuzzy_value;
    }
    double factor = 1.0;
    if (sum > 16800) {
        factor = 16800 / sum;
    }

    // Write the output CSV file
    std::ofstream outfile("output.csv");
    outfile << "id,product,fuzzy\n";
    for (int i = 0; i < data.size(); ++i) {
        double fuzzy_value = fuzzy_values[i] * factor;
        outfile << data[i][0] << "," << data[i][1] << "," << fuzzy_value << "\n";
    }

    return 0;
}