from AspPy2 import ASPProgram, DataGenerator

p = ASPProgram()

# Different types of ASP fact structures

# 1. Simple unary facts (one argument)
p.add_line('^entity^("^name^").',
           {'easy': '^name^ is a ^entity^',
            'med': 'The ^entity^ ^name^ exists',
            'hard': '^name^ belongs to the category of ^entity^'},
           {'easy': 'We know that ^name^ is a ^entity^'},
           label='^name^'
          )

# 2. Binary relation facts (two arguments)
p.add_line('^relation^("^person1^", "^person2^").',
           {'easy': '^person1^ is ^relation^ to ^person2^',
            'med': 'There is a ^relation^ relationship between ^person1^ and ^person2^',
            'hard': 'The ^relation^ relation holds for ^person1^ and ^person2^'},
           {'easy': '^person1^ and ^person2^ have a ^relation^ relationship'},
           label='^person1^'
          )

# 3. Ternary facts (three arguments)
p.add_line('^action^("^agent^", "^object^", "^location^").',
           {'easy': '^agent^ ^action^s ^object^ at ^location^',
            'med': 'The action of ^action^ involves ^agent^, ^object^, and ^location^',
            'hard': '^agent^ performs ^action^ on ^object^ in ^location^'},
           {'easy': '^agent^ does ^action^ with ^object^ at ^location^'},
           label='^agent^'
          )

# 4. Property facts with values
p.add_line('^property^("^item^", "^value^").',
           {'easy': '^item^ has ^property^ of ^value^',
            'med': 'The ^property^ of ^item^ is ^value^',
            'hard': '^item^ exhibits the ^property^ characteristic with value ^value^'},
           {'easy': '^item^\'s ^property^ is ^value^'},
           label='^item^'
          )

# 5. Numeric facts
p.add_line('quantity("^resource^", ^amount^).',
           {'easy': 'There are ^amount^ ^resource^s',
            'med': 'The quantity of ^resource^ is ^amount^',
            'hard': 'The resource ^resource^ has a quantity value of ^amount^'},
           {'easy': 'We have ^amount^ units of ^resource^'},
           label='^resource^'
          )

# 6. Timestamp/temporal facts
p.add_line('event("^event_name^", "^time^").',
           {'easy': '^event_name^ happens at ^time^',
            'med': 'The event ^event_name^ occurs at time ^time^',
            'hard': 'Temporal occurrence of ^event_name^ is scheduled for ^time^'},
           {'easy': '^event_name^ takes place at ^time^'},
           label='^event_name^'
          )

# VARIATIONS - Just 2 options each for simplicity
v = {
    'entity': ['person', 'animal'],
    'name': ['alice', 'bob'],
    'relation': ['friend_of', 'parent_of'],
    'person1': ['john', 'mary', 'bob', 'hank'],
    'person2': ['tom', 'lisa', 'joe', 'kate'],
    'action': ['read', 'write'],
    'agent': ['student', 'worker'],
    'object': ['book', 'document'],
    'location': ['library', 'office'],
    'property': ['color', 'weight'],
    'item': ['car', 'phone', 'keys', 'piano'],
    'value': ['red', 'large'],
    'resource': ['water', 'energy'],
    'amount': ['10', '25'],
    'event_name': ['meeting', 'party'],
    'time': ['9am', 'noon']
}

p.add_variations(v)

# Datagen Setup
cnl_levels = {
    'basic': ['easy'],
    'intermediate': ['med'],
    'advanced': ['hard']
}

nl_levels = {
    'basic': ['easy'],
}

# Multi-granularity splice for varied program lengths
splice_params = {
    'strategy': 'multi_granularity',
    'min_size': 1,           # Single facts
    'max_size': 6,           # Up to all 6 fact types
    'window_type': 'random',
    'random_samples': 2,     # 2 samples per size
    'random_repeat_min': 1,  # Repeat for all sizes
    'random_repeat_cutoff': 7, # Repeat for all sizes
    'randomised_order': True # Randomize order of facts
}

dg = DataGenerator(p, splice_params='single')
dg.generate_data(cnl_levels, nl_levels)
# dg.get_cnl_asp_data() 
dg.export_cnl_asp_instruction_jsonl("asp_facts_1k_single.jsonl", 'Translate this to ASP code', 1000)
# dg.export_cnl_asp_instruction_jsonl("asp_facts_10k.jsonl", 'Translate this to ASP code', 10000)