from AspPy import ASPProgram, DataGenerator

p = ASPProgram()

# Add a rule: happy(X) :- person(X), dog(Y).
p.add_rule('happy', ['{names}'], [['person({names})'], ['dog({dogs})']], {
    'easy': 'If {names} is a person, and {dogs} is a dog, then {names} is happy'
})

v = {
    'names' : ['Alice', 'Bob'], 
    'dogs' : ['Rover', 'Pluto'], 
}
p.add_variations(v)

dg = DataGenerator(p, splice_params='whole')
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



