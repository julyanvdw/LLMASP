from AspPy2 import ASPProgram, DataGenerator

p = ASPProgram()

p.add_group([
        p.add_line(
            '^entity^(Alice).',
            {
                'easy': 'Alice is a ^entity^'
            },
            {
                'easy': 'So we can defs say that Alice is a ^entity^'
            }
        ),

        p.add_line(
            '^entity^(Bob).',
            {
                'easy': 'Bob is a ^entity^'
            },
            {
                'easy': 'So we can defs say that Bob is a ^entity^'
            }
        ),

        p.add_line(
            '^entity^(Jane).',
            {
                'easy': 'Jane is a ^entity^'
            },
            {
                'easy': 'So we can defs say that Jane is a ^entity^'
            }
        )
    ],
    {
        'easy' : 'Alice, Bob and Jane are people',
    }
)

p.add_variations({
    'entity' : ['human', 'person'],
})



cnl_levels = {
    'easy': ['easy']
}

nl_levels = {
    'easy': ['easy'],
}


splice_params = {
    'strategy': 'chunk',
    'chunk_size': 3,
    'randomised_order': False
}


dg = DataGenerator(p, splice_params=splice_params)
dg.generate_data(cnl_levels, nl_levels)


