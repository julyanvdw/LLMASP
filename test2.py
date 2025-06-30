from AspPy import ASPProgram, DataGenerator

p = ASPProgram()

p.add_fact('{entity}', ['Alice'], {
    'easy': 'Alice is a {entity}'})
p.add_fact('dog', ['Rover'], {
    'easy': 'doggy rover'})

v = {
    'entity': ['person', 'human']
}
p.add_variations(v)



dg = DataGenerator(p, splice_params='single')
dg.generate_data()

'''
TODO
Okay so here's the approach we're going to take to generating data
1. We model the ASP constructs wth python 
2. We can then template this to introduce variations
3. We then add CNL variations to each modeled ASP construct - this gives us super fine grain control over each cnl statement


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



