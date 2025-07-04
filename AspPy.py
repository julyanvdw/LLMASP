# AspPy is an API for modeling ASP rules with python in a parametrized way
# Imports and helper functions for ASP program generation

#todo - could add some sort of syntatic type hint to make the modeling usage easier for someone programming
#todo - maybe integrate clingo just to check the syntactic correctness of the generated ASP programs

from jinja2 import Environment, FileSystemLoader
import itertools
import copy

def ensure_list(val):
    if isinstance(val, list):
        return val
    return [val]

# === ASP Construct Classes ===

class Fact:
    def __init__(self, predicate, terms, cnl_map=None):
        self.predicate = ensure_list(predicate)
        self.terms = [ensure_list(t) for t in terms]
        self.cnl_map = cnl_map or {}

class Rule:
    def __init__(self, head_predicate, head_terms, body_literals, cnl_map=None):
        self.head_predicate = ensure_list(head_predicate)
        self.head_terms = [ensure_list(t) for t in head_terms]
        self.body_literals = [ensure_list(lit) for lit in body_literals]
        self.cnl_map = cnl_map or {}
        
class Constraint:
    def __init__(self, body_literals, cnl_map=None):
        self.body_literals = [ensure_list(lit) for lit in body_literals]
        self.cnl_map = cnl_map or {}

class CardinalityConstraint:
    def __init__(self, lower, upper, head_predicate, head_terms,
                 condition_predicate, condition_terms,
                 apply_if_predicate, apply_if_terms, cnl_map=None):
        self.lower = ensure_list(lower)
        self.upper = ensure_list(upper)
        self.head_predicate = ensure_list(head_predicate)
        self.head_terms = [ensure_list(t) for t in head_terms]
        self.condition_predicate = ensure_list(condition_predicate)
        self.condition_terms = [ensure_list(t) for t in condition_terms]
        self.apply_if_predicate = ensure_list(apply_if_predicate)
        self.apply_if_terms = [ensure_list(t) for t in apply_if_terms]
        self.cnl_map = cnl_map or {}

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

    def add_fact(self, predicate, terms, cnl_map=None):
        self.facts.append(Fact(predicate, terms, cnl_map))

    def add_rule(self, head_predicate, head_terms, body_literals, cnl_map=None):
        self.rules.append(Rule(head_predicate, head_terms, body_literals, cnl_map))

    def add_constraint(self, body_literals, cnl_map=None):
        self.constraints.append(Constraint(body_literals, cnl_map))

    def add_cardinality_constraint(self, lower, upper, head_predicate, head_terms,
                                   condition_predicate, condition_terms,
                                   apply_if_predicate, apply_if_terms, cnl_map=None):
        self.card_constraints.append(CardinalityConstraint(
            lower, upper, head_predicate, head_terms,
            condition_predicate, condition_terms,
            apply_if_predicate, apply_if_terms, cnl_map
        ))

# === DataGenerator Class ===
 
