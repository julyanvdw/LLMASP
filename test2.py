from AspPy import ASPProgram, DataGenerator

'''
Program to be modelled
node(1..3).
color("red").
color("green").
color("blue").
connected_to(1,X) :- node(1), node(X), X = 2.
connected_to(1,X) :- node(1), node(X), X = 3.
connected_to(2,X) :- node(2), node(X), X = 1.
connected_to(2,X) :- node(2), node(X), X = 3.
connected_to(3,X) :- node(3), node(X), X = 1.
connected_to(3,X) :- node(3), node(X), X = 2.
1 <= {assigned_to(ND_D,CLR_D): color(CLR_D)} <= 1 :- node(ND_D).
:- connected_to(X,Y), node(X), assigned_to(X,C), node(Y), assigned_to(Y,C), color(C).
'''

p = ASPProgram()

p.add_fact('node', ['1..3'], {'easy' : 'a node goes from 1 to 3'})
p.add_fact('color', ['red'], {'easy' : 'red is a color'})
p.add_fact('color', ['blue'], {'easy' : 'blue is a color'})
p.add_fact('color', ['green'], {'easy' : 'green is a color'})

p.add_rule(
    'connected_to', 
    ['1', 'X'],
    [
        ['node', ['1']],
        ['node', ['X']],
        ['X = 2', []]
    ],
    {'easy': 'node 1 is connected to node 2'}
)

p.add_cardinality_constraint(
    lower='1',
    upper='1',
    head_predicate='assigned_to',
    head_terms=['ND_D', 'CLR_D'],
    condition_predicate='color',
    condition_terms=['CLR_D'],
    apply_if_predicate='node',
    apply_if_terms=['ND_D'],
    cnl_map={'easy': 'each node is assigned exactly one color'}
)

p.add_constraint(
    body_literals=[
        ['connected_to', ['X', 'Y']],
        ['node', ['X']],
        ['assigned_to', ['X', 'C']],
        ['node', ['Y']],
        ['assigned_to', ['Y', 'C']],
        ['color', ['C']]
    ],
    cnl_map={'easy': 'no two connected nodes can have the same color'}
)





dg = DataGenerator(p, splice_params='whole', diffculty_levels=[['easy']])
dg.generate_data()



'''
#no group
p.add_line('color(red)', {red is a color})
p.add_line('color(blue)', {blue is a color})
p.add_line('color(green)', {green is a color})

#group option 1 - all or nothing
p.add_group([
        p.add_line('color(red)', {red is a color})
        p.add_line('color(blue)', {blue is a color})
        p.add_line('color(green)', {green is a color})
    ], 
    {'easy' : 'red, blue and green are colors'}
)

#group option 2
p.add_group([
        p.add_line('color(red)', {easy: 'red is a color'})
        p.add_line('color(blue)', {easy: 'blue is a color'})
        p.add_line('color(green)', {easy: 'green is a color'})
    ], 
    {'easy\3' : '{\1}, {\2} and {\3} are colors',
    'easy\2' : '{\1} and {\2} are colors'},
    'hard\3' : 'use {\1}, {\2} and {\3}
    }
)

#no group
node(A).
node(B).
node(C).

#group option 2
p.add_group([
    p.add_line('node(A)', {'easy': 'A is a node'}),
    p.add_line('node(B)', {'easy': 'B is a node'}),
    p.add_line('node(C)', {'easy': 'C is a node'}),
], {'easy\3' : '{\1}, {\2} and {\3} are nodes'}
)



'''


# # 1. Multi-granularity (default: sliding window)
# splice_params = {
#     'strategy': 'multi_granularity',
#     'min_size': 1,
#     'max_size': None,
#     'window_type': 'random',
#     'random_samples': 5,
#     'random_repeat_min': 2,      # Only repeat if k >= 2
#     'random_repeat_cutoff': 10,   # Only repeat if k < 6
#     'randomised_order': True  # <-- randomise the order of program lines before splicing
# }
# dg = DataGenerator(p, splice_params=splice_params)
# dg.generate_data()
# dg.test_print()

# 2. Single line splices
# splice_params = 'single'
# dg = DataGenerator(p, splice_params=splice_params)
# dg.generate_data()
# dg.test_print()

# 3. Fixed-size chunking (e.g., chunks of 2 lines)
# splice_params = {
#     'strategy': 'chunk',
#     'chunk_size': 2,
#     'randomised_order': True
# }
# dg = DataGenerator(p, splice_params=splice_params)
# dg.generate_data()
# dg.test_print()

# 4. Random sampling (e.g., 3 lines per splice, 4 samples)
# splice_params = {
#     'strategy': 'random',
#     'random_k': 3,
#     'random_samples': 4
# }
# dg = DataGenerator(p, splice_params=splice_params)
# dg.generate_data()
# dg.test_print()

# 5. Whole program as a single splice
# splice_params = {
#     'strategy': 'whole',
#     'randomised_order': True
# }
# dg = DataGenerator(p, splice_params=splice_params)
# dg.generate_data()
# dg.test_print()



