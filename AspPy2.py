# AspPy2: Simple API for modeling ASP programs as lines of strings, with text-based variations

import copy
import itertools
import random
import json

def natural_join(names):
    if len(names) == 1:
        return names[0]
    elif len(names) == 2:
        return f"{names[0]} and {names[1]}"
    else:
        return ", ".join(names[:-1]) + f" and {names[-1]}"

class Line:
    """
    Represents a single line of ASP code, with optional CNL and NL maps and a label.
    """
    def __init__(self, asp_code, cnl_map=None, nl_map=None, label=None):
        self.asp_code = asp_code
        self.cnl_map = cnl_map or {}
        self.nl_map = nl_map or {}
        self.label = label

    def __str__(self):
        return self.asp_code

    def substitute(self, mapping):
        """
        Substitute ^VAR^ placeholders in asp_code, cnl_map, nl_map, and label using the mapping.
        """
        new_asp_code = self.asp_code
        for k, v in mapping.items():
            new_asp_code = new_asp_code.replace(f'^{k}^', v)
        new_cnl_map = {}
        for key, val in self.cnl_map.items():
            if isinstance(val, str):
                new_val = val
                for k, v in mapping.items():
                    new_val = new_val.replace(f'^{k}^', v)
                new_cnl_map[key] = new_val
            else:
                new_cnl_map[key] = val
        new_nl_map = {}
        for key, val in self.nl_map.items():
            if isinstance(val, str):
                new_val = val
                for k, v in mapping.items():
                    new_val = new_val.replace(f'^{k}^', v)
                new_nl_map[key] = new_val
            else:
                new_nl_map[key] = val
        new_label = self.label
        if new_label:
            for k, v in mapping.items():
                new_label = new_label.replace(f'^{k}^', v)
        return Line(new_asp_code, new_cnl_map, new_nl_map, new_label)

class Group:
    """
    Represents a group of lines with a group-level NL map.
    """
    def __init__(self, lines, nl_map=None):
        self.lines = lines  # List of Line objects
        self.nl_map = nl_map or {}

    def substitute(self, mapping):
        """
        Substitute ^VAR^ placeholders in the group's NL map.
        """
        new_nl_map = {}
        for key, val in self.nl_map.items():
            if isinstance(val, str):
                new_val = val
                for k, v in mapping.items():
                    new_val = new_val.replace(f'^{k}^', v)
                new_nl_map[key] = new_val
            else:
                new_nl_map[key] = val
        return Group(self.lines, new_nl_map)

class ASPProgram:
    """
    Stores an ASP program as a list of Line objects and groups.
    """
    def __init__(self):
        self.lines = []  # List of Line objects
        self.variations = {}
        self.groups = []  # List of Group objects

    def add_line(self, asp_code, cnl_map=None, nl_map=None, label=None):
        """
        Add a line of ASP code (as a string) to the program.
        Optionally, attach a CNL and NL mapping and a label.
        Returns the Line object for group referencing.
        """
        line = Line(asp_code, cnl_map, nl_map, label)
        self.lines.append(line)
        return line

    def add_group(self, lines, nl_map=None):
        """
        Add a group of lines with a group-level NL map.
        """
        group = Group(lines, nl_map)
        self.groups.append(group)
        return group

    def add_variations(self, variations):
        """
        Add a dictionary of variations for placeholders.
        Example: {'X': ['color', 'hue']}
        """
        self.variations = variations

    def get_variations(self):
        return self.variations

    def get_lines(self):
        return self.lines

    def get_groups(self):
        return self.groups

    def __str__(self):
        return "\n".join(str(line) for line in self.lines)

