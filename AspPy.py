# AspPy is an API for modeling ASP rules with python in a parametrized way
# Imports and helper functions for ASP program generation

#todo - could add some sort of syntatic type hint to make the modeling usage easier for someone programming

from jinja2 import Environment, FileSystemLoader
import itertools
import copy

def ensure_list(val):
    if isinstance(val, list):
        return val
    return [val]

def substitute_placeholders(obj, mapping):
    """Recursively substitute placeholders in strings, lists, and objects."""
    if isinstance(obj, str):
        for k, v in mapping.items():
            obj = obj.replace('{' + k + '}', v)
        return obj
    elif isinstance(obj, list):
        return [substitute_placeholders(x, mapping) for x in obj]
    elif hasattr(obj, '__dict__'):
        new_obj = copy.deepcopy(obj)
        for attr, value in new_obj.__dict__.items():
            setattr(new_obj, attr, substitute_placeholders(value, mapping))
        return new_obj
    else:
        return obj

# === ASP Construct Classes ===

class Fact:
    def __init__(self, predicate, terms):
        self.predicate = ensure_list(predicate)
        self.terms = [ensure_list(t) for t in terms]

class Rule:
    def __init__(self, head_predicate, head_terms, body_literals):
        self.head_predicate = ensure_list(head_predicate)
        self.head_terms = [ensure_list(t) for t in head_terms]
        self.body_literals = [ensure_list(lit) for lit in body_literals]

class Constraint:
    def __init__(self, body_literals):
        self.body_literals = [ensure_list(lit) for lit in body_literals]

class CardinalityConstraint:
    def __init__(self, lower, upper, head_predicate, head_terms,
                 condition_predicate, condition_terms,
                 apply_if_predicate, apply_if_terms):
        self.lower = ensure_list(lower)
        self.upper = ensure_list(upper)
        self.head_predicate = ensure_list(head_predicate)
        self.head_terms = [ensure_list(t) for t in head_terms]
        self.condition_predicate = ensure_list(condition_predicate)
        self.condition_terms = [ensure_list(t) for t in condition_terms]
        self.apply_if_predicate = ensure_list(apply_if_predicate)
        self.apply_if_terms = [ensure_list(t) for t in apply_if_terms]

# === ASPProgram Class ===

class ASPProgram:
    def __init__(self, template_dir='./ASP-construct-templates'):
        self.facts = []
        self.rules = []
        self.constraints = []
        self.card_constraints = []
        self.template_dir = template_dir
        self.variations = {}
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template('asp_core.j2')

    def __deepcopy__(self, memo):
        # Avoid copying env/template (not deepcopy-able)
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k not in ('env', 'template'):
                setattr(result, k, copy.deepcopy(v, memo))
        result.env = Environment(loader=FileSystemLoader(self.template_dir))
        result.template = result.env.get_template('asp_core.j2')
        return result

    def add_variations(self, variations):
        self.variations = variations

    def get_variations(self):
        return self.variations

    def add_fact(self, predicate, terms):
        self.facts.append(Fact(predicate, terms))

    def add_rule(self, head_predicate, head_terms, body_literals):
        self.rules.append(Rule(head_predicate, head_terms, body_literals))

    def add_constraint(self, body_literals):
        self.constraints.append(Constraint(body_literals))

    def add_cardinality_constraint(self, *args):
        self.card_constraints.append(CardinalityConstraint(*args))

# === Data_Generator Class ===

class DataGenerator:

    def __init__(self, program=None):
        self.programs = []
        self.data_items = []
        if program is not None:
            self.add_program(program)

    def add_program(self, program):
        self.programs.append(program)

    def generate_variations(self, program, variations):
        keys = list(variations.keys())
        for values in itertools.product(*[variations[k] for k in keys]):
            mapping = dict(zip(keys, values))
            new_prog = copy.deepcopy(program)
            new_prog.facts = [substitute_placeholders(f, mapping) for f in program.facts]
            new_prog.rules = [substitute_placeholders(r, mapping) for r in program.rules]
            new_prog.constraints = [substitute_placeholders(c, mapping) for c in program.constraints]
            new_prog.card_constraints = [substitute_placeholders(cc, mapping) for cc in program.card_constraints]
            yield new_prog

    def render(self, program):
        t = program.template.module
        parts = []
        for f in program.facts:
            predicate = f.predicate[0]
            terms = [term[0] for term in f.terms]
            parts.append(t.render_fact(predicate, terms))
        for r in program.rules:
            head_predicate = r.head_predicate[0]
            head_terms = [term[0] for term in r.head_terms]
            body_literals = [lit[0] for lit in r.body_literals]
            parts.append(t.render_rule(head_predicate, head_terms, body_literals))
        for c in program.constraints:
            body_literals = [lit[0] for lit in c.body_literals]
            parts.append(t.render_integrity_constraint(body_literals))
        for cc in program.card_constraints:
            lower = cc.lower[0]
            upper = cc.upper[0]
            head_predicate = cc.head_predicate[0]
            head_terms = [term[0] for term in cc.head_terms]
            condition_predicate = cc.condition_predicate[0]
            condition_terms = [term[0] for term in cc.condition_terms]
            apply_if_predicate = cc.apply_if_predicate[0]
            apply_if_terms = [term[0] for term in cc.apply_if_terms]
            parts.append(t.render_cardinality_constraint(
                lower, upper,
                head_predicate, head_terms,
                condition_predicate, condition_terms,
                apply_if_predicate, apply_if_terms
            ))
        return '\n'.join(parts)
    
    def generate_data(self):
        # For each program added
        for p in self.programs:
            # For each variant for each program
            for variant in self.generate_variations(p, p.get_variations()):
                self.data_items.append(self.render(variant))
                print(self.render(variant))


