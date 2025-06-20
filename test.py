from jinja2 import Environment, FileSystemLoader


# Jinja2 Setup
env = Environment(loader=FileSystemLoader('./ASP-construct-templates'))
asp_core_templates = env.get_template('asp_core.j2')
asp_construct_templates = env.get_template('asp_constructs.j2')

# Access to individual templates
render_atom = asp_core_templates.module.render_atom
render_term = asp_core_templates.module.render_term

# Call the macro with your parameters
print(render_term('a'))

