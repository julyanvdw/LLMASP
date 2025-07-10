from AspPy2 import ASPProgram, DataGenerator

p = ASPProgram()

# Add lines with labels for use in group NLs
alice = p.add_line(
    'person(Alex).',
    {'easy': 'Alex is a person'},
    {'easy': 'So we can defs say that Alex is a person'},
    label='Alex'
)
bob = p.add_line(
    'person(Bob).',
    {'easy': 'Bob is a person'},
    {'easy': 'So we can defs say that Bob is a person'},
    label='Bob'
)
jane = p.add_line( 
    'person(Jane).',
    {'easy': 'Jane is a person'},
    {'easy': 'So we can defs say that Jane is a person'},
    label='Jane'
)

p.add_group(
    [alice, bob, jane],
    {
        'easy/3': 'There are 3 people: {1}, {2} and {3}.',
        'easy/2': '{1} and {2} are people.',
    }
)

p.add_line(
    'connected_to(1,X) :- node(1), node(X), X = 2.',
    {'easy' : 'node 1 is connected to node 2'},
    {'easy' : 'nodes 1 and 2 are connected'}
)


cnl_levels = {
    'easy': ['easy']
}

nl_levels = {
    'easy': ['easy'],
}

dg = DataGenerator(p, splice_params='single')
dg.generate_data(cnl_levels, nl_levels)
# dg.get_all_data()
# dg.get_nl_cnl_data()
# dg.get_cnl_asp_data()
dg.export_cnl_asp_instruction_jsonl("test.jsonl", 'Translate this to ASP code')
# dg.export_nl_cnl_instruction_jsonl("test.jsonl", 'Translate this to simpler statements')