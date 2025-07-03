from AspPy2 import ASPProgram, DataGenerator

p = ASPProgram()

p.add_line('person(Alice).')

dg = DataGenerator(p)
dg.generate_data()

