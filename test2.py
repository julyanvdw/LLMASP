from AspPy import ASP_Program

p = ASP_Program()

variations = {
    'name': ['node', 'vertex'],
    # 'relation': ['connected_to', 'related_to'],
    'ranges': ['1..3', '1..5']
}

p.add_fact('{name}', ['{ranges}'])
# p.add_fact('{relation}', ['A', 'B'])

count = 0
for variant in p.generate_variations(variations):
    count += 1
    print(variant.render())
    print("")

print(count)
