from AspPy2 import ASPProgram, DataGenerator

"""
node(1..3).
color("red").
color("green").
color("blue").
^connected_to^(1,X) :- node(1), node(X), X = 2.
^connected_to^(1,X) :- node(1), node(X), X = 3.
^connected_to^(2,X) :- node(2), node(X), X = 1.
^connected_to^(2,X) :- node(2), node(X), X = 3.
^connected_to^(3,X) :- node(3), node(X), X = 1.
^connected_to^(3,X) :- node(3), node(X), X = 2.
1 <= {assigned_to(ND_D,CLR_D): color(CLR_D)} <= 1 :- node(ND_D).
:- ^connected_to^(X,Y), node(X), assigned_to(X,C), node(Y), assigned_to(Y,C), color(C).
"""

# Models line by line - NO GROUPS bc this only cares about CNL:ASP mappings

p = ASPProgram()

# Problem modelling:
p.add_line(
        "^node^(1..^node_count^).",
        {
            'level1': "A ^node^ goes from 1..^node_count^",
            'level2': "There are ^node^s 1..^node_count^",
            'level3': "There are ^node_count^ ^node^s",
        },
        {
            'level1': "There are ^node_count^ ^node^s"
        }, 
        label="^node^"
    )

p.add_line(
        '^colourName^("^colour1^").',
        {
            'level1': "^colour1^ is a ^colourName^",
            'level2': "The ^colourName^ ^colour1^ exists",
            'level3': "Out of the ^colourName^ available, there is ^colour1^",
        },
        {
            'level1': "^colour1^ is a ^colourName^"
        }, 
        label="^colourName^"
    )

p.add_line(
        '^colourName^("^colour2^").',
        {
            'level1': "^colour2^ is a ^colourName^",
            'level2': "The ^colourName^ ^colour2^ exists",
            'level3': "Out of the ^colourName^s available, there is ^colour2^",
        },
        {
            'level1': "^colour2^ is a ^colourName^"
        }, 
        label="^colourName^"
    )

p.add_line(
        '^colourName^("^colour3^").',
        {
            'level1': "^colour3^ is a ^colourName^",
            'level2': "The ^colourName^ ^colour3^ exists",
            'level3': "Out of the ^colourName^s available, there is ^colour3^",
        },
        {
            'level1': "^colour3^ is a ^colourName^"
        }, 
        label="^colourName^"
    )

p.add_line(
        '^connected_to^(1,^X^) :- ^node^(1), ^node^(^X^), ^X^ = 2.',
        {
            'level1': "^node^ 1 and ^node^ 2 are connected",
            'level2': "^node^s 1 and 2 are connected",
            'level3': "There is a connection between ^node^ 1 and ^node^ ^X^ where ^X^ is 2",
        },
        {
            'level1': "^node^s 1 and 2 are connected"
        }, 
        label="^node^"
    )

p.add_line(
        '^connected_to^(1,^X^) :- ^node^(1), ^node^(^X^), ^X^ = 3.',
        {
            'level1': "^node^ 1 and ^node^ 3 are connected",
            'level2': "^node^s 1 and 3 are connected",
            'level3': "There is a connection between ^node^ 1 and ^node^ ^X^ where ^X^ is 3",
        },
        {
            'level1': "^node^s 1 and 3 are connected"
        }, 
        label="^node^"
    )

p.add_line(
        '^connected_to^(2,^X^) :- ^node^(2), ^node^(^X^), ^X^ = 1.',
        {
            'level1': "^node^ 2 and ^node^ 1 are connected",
            'level2': "^node^s 2 and 1 are connected",
            'level3': "There is a connection between ^node^ 2 and ^node^ ^X^ where ^X^ is 1",
        },
        {
            'level1': "^node^s 2 and 1 are connected"
        }, 
        label="^node^"
    )

