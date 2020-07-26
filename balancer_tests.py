from balancer_updated import Balancer

bl = Balancer()

def species_tests():
    species_a = 'KHCO3'
    species_b = 'C2H5OH'
    species_c = 'Ca(OH)2'
    species_d = 'PtCl2(NH3)2'
    species_e = 'Fe(H2O)4(OH)2'
 
    assert bl.handle_species(species_a) == {'K' : 1, 'H' : 1, 'C' : 1, 'O' : 3}
    assert bl.handle_species(species_b) == {'C' : 2, 'H' : 6, 'O' : 1}
    assert bl.handle_species(species_c) == {'Ca' : 1, 'O' : 2, 'H' : 2}
    assert bl.handle_species(species_d) == {'Pt' : 1, 'Cl' : 2, 'N' : 2, 'H' : 6}
    assert bl.handle_species(species_e) == {'Fe' : 1, 'H' : 10, 'O' : 6}


def two_two_tests():
    rxn_a = 'Br2 + KI -> KBr + I2'
    rxn_b = 'Mg + HCl -> MgCl2 + H2'
    rxn_c = 'C2H5OH + O2 -> CO2 + H2O'

    # parser tests
    assert bl.parse_equation(rxn_a) == (['Br2', 'KI'], ['KBr', 'I2'])
    assert bl.parse_equation(rxn_b) == (['Mg', 'HCl'], ['MgCl2', 'H2'])
    assert bl.parse_equation(rxn_c) == (['C2H5OH', 'O2'], ['CO2', 'H2O'])

    # balancer tests
    assert bl.balance_equation(rxn_a) == '1 Br2 + 2 KI -> 2 KBr + 1 I2'
    assert bl.balance_equation(rxn_b) == '1 Mg + 2 HCl -> 1 MgCl2 + 1 H2'
    assert bl.balance_equation(rxn_c) == '1 C2H5OH + 3 O2 -> 2 CO2 + 3 H2O'

def one_two_tests():
    rxn_a = 'CuCl2 -> Cu + Cl'
    rxn_b = 'Mg3(SO4)2 -> Mg + SO4'

    # parser tests
    assert bl.parse_equation(rxn_a) == (['CuCl2'], ['Cu', 'Cl'])
    assert bl.parse_equation(rxn_b) == (['Mg3(SO4)2'], ['Mg', 'SO4'])

    # balancer tests
    assert bl.balance_equation(rxn_a) == '1 CuCl2 -> 1 Cu + 2 Cl'
    assert bl.balance_equation(rxn_b) == '1 Mg3(SO4)2 -> 3 Mg + 2 SO4'

def two_one_tests():
    rxn_a = 'Cu + Cl -> CuCl2'
    rxn_b = 'Fe + Cl2 -> FeCl3'

    assert bl.parse_equation(rxn_a) == (['Cu', 'Cl'], ['CuCl2'])
    assert bl.parse_equation(rxn_b) == (['Fe', 'Cl2'], ['FeCl3'])

    assert bl.balance_equation(rxn_a) == '1 Cu + 2 Cl -> 1 CuCl2'
    assert bl.balance_equation(rxn_b) == '2 Fe + 3 Cl2 -> 2 FeCl2'

def three_one_tests():
    rxn_a = 'K2CO3 + H2O + CO2 -> KHCO3'
    
    # parser tests
    assert bl.parse_equation(rxn_a) == (['K2CO3', 'H2O', 'CO2'], ['KHCO3'])

    # balancer tests
    assert bl.balance_equation(rxn_a) == '1 K2CO3 + 1 H2O + 1 CO2 -> 2 KHCO3'

def one_three_tests():
    rxn_a = 'KHCO3 -> K2CO3 + H2O + CO2'

    # parser tests
    assert bl.parse_equation(rxn_a) == (['KHCO3'], ['K2CO3', 'H2O', 'CO2'])

    # balancer tests
    assert bl.balance_equation(rxn_a) == '2 KHCO3 -> 1 K2CO3 + 1 H2O + 1 CO2'

def two_three_tests():
    rxn_a = 'HCl + MgCO3 -> MgCl2 + CO2 + H2O'
    
    # parser tests
    assert bl.parse_equation(rxn_a) == (['HCl', 'MgCO3'], ['MgCl2', 'CO2', 'H2O'])

    # balancer tests
    assert bl.balance_equation(rxn_a) == '2 HCl + 1 MgCO3 -> 1 MgCl2 + 1 CO2 + 1 H2O'

species_tests()
two_three_tests()
one_three_tests()
three_one_tests()
one_two_tests()
two_two_tests()