class DataGenerator:

    def __init__(self, program=None, splice_params=None, diffculty_levels=None):
        self.modeled_programs = []
        self.data_items = []
        self.splice_params = ''
        self.diffculty_levels = ['default']

        if program is not None:
            self.add_program(program)

        if splice_params is not None:
            self.add_splice_params(splice_params)

        if diffculty_levels is not None:
            self.add_diffculty_levels(diffculty_levels)

    def add_program(self, program):
        self.modeled_programs.append(program)

    def add_splice_params(self,splice_params):
        self.splice_params = splice_params

    def add_diffculty_levels(self,diffculty_levels):
        self.diffculty_levels = diffculty_levels

    def _substitute_placeholders(self, obj, mapping):
        """Recursively substitute placeholders in strings, lists, and objects."""
        if isinstance(obj, str):
            for k, v in mapping.items():
                obj = obj.replace('{' + k + '}', v)
            return obj
        elif isinstance(obj, list):
            return [self._substitute_placeholders(x, mapping) for x in obj]
        elif hasattr(obj, '__dict__'):
            new_obj = copy.deepcopy(obj)
            for attr, value in new_obj.__dict__.items():
                if attr == 'cnl_map' and isinstance(value, dict):
                    # Substitute placeholders in all CNL map values
                    new_obj.cnl_map = {k: self._substitute_placeholders(v, mapping) for k, v in value.items()}
                else:
                    setattr(new_obj, attr, self._substitute_placeholders(value, mapping))
            return new_obj
        else:
            return obj

    def _generate_variations(self, program, variations):
        keys = list(variations.keys())
        for values in itertools.product(*[variations[k] for k in keys]):
            mapping = dict(zip(keys, values))
            new_prog = copy.deepcopy(program)
            new_prog.facts = [self._substitute_placeholders(f, mapping) for f in program.facts]
            new_prog.rules = [self._substitute_placeholders(r, mapping) for r in program.rules]
            new_prog.constraints = [self._substitute_placeholders(c, mapping) for c in program.constraints]
            new_prog.card_constraints = [self._substitute_placeholders(cc, mapping) for cc in program.card_constraints]
            yield new_prog

    def _render_ASP_component(self, program):
        t = program.template.module
        parts = []
        for f in program.facts:
            predicate = f.predicate[0]
            terms = [term[0] for term in f.terms]
            parts.append(t.render_fact(predicate, terms))
        for r in program.rules:
            head_predicate = r.head_predicate[0]
            head_terms = [term[0] for term in r.head_terms]
            body_literals = [
                f"{lit[0]}({', '.join(lit[1])})" if lit[1] else lit[0]
                for lit in r.body_literals
            ]
            parts.append(t.render_rule(head_predicate, head_terms, body_literals))
        for c in program.constraints:
            # Render each body literal as predicate(term1,term2,...)
            body = []
            for lit in c.body_literals:
                pred = lit[0]
                terms = lit[1] if len(lit) > 1 else []
                if terms:
                    body.append(f"{pred}({','.join(terms)})")
                else:
                    body.append(f"{pred}")
            constraint_str = ":- " + ", ".join(body) + "."
            parts.append(constraint_str)
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
        return "\n".join(parts)

    def _generate_splices(self, variation, splice_param):
        """
        Splicing Strategies for DataGenerator

        You can control how ASP program variations are split into "splices" (sub-programs) using the `splice_params` argument.
        This enables you to generate more data from each variation at different granularities.

        splice_params can be a string (strategy name) or a dict with more options.

        Supported strategies and parameters:

        1. 'multi_granularity'
            - For a program of n lines, generates splices for every chunk size from max_size down to min_size.
            - For each chunk size k, you can choose how to select the chunks:
                - window_type = 'sliding': All consecutive k-line windows (default).
                - window_type = 'nonoverlap': Non-overlapping k-line chunks.
                - window_type = 'random': Randomly sample k lines (random_samples times).
            - Example:
                splice_params = {
                    'strategy': 'multi_granularity',
                    'min_size': 1,
                    'max_size': None,  # None means use program size
                    'window_type': 'sliding',  # or 'random', 'nonoverlap'
                    'random_samples': 5        # Only used if window_type is 'random'
                }

        2. 'single'
            - Each line (fact, rule, constraint, etc.) is its own splice.
            - Example: splice_params = 'single'

        3. 'chunk'
            - Program is split into consecutive chunks of a fixed size.
            - Parameters:
                - chunk_size: number of lines per chunk (default 2)
            - Example:
                splice_params = {
                    'strategy': 'chunk',
                    'chunk_size': 3
                }

        4. 'random'
            - Randomly sample k lines per splice, repeated random_samples times.
            - Parameters:
                - random_k: number of lines per splice (default 2)
                - random_samples: number of samples to generate (default 3)
            - Example:
                splice_params = {
                    'strategy': 'random',
                    'random_k': 3,
                    'random_samples': 10
                }

        5. 'whole'
            - The entire program is a single splice.
            - Example: splice_params = 'whole'

        Usage:
            - Pass the desired strategy and parameters to DataGenerator:
                dg = DataGenerator(program, splice_params=splice_params)
            - For multi_granularity, you get the most data diversity.

        Notes:
            - If you pass a string (e.g., 'single'), defaults are used for other parameters.
            - For 'multi_granularity', max_size defaults to program size, min_size to 1.
            - For 'random' and 'multi_granularity' with window_type='random', results are non-deterministic unless you set a random seed.

        """
        import random

        # Parse params
        if isinstance(splice_param, str):
            strategy = splice_param
            min_size = 1
            max_size = len(variation.facts) + len(variation.rules) + len(variation.constraints) + len(variation.card_constraints)
            window_type = 'sliding'
            random_samples = 3
            random_repeat_cutoff = 1
            randomised_order = False
        else:
            strategy = splice_param.get('strategy', 'multi_granularity')
            min_size = splice_param.get('min_size', 1)
            max_size = splice_param.get('max_size', None)
            if max_size is None:
                max_size = len(variation.facts) + len(variation.rules) + len(variation.constraints) + len(variation.card_constraints)
            window_type = splice_param.get('window_type', 'sliding')
            random_samples = splice_param.get('random_samples', 3)
            random_repeat_cutoff = splice_param.get('random_repeat_cutoff', 1)
            randomised_order = splice_param.get('randomised_order', False)

        # Convert all ASP components to a flat list of (type, obj)
        lines = []
        for f in variation.facts:
            lines.append(('fact', f))
        for r in variation.rules:
            lines.append(('rule', r))
        for c in variation.constraints:
            lines.append(('constraint', c))
        for cc in variation.card_constraints:
            lines.append(('card_constraint', cc))
        n = len(lines)
        if n == 0:
            return

        def make_program_from_lines(lines_subset):
            # Shuffle the lines within the splice if requested
            if randomised_order:
                lines_shuffled = lines_subset[:]
                random.shuffle(lines_shuffled)
            else:
                lines_shuffled = lines_subset
            prog = copy.deepcopy(variation)
            prog.facts = []
            prog.rules = []
            prog.constraints = []
            prog.card_constraints = []
            for typ, obj in lines_shuffled:
                if typ == 'fact':
                    prog.facts.append(obj)
                elif typ == 'rule':
                    prog.rules.append(obj)
                elif typ == 'constraint':
                    prog.constraints.append(obj)
                elif typ == 'card_constraint':
                    prog.card_constraints.append(obj)
            return prog

        # --- Generate and yield splices ---
        if strategy == 'multi_granularity':
            random_repeat_min = splice_param.get('random_repeat_min', 1)
            for k in range(max_size, min_size - 1, -1):
                if k > n:
                    continue
                if window_type == 'sliding':
                    for i in range(n - k + 1):
                        yield make_program_from_lines(lines[i:i+k])
                elif window_type == 'nonoverlap':
                    for i in range(0, n, k):
                        if i + k <= n:
                            yield make_program_from_lines(lines[i:i+k])
                elif window_type == 'random':
                    # Only repeat if random_repeat_min <= k < random_repeat_cutoff
                    if random_repeat_min <= k < random_repeat_cutoff:
                        repeat = random_samples
                    else:
                        repeat = 1
                    for _ in range(repeat):
                        indices = sorted(random.sample(range(n), k))
                        yield make_program_from_lines([lines[idx] for idx in indices])
        elif strategy == 'single':
            for line in lines:
                yield make_program_from_lines([line])
        elif strategy == 'chunk':
            chunk_size = splice_param.get('chunk_size', 2)
            for i in range(0, n, chunk_size):
                yield make_program_from_lines(lines[i:i+chunk_size])
        elif strategy == 'random':
            k = splice_param.get('random_k', 2)
            random_samples = splice_param.get('random_samples', 3)
            randomised_order = splice_param.get('randomised_order', False)
            if k > n:
                return
            for _ in range(random_samples):
                indices = sorted(random.sample(range(n), k))
                yield make_program_from_lines([lines[idx] for idx in indices])
        elif strategy == 'whole':
            yield make_program_from_lines(lines)
        else:
            raise ValueError(f"Unknown splicing strategy: {strategy}")

    def _render_CNL_component(self, program, difficulty_modifiers):
        """
        Render the CNL version of the program (splice) according to the provided difficulty_modifiers.
        For each construct, if any modifier in difficulty_modifiers is present in cnl_map, use it.
        If not, fall back to the default template in cnl_core.j2.
        """
        # Load the CNL template
        env = Environment(loader=FileSystemLoader(program.template_dir))
        t = env.get_template('cnl_core.j2').module

        parts = []
        # Facts
        for f in program.facts:
            found = False
            for mod in difficulty_modifiers:
                cnl = f.cnl_map.get(mod)
                if cnl:
                    if isinstance(cnl, list):
                        parts.extend(cnl)
                    else:
                        parts.append(cnl)
                    found = True
                    break
            if not found:
                predicate = f.predicate[0]
                terms = [term[0] for term in f.terms]
                parts.append(t.render_fact(predicate, terms))
        # Rules
        for r in program.rules:
            found = False
            for mod in difficulty_modifiers:
                cnl = r.cnl_map.get(mod)
                if cnl:
                    if isinstance(cnl, list):
                        parts.extend(cnl)
                    else:
                        parts.append(cnl)
                    found = True
                    break
            if not found:
                head_predicate = r.head_predicate[0]
                head_terms = [term[0] for term in r.head_terms]
                body_literals = [lit[0] for lit in r.body_literals]
                parts.append(t.render_rule(head_predicate, head_terms, body_literals))
        # Constraints
        for c in program.constraints:
            found = False
            for mod in difficulty_modifiers:
                cnl = c.cnl_map.get(mod)
                if cnl:
                    if isinstance(cnl, list):
                        parts.extend(cnl)
                    else:
                        parts.append(cnl)
                    found = True
                    break
            if not found:
                body_literals = [lit[0] for lit in c.body_literals]
                parts.append(t.render_integrity_constraint(body_literals))
        # Cardinality Constraints
        for cc in program.card_constraints:
            found = False
            for mod in difficulty_modifiers:
                cnl = cc.cnl_map.get(mod)
                if cnl:
                    if isinstance(cnl, list):
                        parts.extend(cnl)
                    else:
                        parts.append(cnl)
                    found = True
                    break
            if not found:
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

        # GENERATE ASP COMPONENTS

        for level in self.diffculty_levels:
            for p in self.modeled_programs:
                for variation in self._generate_variations(p, p.get_variations()):
                    for splice in self._generate_splices(variation, self.splice_params):
                        print(self._render_ASP_component(splice))
                        print()
                        print(self._render_CNL_component(splice, level))
                        print()

       

                




        #for difficulty level in difficulty_levels:

        '''
        for asp_component in asp_components:
            
            asp_component is an ASPProgram object
            asp_components (the array) contains all the splices we generated previously

            now we generate the CNL and NL components 
            NB: there may be multiple CNL statements joined with the same ASP component (this gives us expansion)

            We can also paraphrase each CNL component multiple times


            #CNL component - generate according to specified difficulty levels
            for difficulty_level in difficulty_levels:
            
                #Generate CNL statement
                cnl_component_rendered_raw = _render_CNL_component(asp_component, difficulty_level)

                #for each difficulty levels, create different paraphrases
                    for i range (1..how_many_paraphrases):

                        data_item = {
                            'ASP': None,
                            'CNL': None,
                            'NL': None
                        }
                        
                        #Generate paraphrase
                        cnl_component_rendered = cnl_paraphrase(cnl_component_rendered_raw, some_paraphrase_modifier)
                        
                        #Generate NL component
                        nl_component_rendered = some_function()

                        data_item['ASP'] = _render_ASP_component(asp_component)
                        data_item['CNL'] = cnl_component_rendered
                        data_item['NL'] = nl_component_rendered

            '''













