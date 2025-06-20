from jinja2 import Environment, FileSystemLoader


# Jinja2 Setup
env = Environment(loader=FileSystemLoader('./ASP-construct-templates'))
asp_core_templates = env.get_template('asp_core.j2')
asp_construct_templates = env.get_template('asp_constructs.j2')

# Access to individual templates
render_atom = asp_core_templates.module.render_atom
render_fact = asp_construct_templates.module.render_fact
render_rule = asp_construct_templates.module.render_rule
render_cardinality_constraint = asp_construct_templates.module.render_cardinality_constraint
render_integrity_constraint = asp_construct_templates.module.render_integrity_constraint

# Define head predicate and terms
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

rule_str = render_rule('connected_to', ['1', 'X'], [render_atom('node', ['1']), render_atom('node', ['X']), 'X=2'])

print(rule_str)

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

#basically now you need to give the ability to model ASP programs in python - which allows you to template them
#maybe make it like an API 
#then you build in all the variation
#so this contribution is an API for modeling ASP problems in python - which templates them so that you can generate lots of varients according to your modeling (and also vary the difficulty with difficulty modifiers built int)
#it is therefore, not your responsibility to automate the modeling process (this is hard to do, hence why we need LLMs / some form of intelligence in the first place)
#it is only your responsibility to provide an interface in which peopole can take their modled programs, model them in python, which allos them to be extrapolated and varied
