from jinja2 import Environment, FileSystemLoader


# Jinja2 Setup
env = Environment(loader=FileSystemLoader('./ASP-construct-templates'))
asp_core_templates = env.get_template('asp_core.j2')
asp_construct_templates = env.get_template('asp_constructs.j2')

# Access to individual templates
render_atom = asp_core_templates.module.render_atom
render_rule = asp_construct_templates.module.render_rule
render_cardinality_constraint = asp_construct_templates.module.render_cardinality_constraint
render_integrity_constraint = asp_construct_templates.module.render_integrity_constraint

# # Define head predicate and terms
# head_predicate = 'connected_to'
# head_terms = ['1', 'X']

# # Define body literals as strings (pre-rendered)
# body_literals = [
#     render_atom('node', ['1']),
#     'node(X)',
#     'X = 2'
# ]

# # Render the rule
# rule_str = render_rule(head_predicate, head_terms, body_literals)

# print(rule_str)

# result = render_cardinality_constraint(
#     1, 1,
#     'assigned_to', ['ND_D', 'CLR_D'],
#     'color', ['CLR_D'],
#     'node', ['ND_D']
# )

# print(result)


# constraint = render_integrity_constraint([
#     'connected_to(X,Y)',
#     'node(X)',
#     'assigned_to(X,C)',
#     'node(Y)',
#     'assigned_to(Y,C)',
#     'color(C)'
# ])

# print(constraint)

