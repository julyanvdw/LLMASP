from AspPy2 import ASPProgram, DataGenerator

p = ASPProgram()

# Program modelling with variations
p.add_line('^animal^(^name^)',
            {'easy': '^name^ is a ^animal^'},
            {'easy': 'So we can say that ^name^ is a ^animal^'},
            label='^name^'
          )

# Adding variations
v = {
    'animal': ['dog', 'cat', 'bird'],
    'name': ['Max', 'Luna', 'Charlie']
}

p.add_variations(v)

# Datagen Setup
cnl_levels = {
    'easy': ['easy'],    
}

nl_levels = {
    'easy': ['easy'],
}

dg = DataGenerator(p, splice_params='whole')
dg.generate_data(cnl_levels, nl_levels)
dg.get_all_data()
