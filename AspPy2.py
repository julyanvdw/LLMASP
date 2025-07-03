# AspPy2: Simple API for modeling ASP programs as lines of strings, with text-based variations

import copy
import itertools
import random

class Line:
    """
    Represents a single line of ASP code, with optional CNL and NL maps.
    """
    def __init__(self, asp_code, cnl_map=None, nl_map=None):
        self.asp_code = asp_code
        self.cnl_map = cnl_map or {}
        self.nl_map = nl_map or {}

    def __str__(self):
        return self.asp_code

    def substitute(self, mapping):
        """
        Substitute ^VAR^ placeholders in asp_code, cnl_map, and nl_map using the mapping.
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
        return Line(new_asp_code, new_cnl_map, new_nl_map)

class ASPProgram:
    """
    Stores an ASP program as a list of Line objects.
    """
    def __init__(self):
        self.lines = []  # List of Line objects
        self.variations = {}

    def add_line(self, asp_code, cnl_map=None, nl_map=None):
        """
        Add a line of ASP code (as a string) to the program.
        Optionally, attach a CNL and NL mapping.
        """
        self.lines.append(Line(asp_code, cnl_map, nl_map))

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
    Generates data from ASPProgram objects, supporting text-based variations and splicing.
    """
    def __init__(self, program=None, splice_params='whole'):
        self.modeled_programs = []
        self.splice_params = splice_params
        if program is not None:
            self.add_program(program)

    def add_program(self, program):
        self.modeled_programs.append(program)

    def add_splice_params(self, splice_params):
        self.splice_params = splice_params

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

    def _generate_splices(self, program, splice_param):
        """
        Generate splices (sub-programs) from the program according to the specified strategy.
        Supports: 'multi_granularity', 'single', 'chunk', 'random', 'whole'
        """

        """ HOW TO USE
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

    def _render_CNL_NL_combinations(self, program, cnl_mods, nl_mods):
        """
        For each line, get all CNLs for cnl_mods and all NLs for nl_mods.
        Return all possible combinations (cartesian product) of CNL and NL for the splice.
        """
        import itertools
        all_cnl_lists = []
        all_nl_lists = []
        for line in program.get_lines():
            cnls = [line.cnl_map[m] for m in cnl_mods if m in line.cnl_map] or [line.asp_code]
            nls = [line.nl_map[m] for m in nl_mods if m in line.nl_map] or [line.asp_code]
            all_cnl_lists.append(cnls)
            all_nl_lists.append(nls)
        for cnl_tuple in itertools.product(*all_cnl_lists):
            for nl_tuple in itertools.product(*all_nl_lists):
                yield "\n".join(cnl_tuple), "\n".join(nl_tuple)

    def generate_data(self, cnl_levels, nl_levels, pairings=None):
        """
        Generate all combinations of CNL and NL according to the specified levels and pairings.
        """
        if pairings is None:
            # Default: full cross-product of all cnl_levels and nl_levels
            pairings = [(c, n) for c in cnl_levels for n in nl_levels]

        for cnl_level, nl_level in pairings:
            cnl_mods = cnl_levels[cnl_level]
            nl_mods = nl_levels[nl_level]
            print(f"=== CNL Level: {cnl_level} | NL Level: {nl_level} ===")
            for p in self.modeled_programs:
                for variation in self._generate_variations(p, p.get_variations()):
                    for splice in self._generate_splices(variation, self.splice_params):
                        for cnl, nl in self._render_CNL_NL_combinations(splice, cnl_mods, nl_mods):
                            print(splice)
                            print(cnl)
                            print(nl)
                            print()

    