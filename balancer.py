from sympy import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Author: Jack Donofrio
# Date: January 5th 2019
#
# 7-24-2020:
# I just found this on my old computer. This was the project that started it all.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


def handle_species(species):
    elements = {}
    for i in range(len(species)):
        if species[i].isupper():
            if i == len(species) - 1: # if it's last
                if species[i] not in elements: 
                    elements[species[i]] = 1
                else:
                    elements[species[i]] = elements[species[i]] + 1
            else:
                if i + 2 <= len(species) - 1 and species[i + 1 : i + 3].isdigit():
                    if species[i] not in elements:
                        elements[species[i]] = int(species[i + 1 : i + 3])
                    else:
                        elements[species[i]] = int(species[i + 1 : i + 3]) + elements[species[i]]
                elif species[i + 1].isdigit():
                    if species[i] not in elements:
                        elements[species[i]] = int(species[i + 1])
                    else:
                        elements[species[i]] = int(species[i + 1]) + elements[species[i]]
                elif species[i + 1].islower(): # if you have Na for example
                    if i + 3 <= len(species) - 1 and species[i + 2 : i + 4].isdigit():
                        if species[i : i + 2] not in elements:
                            elements[species[i : i + 2]] = int(species[i + 2 : i + 4])
                        else:
                            elements[species[i : i + 2]] = int(species[i + 2 : i + 4]) + elements[species[i : i + 2]]
                    elif i + 1 == len(species) - 1 or species[i + 2].isalpha(): # means there's only one of Na
                        if species[i : i + 2] not in elements:
                            elements[species[i : i + 2]] = 1
                        else:
                            elements[species[i : i + 2]] = elements[species[i : i + 2]] + 1
                    elif i + 2 <= len(species) - 1 and species[i + 2].isdigit():
                        if species[i : i + 2] not in elements:
                            elements[species[i : i + 2]] = int(species[i + 2])
                        else:
                            elements[species[i : i + 2]] = int(species[i + 2]) + elements[species[i : i + 2]]
                else:
                    if species[i] not in elements:
                        elements[species[i]] = 1
                    else:
                        elements[species[i]] = 1 + elements[species[i]]           
    return elements


# Equations should be received in the form:
# C2H5OH + O2 -> CO2 + H2O
# or
# C2H5OH + O2 = CO2 + H2O
raw_eq = input("Enter equation: ")

def parse_equation(raw_eq):
    if '=' in raw_eq:
        equation = [x.strip() for x in raw_eq.split('=')]
    else:
        equation = [x.strip() for x in raw_eq.split('->')]

    reactants = [x.strip() for x in equation[0].split('+')]
    products = [x.strip() for x in equation[1].split('+')]
    
    return reactants, products

# print(parse_equation(raw_eq))
equation = parse_equation(raw_eq)

##################################
reactants = equation[0]
reactant_variable_names = ['x', 'y']

reactant_dict = {}
for i in range(len(reactants)):
    reactant_dict[reactant_variable_names[i]] = reactants[i]
# print(reactant_dict)


products = equation[1]

product_variable_names = ['a', 'b']
product_dict = {}
for i in range(len(products)):
    product_dict[product_variable_names[i]] = products[i]

# print(product_dict)
#######################################################

set_of_elements = set() # set holding all elements being handled in this reaction
for reactant in reactants:
    elements = handle_species(reactant).keys()
    for element in elements:
        set_of_elements.add(element)
# print(set_of_elements)

reactant_values = {} # holds each reacting element's coefficient * variable
product_values = {}

for element in set_of_elements:
    reactant_expressions_for_element = []
    product_expressions_for_element = []

    for reactant in reactant_dict:
        if element in reactant_dict[reactant]:
            species_data = handle_species(reactant_dict[reactant])
            reactant_expressions_for_element.append(f'{species_data[element]} * {reactant}')
            # print(f'{element} = {species_data[element]} * {reactant}')
    
    for product in product_dict:
        if element in product_dict[product]:
            species_data = handle_species(product_dict[product])
            product_expressions_for_element.append(f'{species_data[element]} * {product}')

    reactant_values[element] = reactant_expressions_for_element
    product_values[element] = product_expressions_for_element


# on each side, combine expressions relating to the same element across species.
for reactant in reactant_values:
    reactant_values[reactant] = ' + '.join(reactant_values[reactant])
for product in product_values:
    product_values[product] = ' + '.join(product_values[product])

# print(f'Reactants: {reactant_values}')
# print(f'Products: {product_values}')

##########################################################
final_expressions = set()

for element in set_of_elements:
    expression = f'{reactant_values[element]} - ({product_values[element]})'
    final_expressions.add(expression) 

# print(final_expressions)

x, y, a, b = symbols('x y a b')
results = solve(final_expressions, (x, y, a, b))
# print(results)
most_recently_added = b
for key in list(results):
    if results[key] == a or results[key] == y or results[key] == b:
        most_recently_added = results[key]
        results[results[key]] = 1
        results[key] = 1

# print(results)

for i in list(results):
    if str(most_recently_added) in str(results[i]):
        results[i] = str(results[i].replace(most_recently_added, 1))
results[most_recently_added] = 1
# print(results)

# # Euclid's algorithm
# def gcd(x, y):
#     if y == 0:
#         return x
#     return gcd(y, x % y)

# Find largest denominator, multiply all numbers by that
biggest = 1
for i in results.values():
    if '/' in str(i):
        num = int(i[-1])
        if num > biggest:
            biggest = num

# print("HERE",end=' ')
# print(results)

for i in results:
    if type(results[i]) == str:
        results[i] = eval(results[i])
    results[i] *= biggest

# t_gcd = gcd(results[x], gcd(results[y], gcd(results[a], results[b])))
# print(results)
# print(t_gcd)
# gcd_value = gcd(results[x], results[y])


print(f'{int(results[x])} {reactants[0]}', end='')
if y in results:
    print(f' + {int(results[y])} {reactants[1]}', end = ' -> ')
if a in results:
    print(f'{int(results[a])} {products[0]}', end='')
if b in results:
    print(f' + {int(results[b])} {products[1]}')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
