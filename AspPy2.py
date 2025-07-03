# AspPy2: Simple API for modeling ASP programs as lines of strings, with text-based variations

import copy
import itertools

class Line:
    """
    Represents a single line of ASP code, with optional metadata (e.g., CNL/NL mapping).
    """
    def __init__(self, asp_code, cnl_map=None):
        self.asp_code = asp_code  # The ASP rule/fact/constraint as a string
        self.cnl_map = cnl_map or {}  # Optional: mapping for explanations/variations

    def __str__(self):
        return self.asp_code

    def substitute(self, mapping):
        """
        Substitute ^VAR^ placeholders in asp_code and cnl_map using the mapping.
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
        return Line(new_asp_code, new_cnl_map)

class ASPProgram:
    """
    Stores an ASP program as a list of Line objects.
    """
    def __init__(self):
        self.lines = []  # List of Line objects
        self.variations = {}

    def add_line(self, asp_code, cnl_map=None):
        """
        Add a line of ASP code (as a string) to the program.
        Optionally, attach a CNL/NL mapping.
        """
        self.lines.append(Line(asp_code, cnl_map))

    def add_variations(self, variations):
        """
        Add a dictionary of variations for placeholders.
        Example: {'X': ['color', 'hue']}
        """
        self.variations = variations

    def get_variations(self):
        return self.variations

    def get_lines(self):
        """
        Return the list of Line objects.
        """
        return self.lines

    def __str__(self):
        """
        Render the ASP program as a string (just the ASP code).
        """
        return "\n".join(str(line) for line in self.lines)

class DataGenerator:
    """
    Generates data from ASPProgram objects, supporting text-based variations.
    """
    def __init__(self, program=None):
        self.modeled_programs = []
        if program is not None:
            self.add_program(program)

    def add_program(self, program):
        self.modeled_programs.append(program)

    def _substitute_placeholders(self, line, mapping):
        """
        Substitute ^VAR^ placeholders in a Line object using the mapping.
        """
        return line.substitute(mapping)

    def _generate_variations(self, program, variations):
        """
        Generate all combinations of variations for the program.
        """
        if not variations:
            yield program
            return

        keys = list(variations.keys())
        for values in itertools.product(*[variations[k] for k in keys]):
            mapping = dict(zip(keys, values))
            new_prog = copy.deepcopy(program)
            new_prog.lines = [self._substitute_placeholders(line, mapping) for line in program.lines]
            yield new_prog

    def generate_data(self):
        """
        Generate and print all variations of all modeled programs.
        """
        for p in self.modeled_programs:
            for variation in self._generate_variations(p, p.get_variations()):
                print(variation)
                print()