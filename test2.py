from AspPy import ASPProgram, DataGenerator

# FACTS WITH VARIATIONS AND TEMPLATES
# Create the project obeject
p = ASPProgram()

# Add lines
p.add_fact('{entity}', ['Alice'])
p.add_fact('{entity}', ['Bob'])

#Add variations
variations = {
    'entity': ['person', 'human']
}
p.add_variations(variations)

# Create and setup the data generator object
dg = DataGenerator(p, splice_params='whole')

# Add CNL templates
templates = {
    'entity/1:fact': '{/1} is defs a {entity}'
}

dg.add_cnl_templates(templates)













'''
TODO
1. check the template with other constructs
2. make the templates work with variations

for rules: 
1. the default template is bad


within a template, we might make use of predicates. For example in a rule, we might say if {1} teaches... but 'teaches' 
is a predicate in and of itself... 

And then for difficulty
we could extend this by just manually hardcoding different difficulty variations: 
templates_plain = {}
templates_negated = {}

pro: super fine-grained control coupled with combinatorial explosive power
pro: super extensible (can add more difficutlty variations)
con: a little bit more up-front effort when moedelling the problem
'''


# 5. Whole program as a single splice

dg.generate_data()


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



