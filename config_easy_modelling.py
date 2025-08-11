from AspPy2 import ASPProgram, DataGenerator

# Define the theme set for the computer build problem
theme_sets = [
    {
        'P1': 'cpu',
        'P2': 'selected_cpu',
        'P3': 'gpu',
        'P4': 'selected_gpu',
        'P5': 'mobo',
        'P6': 'selected_mobo',
        'V1': 'Ryzen5',
        'V2': 'i5',
        'V3': 'GTX1660',
        'V4': 'RX580',
        'V5': 'B450',
        'V6': 'Z390',
        'C': 'C',
        'G': 'G',
        'M': 'M',
        'variations': {
            'V1': ['Ryzen5', 'Ryzen4'],
            'V2': ['i5'],
            'V3': ['GTX1660'],
            'V4': ['RX580'],
            'V5': ['B450'],
            'V6': ['Z390']
        }
    }
]

def generate_programs(theme_sets):
    generated_programs = []

    for theme in theme_sets:
        p = ASPProgram()

        # CPU
        cpu_fact = p.add_line(
            '{P1}("^V1^"; "^V2^").'.format(**theme),
            {'simple': '^V1^ and ^V2^ are {P1}s.'.format(**theme)},
            {'simple': 'There are two {P1}s: ^V1^ and ^V2^.'.format(**theme)},
            label='cpu'
        )
        cpu_choice = p.add_line(
            '1 {{ {P2}({C}) : {P1}({C}) }} 1.'.format(**theme),
            {'simple': 'Select exactly one {P1} from ^V1^, ^V2^.'.format(**theme)},
            {'simple': 'You must choose one {P1}: ^V1^ or ^V2^.'.format(**theme)},
            label='cpu_choice'
        )

        # GPU
        gpu_fact = p.add_line(
            '{P3}("^V3^"; "^V4^").'.format(**theme),
            {'simple': '^V3^ and ^V4^ are {P3}s.'.format(**theme)},
            {'simple': 'There are two {P3}s: ^V3^ and ^V4^.'.format(**theme)},
            label='gpu'
        )
        gpu_choice = p.add_line(
            '1 {{ {P4}({G}) : {P3}({G}) }} 1.'.format(**theme),
            {'simple': 'Select exactly one {P3} from ^V3^, ^V4^.'.format(**theme)},
            {'simple': 'You must choose one {P3}: ^V3^ or ^V4^.'.format(**theme)},
            label='gpu_choice'
        )

        # Motherboard
        mobo_fact = p.add_line(
            '{P5}("^V5^"; "^V6^").'.format(**theme),
            {'simple': '^V5^ and ^V6^ are {P5}s.'.format(**theme)},
            {'simple': 'There are two {P5}s: ^V5^ and ^V6^.'.format(**theme)},
            label='mobo'
        )
        mobo_choice = p.add_line(
            '1 {{ {P6}({M}) : {P5}({M}) }} 1.'.format(**theme),
            {'simple': 'Select exactly one {P5} from ^V5^, ^V6^.'.format(**theme)},
            {'simple': 'You must choose one {P5}: ^V5^ or ^V6^.'.format(**theme)},
            label='mobo_choice'
        )

        # Selection group
        p.add_group(
            [cpu_fact, cpu_choice, gpu_fact, gpu_choice, mobo_fact, mobo_choice],
            {'simple/6': 'You must select exactly one {P1}, one {P3}, and one {P5} for your build.'.format(**theme)}
        )

        # Compatibility constraints
        req1 = p.add_line(
            ':- {P2}("^V1^"), {P6}(M), M != "^V5^".'.format(**theme),
            {'simple': 'The ^V1^ {P1} requires the ^V5^ {P5}.'.
                format(**theme)},
            {'simple': 'If you select ^V1^, you must use ^V5^ as the {P5}.'.
                format(**theme)},
            label='req1'
        )
        req2 = p.add_line(
            ':- {P2}("^V2^"), {P6}(M), M != "^V6^".'.format(**theme),
            {'simple': 'The ^V2^ {P1} requires the ^V6^ {P5}.'.
                format(**theme)},
            {'simple': 'If you select ^V2^, you must use ^V6^ as the {P5}.'.
                format(**theme)},
            label='req2'
        )
        req3 = p.add_line(
            ':- {P4}("^V4^"), {P6}("^V6^").'.format(**theme),
            {'simple': 'The ^V4^ {P3} is incompatible with the ^V6^ {P5}.'.
                format(**theme)},
            {'simple': 'You cannot use ^V4^ with ^V6^.'.
                format(**theme)},
            label='req3'
        )

        # Constraints group
        p.add_group(
            [req1, req2, req3],
            {'simple/3': 'Compatibility rules: {1}, {2}, and {3}.'}
        )

        # Register value variations
        p.add_variations(theme['variations'])
        generated_programs.append(p)

    return generated_programs

# Set up CNL and NL levels
cnl_levels = {'simple': ['simple']}
nl_levels = {'simple': ['simple']}

# Generate the programs from the theme sets
programs = generate_programs(theme_sets)

# Generate and print all data for each program
for p in programs:
    dg = DataGenerator(p, splice_params='whole')
    dg.generate_data(cnl_levels=cnl_levels, nl_levels=nl_levels)
    dg.get_all_data()