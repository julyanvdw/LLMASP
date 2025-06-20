#An API to model and generate ASP programs using python
#Allows a user to model ASP programs as templates which van be varied

from jinja2 import Environment, FileSystemLoader

# === ASP Construct Classes ===

class Fact:
    def __init__(self, predicate, terms):
        self.predicate = predicate
        self.terms = terms

class Rule:
    def __init__(self, head_predicate, head_terms, body_literals):
        self.head_predicate = head_predicate
        self.head_terms = head_terms
        self.body_literals = body_literals

class Constraint:
    def __init__(self, body_literals):
        self.body_literals = body_literals

class CardinalityConstraint:
    def __init__(self, lower, upper, head_predicate, head_terms,
                 condition_predicate, condition_terms,
                 apply_if_predicate, apply_if_terms):
        self.lower = lower
        self.upper = upper
        self.head_predicate = head_predicate
        self.head_terms = head_terms
        self.condition_predicate = condition_predicate
        self.condition_terms = condition_terms
        self.apply_if_predicate = apply_if_predicate
        self.apply_if_terms = apply_if_terms

# === Program Builder ===

class ASP_Program:
    def __init__(self, template_dir='./ASP-construct-templates'):
        self.facts = []
        self.rules = []
        self.constraints = []
        self.card_constraints = []
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template('asp_core.j2')

    def add_fact(self, predicate, terms):
        self.facts.append(Fact(predicate, terms))

    def add_rule(self, head_predicate, head_terms, body_literals):
        self.rules.append(Rule(head_predicate, head_terms, body_literals))

    def add_constraint(self, body_literals):
        self.constraints.append(Constraint(body_literals))

    def add_cardinality_constraint(self, *args):
        self.card_constraints.append(CardinalityConstraint(*args))

    def render(self):
        t = self.template.module
        parts = []

        for f in self.facts:
            parts.append(t.render_fact(f.predicate, f.terms))
        for r in self.rules:
            parts.append(t.render_rule(r.head_predicate, r.head_terms, r.body_literals))
        for c in self.constraints:
            parts.append(t.render_integrity_constraint(c.body_literals))
        for cc in self.card_constraints:
            parts.append(t.render_cardinality_constraint(
                cc.lower, cc.upper,
                cc.head_predicate, cc.head_terms,
                cc.condition_predicate, cc.condition_terms,
                cc.apply_if_predicate, cc.apply_if_terms
            ))

        return '\n'.join(parts)
    
    # === Data Generator ===