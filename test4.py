from AspPy2 import ASPProgram, DataGenerator

p = ASPProgram()

# Program Modelling

p.add_line(
    '^object^(^name^).',
    {
        'easy': '^name^ is a ^object^',
        'med': 'A ^object^ is called ^name^',
        'hard': '^object^: ^name^',
    },
    {
        'easy': 'So we can defs say that ^name^ is a ^object^'
    },
    label='^name^'
)

v = {
    'object' : ['car', 'book', 'table', 'computer', 'phone', 'building', 'tree', 'rock', 'bottle', 'person', 'dog', 'cat', 'parrot', 'chair', 'lamp', 'window', 'door', 'bicycle', 'guitar', 'piano', 'camera', 'watch', 'pen', 'pencil', 'notebook', 'backpack', 'shoe', 'hat', 'flower', 'bird', 'fish', 'horse', 'elephant', 'lion', 'tiger', 'bear', 'rabbit', 'mouse', 'snake', 'turtle'],
    'name' : ['Alex', 'Bob', 'Charlie', 'Diana', 'Echo', 'Jane', 'Mary', 'Matthew', 'Rob', 'Sarah', 'Tom', 'Lisa', 'Mike', 'Emma', 'John', 'Kate', 'David', 'Anna', 'Peter', 'Lucy', 'Sam', 'Nina', 'Jack', 'Zoe', 'Ben', 'Mia', 'Leo', 'Ivy', 'Max', 'Eva', 'Ryan', 'Chloe', 'Adam', 'Grace', 'Owen', 'Lily', 'Noah', 'Ella', 'Luke', 'Ava']
}

p.add_variations(v)

# Data generator

cnl_levels = {
    'easy': ['easy', 'med', 'hard']
}

nl_levels = {
    'easy': ['easy'],
}

dg = DataGenerator(p, splice_params='single')
dg.generate_data(cnl_levels, nl_levels)
# dg.get_all_data()
# dg.get_nl_cnl_data()
# dg.get_cnl_asp_data()
dg.export_cnl_asp_instruction_jsonl("raw.jsonl", 'Translate this to ASP code')
# dg.export_nl_cnl_instruction_jsonl("test.jsonl", 'Translate this to simpler statements')