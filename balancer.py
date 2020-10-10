from sympy import *
import json

# ~ Updated Version ~
#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~!#
# Title: Chemical Equation Balancer
# Author: Jack Donofrio
# Creation Date: January 5th 2019
# 
# Updated July 29 2020
# Version: 1.0.3
#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~!#

class SpeciesHandler:
    def add_to_dict(self, dict, item_to_add, value):
        dict[item_to_add] = value if item_to_add not in dict else value + dict[item_to_add]

    def get_species_data(self, species):
        elements = {}
        for i in range(len(species)):
            if species[i] == '(': 
                value_enclosed = species[i + 1 : species[i+1:].index(')') + i + 1]
                elements_in_parentheses = self.get_species_data(value_enclosed)
                i = species[i+1:].index(')') + i + 1
                if i + 1 < len(species) and species[i+1].isdigit():
                    subscript = int(species[i+1])
                    for element in elements_in_parentheses:
                        self.add_to_dict(elements, element, (elements_in_parentheses[element] * subscript) - elements_in_parentheses[element])
            elif species[i].isupper():
                if i == len(species) - 1: 
                    self.add_to_dict(elements, species[i], 1)
                else:
                    if i + 2 <= len(species) - 1 and species[i + 1 : i + 3].isdigit():
                        self.add_to_dict(elements, species[i], int(species[i + 1 : i + 3]))
                    elif species[i + 1].isdigit():
                        self.add_to_dict(elements, species[i], int(species[i + 1]))
                    elif species[i + 1].islower(): 
                        if i + 3 <= len(species) - 1 and species[i + 2 : i + 4].isdigit():
                            self.add_to_dict(elements, species[i : i + 2], int(species[i + 2 : i + 4]))
                        elif i + 1 == len(species) - 1 or species[i + 2].isalpha() or species[i + 2] == '(': 
                            self.add_to_dict(elements, species[i : i + 2], 1)
                        elif i + 2 <= len(species) - 1 and species[i + 2].isdigit():
                            self.add_to_dict(elements, species[i : i + 2], int(species[i + 2]))
                    else:
                        self.add_to_dict(elements, species[i], 1)
        return elements
    
    def get_molar_mass(self, species):
        molar_masses = json.load(open('molarmasses.json'))
        species_data = self.get_species_data(species)
        molar_mass = sum([species_data[element] * molar_masses[element] for element in species_data])
        return round(molar_mass,3)

class Balancer:

    # Equations should be received in the form:
    # C2H5OH + O2 -> CO2 + H2O
    # or
    # C2H5OH + O2 = CO2 + H2O

    def parse_equation(self, raw_equation: str):
        if '=' in raw_equation:
            equation = [x.strip() for x in raw_equation.split('=')]
        else:
            equation = [x.strip() for x in raw_equation.split('->')]
        reactants = [x.strip() for x in equation[0].split('+')]
        products = [x.strip() for x in equation[1].split('+')]
        return reactants, products
    
    def balance_equation(self, raw_equation: str):
        reactants, products = self.parse_equation(raw_equation)
        
        reactant_variable_names = ['x', 'y', 'z']
        reactant_dict = {reactant_variable_names[i] : reactants[i] for i in range(len(reactants))}
        
        product_variable_names = ['a', 'b', 'c']
        product_dict = {product_variable_names[i] : products[i] for i in range(len(products))}

        set_of_elements = set()
        for reactant in reactants:
            elements = SpeciesHandler().get_species_data(reactant).keys()
            for element in elements:
                set_of_elements.add(element)
        
        reactant_expressions, product_expressions = {},{}

        for element in set_of_elements:
            reactant_expressions_for_element = []
            product_expressions_for_element = []

            for reactant in reactant_dict:
                if element in reactant_dict[reactant]:
                    species_data = SpeciesHandler().get_species_data(reactant_dict[reactant])
                    if element in species_data:
                        reactant_expressions_for_element.append(f'{species_data[element]} * {reactant}')
            
            for product in product_dict:
                if element in product_dict[product]:
                    species_data = SpeciesHandler().get_species_data(product_dict[product])
                    if element in species_data:
                        product_expressions_for_element.append(f'{species_data[element]} * {product}')
            
            reactant_expressions[element] = reactant_expressions_for_element
            product_expressions[element] = product_expressions_for_element
        
        for reactant in reactant_expressions:
            reactant_expressions[reactant] = ' + '.join(reactant_expressions[reactant])
        for product in product_expressions:
            product_expressions[product] = ' + '.join(product_expressions[product])
        
        final_expressions = set([f'{reactant_expressions[element]} - ({product_expressions[element]})' for element in set_of_elements])
        
        x, y, z, a, b, c = symbols('x y z a b c')
        results = solve(final_expressions, (x, y, z, a, b, c))

        for key in list(results):
            value = str(results[key])
            for ch in value:
                if ch.isalpha():
                    results[key] = parse_expr(value.replace(ch, '1'))
                    results[symbols(ch)] = 1

        # Find largest denominator, multiply all numbers by that
        greatest_denominator = 1

        for i in results.values():
            if '/' in str(i):
                denominator = int(str(i)[-1])
                if denominator > greatest_denominator:
                    greatest_denominator = denominator

        for i in results:
            if type(results[i]) == str:
                results[i] = eval(results[i])
            results[i] *= greatest_denominator

        balanced_equation = f'{int(results[x])} {reactants[0]}'
        if y in results:
            balanced_equation += f' + {int(results[y])} {reactants[1]}'
        if z in results:
            balanced_equation += f' + {int(results[z])} {reactants[2]}'
        balanced_equation += ' -> '
        if a in results:
            balanced_equation += f'{int(results[a])} {products[0]}'
        if b in results:
            balanced_equation += f' + {int(results[b])} {products[1]}'
        if c in results:
            balanced_equation += f' + {int(results[c])} {products[2]}'
        
        return balanced_equation

#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~!#

if __name__ == '__main__':
    print(Balancer().balance_equation(input('> Enter a Chemical Equation: ')))
