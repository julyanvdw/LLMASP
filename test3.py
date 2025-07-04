from AspPy2 import ASPProgram, DataGenerator

p = ASPProgram()

# Add lines with labels for use in group NLs
alice = p.add_line(
    'person(^name^).',
    {'easy': '^name^ is a person'},
    {'easy': 'So we can defs say that ^name^ is a person'},
    label='^name^'
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
        'hard/3': 'HARD - There are 3 people: {1}, {2} and {3}.',
    }
)

p.add_variations({
    'name': ['Alice', 'Alex']
})


cnl_levels = {
    'easy': ['easy']
}

nl_levels = {
    'easy': ['easy'],
    'hard': ['hard'],
}

splice_params = {
    'strategy': 'chunk',
    'chunk_size': 3,  # Try different chunk sizes to see group NLs for subsets
    'randomised_order': False
}

dg = DataGenerator(p, splice_params=splice_params)
dg.generate_data(cnl_levels, nl_levels)
# dg.get_all_data()
dg.get_nl_cnl_data()
# dg.get_cnl_asp_data()
