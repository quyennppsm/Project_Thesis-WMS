import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Define the input and output variables
value = ctrl.Antecedent(np.arange(0, 101, 1), 'value')
cost = ctrl.Antecedent(np.arange(0, 11, 1), 'cost')
benefit = ctrl.Antecedent(np.arange(0, 1001, 1), 'benefit')
demand = ctrl.Antecedent(np.arange(0, 1001, 1), 'demand')
frequency = ctrl.Antecedent(np.arange(0, 101, 1), 'frequency')

output = ctrl.Consequent(np.arange(0, 61, 1), 'output')

# Define the membership functions for the input variables
value['a'] = fuzz.trapmf(value.universe, [0, 0, 10, 20])
value['b'] = fuzz.trimf(value.universe, [10, 20, 30])
value['c'] = fuzz.trapmf(value.universe, [20, 30, 100, 100])

cost['a'] = fuzz.trapmf(cost.universe, [0, 0, 1, 2])
cost['b'] = fuzz.trimf(cost.universe, [1, 2, 3])
cost['c'] = fuzz.trapmf(cost.universe, [2, 3, 10, 10])

benefit['a'] = fuzz.trapmf(benefit.universe, [0, 0, 50, 100])
benefit['b'] = fuzz.trimf(benefit.universe, [50, 100, 150])
benefit['c'] = fuzz.trapmf(benefit.universe, [100, 150, 1000, 1000])

demand['a'] = fuzz.trapmf(demand.universe, [0, 0, 100, 200])
demand['b'] = fuzz.trimf(demand.universe, [100, 200, 300])
demand['c'] = fuzz.trapmf(demand.universe, [200, 300, 1000, 1000])

frequency['a'] = fuzz.trapmf(frequency.universe, [0, 0, 10, 20])
frequency['b'] = fuzz.trimf(frequency.universe, [10, 20, 30])
frequency['c'] = fuzz.trapmf(frequency.universe, [20, 30, 100, 100])

# Define the membership functions for the output variables
output['max_param'] = fuzz.trimf(output.universe, [0, 10, 20])
output['a_param'] = fuzz.trimf(output.universe, [10, 20, 30])
output['b_param'] = fuzz.trimf(output.universe, [20, 30, 40])
output['c_param'] = fuzz.trimf(output.universe, [30, 40, 50])
output['min_param'] = fuzz.trimf(output.universe, [40, 50, 60])

# Define the rules for the fuzzy controller
rule1 = ctrl.Rule(value['a'] & cost['a'] & benefit['a'] & demand['a'] & frequency['a'], output['max_param'])
rule2 = ctrl.Rule(value['b'] & cost['b'] & benefit['b'] & demand['b'] & frequency['b'], output['a_param'])
rule3 = ctrl.Rule(value['c'] & cost['c'] & benefit['c'] & demand['c'] & frequency['c'], output['b_param'])
rule4 = ctrl.Rule(value['b'] & cost['c'] & benefit['c'] & demand['c'] & frequency['c'], output['c_param'])
rule5 = ctrl.Rule(value['c'] & cost['c'] & benefit['c'] & demand['c'] & frequency['c'], output['min_param'])

# Create the control system and simulate the fuzzy controller
fuzzy_system = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
simulation = ctrl.ControlSystemSimulation(fuzzy_system)
simulation.input['value'] = 15  # Example input values
simulation.input['cost'] = 2.5
simulation.input['benefit'] = 75
simulation.input['demand'] = 150
simulation.input['frequency'] = 25
simulation.compute()

# Print the output parameters of the fuzzy controller
print('max_param:', simulation.output['max_param'])
print('a_param:', simulation.output['a_param'])
print('b_param:', simulation.output['b_param'])