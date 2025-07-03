from AspPy2 import ASPProgram, DataGenerator

p = ASPProgram()
p.add_line('person(Alice).', 
           {
            'easy' : 'Alice is a person',
            },
           {
            'easy' : 'EASY - In this example, Alice is a person',
            }
        )



cnl_levels = {
    'easy': ['easy']
}

nl_levels = {
    'easy': ['easy'],
}



dg = DataGenerator(p)
dg.generate_data(cnl_levels, nl_levels)

