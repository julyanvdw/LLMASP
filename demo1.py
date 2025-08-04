from AspPy2 import ASPProgram, DataGenerator

p = ASPProgram()

# Program modelling

p.add_line('person(Jane).',
            {'easy': 'Jane is a person'},
            {'easy': 'So we can say that Jane is a person'},
            label='Jane'
          )

# p.add_line('person(Bob)',
#             {'easy': 'Bob is a person'},
#             {'easy': 'So we can say that Bob is a person'},
#             label='Bob'
#           )

# p.add_line('dog(Rover)',
#             {'easy': 'Rover is a dog'},
#             {'easy': 'So we can say that Rover is a dog'},
#             label='Rover'
#           )


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