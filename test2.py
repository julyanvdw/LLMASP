from AspPy import ASPProgram, DataGenerator


# first program
p = ASPProgram()

variations = {
    'name': ['node', 'vertex'],
    'ranges': ['1..3', '1..5']
}

p.add_variations(variations)

p.add_fact('{name}', ['{ranges}'])

# second program
p2 = ASPProgram()

variations = {
    'name': ['Alice', 'Bob', 'John']
}

p2.add_fact('person', ['{name}'])
p2.add_variations(variations)


# Set up the generator

dataGen = DataGenerator()
dataGen.add_program(p)
dataGen.add_program(p2)

dataGen.generate_data()