p.add_line(
        '^connected_to^(2,^X^) :- ^node^(2), ^node^(^X^), ^X^ = 3.',
        {
            'level1': "^node^ 2 and ^node^ 3 are connected",
            'level2': "^node^s 2 and 3 are connected",
            'level3': "There is a connection between ^node^ 2 and ^node^ ^X^ where ^X^ is 3",
        },
        {
            'level1': "^node^s 2 and 3 are connected"
        }, 
        label="^node^"
    )

p.add_line(
        '^connected_to^(3,^X^) :- ^node^(3), ^node^(^X^), ^X^ = 1.',
        {
            'level1': "^node^ 3 and ^node^ 1 are connected",
            'level2': "^node^s 3 and 1 are connected",
            'level3': "There is a connection between ^node^ 3 and ^node^ ^X^ where ^X^ is 1",
        },
        {
            'level1': "^node^s 3 and 1 are connected"
        }, 
        label="^node^"
    )

p.add_line(
        '^connected_to^(3,^X^) :- ^node^(3), ^node^(^X^), ^X^ = 2.',
        {
            'level1': "^node^ 3 and ^node^ 2 are connected",
            'level2': "^node^s 3 and 2 are connected",
            'level3': "There is a connection between ^node^ 3 and ^node^ ^X^ where ^X^ is 2",
        },
        {
            'level1': "^node^s 3 and 2 are connected"
        }, 
        label="^node^"
    )

p.add_line(
        '1 <= {assigned_to(ND_D,CLR_D): color(CLR_D)} <= 1 :- ^node^(ND_D).',
        {
            'level1': "Every ^node^ can only be assigned a single colour",
            'level2': "^node^s can't be assigned more than one of the colours",
            'level3': "It can't be the case that a ^node^ has more than one colour",
        },
        {
            'level1': "^node^s 3 and 1 are connected"
        }, 
        label="^node^"
    )

p.add_line(
        ':- ^connected_to^(^X^,Y), ^node^(^X^), assigned_to(^X^,C), ^node^(Y), assigned_to(Y,C), color(C).',
        {
            'level1': "Connected ^node^s cannot have the same colour",
            'level2': "If two ^node^s are connected, they must have different colours",
            'level3': "It is not allowed for adjacent ^node^s to share the same colour",
        },
        {
            'level1': "Two adjacent ^node^s cannot have the same colour"
        }, 
        label="^node^"
    )

# Adding variation
v = {
    'node': ['node', 'vertex', 'point', 'element'],
    'node_count': ['3', '14', '32'],
    'colour1': ['red', 'pink', 'purple', 'crimson', 'scarlet', 'maroon'],
    'colour2': ['blue', 'skyBlue', 'cyan', 'azure', 'cobalt'],
    'colour3': ['green', 'limeGreen', 'Emerald', 'olive', 'mint', 'jade',],
    'colourName': ['colour', 'hue', 'shade'],
    'connected_to': ['connected_to', 'linked_to', 'adjacent_to', 'joined_to', 'attached_to'],
    'X': ['X', 'G', 'A', 'C']
}

p.add_variations(v)

# Datagen Setup

cnl_levels = {
    'round1': ['level1'],  
    'round2': ['level2'],   
    'round3': ['level3']   
}

nl_levels = {
    'round1': ['level1'],
}

splice_params = {
    'strategy': 'multi_granularity',
    'min_size': 1,
    'max_size': 11,
    'window_type': 'random',
    'random_samples': 3,
    'random_repeat_min': 2,      
    'random_repeat_cutoff': 10,   
    'randomised_order': True  
}

dg = DataGenerator(p, splice_params=splice_params)
dg.generate_data(cnl_levels, nl_levels)
# dg.get_all_data()
# dg.get_nl_cnl_data()
# dg.get_cnl_asp_data()
dg.export_cnl_asp_instruction_jsonl("raw.jsonl", 'Translate this to ASP code', max_samples=100000)
# dg.export_nl_cnl_instruction_jsonl("test.jsonl", 'Translate this to simpler statements')