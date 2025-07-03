from AspPy2 import ASPProgram, DataGenerator

p = ASPProgram()

p.add_line('^entity^(^name^).', 
           {
               'easy': '^name^ is a ^entity^', 
               'hard': 'It can be said that ^name^ is an ^entity^'
            })

v = {
    'entity' : ['human', 'person'],
    'name' : ['Alice', 'Bob'],
}

p.add_variations(v)

dg = DataGenerator(p)
dg.generate_data()

