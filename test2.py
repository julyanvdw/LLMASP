from ASP_Data_Gen import ASP_Program

p = ASP_Program()
# p.add_fact('{name}', ['1..3'])
# # p.add_fact('color', ['"red"'])
# # p.add_fact('color', ['"green"'])
# # p.add_fact('color', ['"blue"'])
# p.add_rule('{rel}', ['1', 'X'], [['{name}', ['1']], ['{name}', ['X']], ['X = 2']])

# variations = {
#     'name': ['node', 'vertex'],
#     'rel': ['connected_to', 'linked_to']
# }

variations = {
    'name': ['node', 'vertex'],
    'relation': ['connected_to', 'related_to'],
    'range': ['1..3', '1..5']
}

p.add_fact('{name}', ['{range}'])
p.add_fact('{relation}', ['A', 'B'])

count = 0
for variant in p.generate_variations(variations):
    count += 1
    print(variant.render())
    print("")

print(count)