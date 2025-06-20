from ASP_Data_Gen import ASP_Program

p = ASP_Program()

p.add_fact('node', ['1..3'])
p.add_fact('color', ['"red"'])
p.add_fact('color', ['"blue"'])

p.add_rule('connected_to', ['1', 'X'], ['node(1)', 'node(X)', 'X = 2'])

p.add_constraint([
    'connected_to(X,Y)',
    'node(X)',
    'assigned_to(X,C)',
    'node(Y)',
    'assigned_to(Y,C)',
    'color(C)'
])

p.add_cardinality_constraint(
    1, 1,
    'assigned_to', ['ND_D', 'CLR_D'],
    'color', ['CLR_D'],
    'node', ['ND_D']
)

print(p.render())