class DataGenerator:
    """
    Generates data from ASPProgram objects, supporting text-based variations, splicing, and group NLs.
    Stores all generated data and provides methods for unique NL:CNL and CNL:ASP pairs.
    """
    def __init__(self, program=None, splice_params='whole'):
        self.modeled_programs = []
        self.splice_params = splice_params
        self.all_data = []      # List of dicts: {'asp': asp, 'cnl': cnl, 'nl': nl}
        self.nl_cnl_set = set() # Set of (nl, cnl)
        self.cnl_asp_set = set()# Set of (cnl, asp)
        if program is not None:
            self.add_program(program)

    def add_program(self, program):
        self.modeled_programs.append(program)

    def add_splice_params(self, splice_params):
        self.splice_params = splice_params

    def _substitute_placeholders(self, obj, mapping):
        """
        Substitute ^VAR^ placeholders in a Line or Group object using the mapping.
        """
        return obj.substitute(mapping)

    def _generate_variations(self, program, variations):
        """
        Generate all combinations of variations for the program, including lines and groups.
        """
        if not variations:
            yield program
            return

        keys = list(variations.keys())
        for values in itertools.product(*[variations[k] for k in keys]):
            mapping = dict(zip(keys, values))
            new_prog = copy.deepcopy(program)
            # Substitute in lines
            new_prog.lines = [self._substitute_placeholders(line, mapping) for line in program.lines]
            # Substitute in groups
            new_prog.groups = []
            for group in program.groups:
                # Find the corresponding new Line objects in new_prog for this group
                new_lines = []
                for orig_line in group.lines:
                    # Match by asp_code after substitution
                    for new_line in new_prog.lines:
                        if new_line.asp_code == self._substitute_placeholders(orig_line, mapping).asp_code:
                            new_lines.append(new_line)
                            break
                new_prog.groups.append(self._substitute_placeholders(Group(new_lines, group.nl_map), mapping))
            yield new_prog

    def _generate_splices(self, program, splice_param):
        """
        Generate splices (sub-programs) from the program according to the specified strategy.
        """
        lines = program.get_lines()
        n = len(lines)
        if n == 0:
            return

        # Parse params
        if isinstance(splice_param, str):
            strategy = splice_param
            min_size = 1
            max_size = n
            window_type = 'sliding'
            random_samples = 3
            randomised_order = False
        else:
            strategy = splice_param.get('strategy', 'multi_granularity')
            min_size = splice_param.get('min_size', 1)
            max_size = splice_param.get('max_size', n)
            window_type = splice_param.get('window_type', 'sliding')
            random_samples = splice_param.get('random_samples', 3)
            randomised_order = splice_param.get('randomised_order', False)

        def make_program_from_lines(lines_subset):
            if randomised_order:
                lines_shuffled = lines_subset[:]
                random.shuffle(lines_shuffled)
            else:
                lines_shuffled = lines_subset
            prog = copy.deepcopy(program)
            prog.lines = lines_shuffled
            return prog

        # --- Generate and yield splices ---
        if strategy == 'multi_granularity':
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
                    for _ in range(random_samples):
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

    def _render_cnl_combinations(self, program, cnl_mods):
        """
        For each line, get all CNLs for cnl_mods.
        Return all possible combinations (cartesian product) of CNL for the splice.
        """
        all_cnl_lists = []
        for line in program.get_lines():
            cnls = [line.cnl_map[m] for m in cnl_mods if m in line.cnl_map] or [line.asp_code]
            all_cnl_lists.append(cnls)
        for cnl_tuple in itertools.product(*all_cnl_lists):
            yield "\n".join(cnl_tuple)

    def _render_nl_combinations_with_groups(self, program, nl_mods, splice_lines):
        """
        Render NL for a splice, using group NLs for any subset of group lines (>=2).
        Fills ^GROUP_MEMBERS^ with the joined labels of present lines.
        Returns all possible combinations (cartesian product) of NLs for the splice.
        """
        used_lines = set()
        nl_lists = []

        # Handle groups first (largest groups first for priority)
        for group in sorted(program.get_groups(), key=lambda g: -len(g.lines)):
            present_lines = [line for line in group.lines if line in splice_lines]
            arity = len(present_lines)
            if arity >= 1:
                for m in nl_mods:
                    key = f"{m}/{arity}"
                    if key in group.nl_map:
                        template = group.nl_map[key]
                        # Fill {1}, {2}, ... with labels
                        label_map = {f"{{{i+1}}}": (line.label or line.asp_code) for i, line in enumerate(present_lines)}
                        nl = template
                        for k, v in label_map.items():
                            nl = nl.replace(k, v)
                        nl_lists.append([nl])
                        used_lines.update(present_lines)
                        break  # Only use the first matching template

        # Handle remaining lines not covered by a group
        for line in splice_lines:
            if line not in used_lines:
                nls = [line.nl_map[m] for m in nl_mods if m in line.nl_map] or [line.asp_code]
                nl_lists.append(nls)

        # Cartesian product of all NL lists
        for nl_tuple in itertools.product(*nl_lists):
            yield "\n".join(nl_tuple)

    def generate_data(self, cnl_levels, nl_levels, pairings=None):
        """
        Generate all combinations of CNL and NL according to the specified levels and pairings.
        Stores all data and unique NL:CNL and CNL:ASP pairs.
        """
        self.all_data = []
        self.nl_cnl_set = set()
        self.cnl_asp_set = set()

        if pairings is None:
            pairings = [(c, n) for c in cnl_levels for n in nl_levels]

        for cnl_level, nl_level in pairings:
            cnl_mods = cnl_levels[cnl_level]
            nl_mods = nl_levels[nl_level]
            for p in self.modeled_programs:
                for variation in self._generate_variations(p, p.get_variations()):
                    for splice in self._generate_splices(variation, self.splice_params):
                        for cnl in self._render_cnl_combinations(splice, cnl_mods):
                            for nl in self._render_nl_combinations_with_groups(variation, nl_mods, splice.get_lines()):
                                asp_str = str(splice)
                                entry = {'asp': asp_str, 'cnl': cnl, 'nl': nl}
                                self.all_data.append(entry)
                                self.nl_cnl_set.add((nl, cnl))
                                self.cnl_asp_set.add((cnl, asp_str))

    def get_all_data(self):
        """
        Print all generated (ASP, CNL, NL) triplets.
        """
        for entry in self.all_data:
            print(entry['asp'])
            print(entry['cnl'])
            print(entry['nl'])
            print()

        print(f"COUNT: {len(self.all_data)}")

    def get_nl_cnl_data(self):
        """
        Print all unique (NL, CNL) pairs.
        """
        for nl, cnl in self.nl_cnl_set:
            print(cnl)
            print(nl)
            print()

        print(f"COUNT: {len(self.nl_cnl_set)}")

    def get_cnl_asp_data(self):
        """
        Print all unique (CNL, ASP) pairs.
        """
        for cnl, asp in self.cnl_asp_set:
            print(asp)
            print(cnl)
            print()
        
        print(f"COUNT: {len(self.cnl_asp_set)}")

    def export_nl_cnl_instruction_jsonl(self, filename, instruction):
        """
        Export unique NL:CNL pairs as a JSONL file for instruction tuning (NL input, CNL output).
        Each line is: {"instruction": <instruction>, "input": <NL>, "output": <CNL>}
        """
        with open(filename, "w", encoding="utf-8") as f:
            for nl, cnl in self.nl_cnl_set:
                obj = {
                    "instruction": instruction,
                    "input": nl,
                    "output": cnl
                }
                f.write(json.dumps(obj, ensure_ascii=False) + "\n")
        print(f"Wrote {len(self.nl_cnl_set)} NL:CNL instruction pairs to {filename}")

    def export_cnl_asp_instruction_jsonl(self, filename, instruction):
        """
        Export unique CNL:ASP pairs as a JSONL file for instruction tuning (CNL input, ASP output).
        Each line is: {"instruction": <instruction>, "input": <CNL>, "output": <ASP>}
        """
        with open(filename, "w", encoding="utf-8") as f:
            for cnl, asp in self.cnl_asp_set:
                obj = {
                    "instruction": instruction,
                    "input": cnl,
                    "output": asp
                }
                f.write(json.dumps(obj, ensure_ascii=False) + "\n")
        print(f"Wrote {len(self.cnl_asp_set)} CNL:ASP instruction pairs to {filename}")

