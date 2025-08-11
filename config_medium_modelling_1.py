from AspPy2 import ASPProgram, DataGenerator
import random
import json

theme_sets = [
    {
        'P1': 'cpu',
        'P2': 'selected_cpu',
        'P3': 'gpu',
        'P4': 'selected_gpu',
        'P5': 'mobo',
        'P6': 'selected_mobo',
        'P7': 'psu',
        'P8': 'selected_psu',
        'P9': 'high_power',
        'theme': 'Workstation Build',
        'verb': 'assemble',
        # 'variations': {
        #     'V1': ['Ryzen7', 'i9', 'Xeon'],
        #     'V2': ['i9', 'Xeon', 'Ryzen7'],
        #     'V3': ['Xeon', 'Ryzen7', 'i9'],
        #     'V4': ['RTX4060', 'RTX3090', 'Quadro'],
        #     'V5': ['RTX3090', 'Quadro', 'RTX4060'],
        #     'V6': ['Quadro', 'RTX4060', 'RTX3090'],
        #     'V7': ['X670', 'Z690', 'C621'],
        #     'V8': ['Z690', 'C621', 'X670'],
        #     'V9': ['C621', 'X670', 'Z690'],
        #     'V10': ['Bronze', 'Gold', 'Platinum'],
        #     'V11': ['Gold', 'Platinum', 'Bronze'],
        #     'V12': ['Platinum', 'Bronze', 'Gold'],
        #     'C1': ['300', '400', '500'],
        #     'C2': ['400', '500', '300'],
        #     'C3': ['500', '300', '400'],
        #     'C4': ['350', '700', '800'],
        #     'C5': ['700', '800', '350'],
        #     'C6': ['800', '350', '700'],
        #     'C7': ['180', '200', '250'],
        #     'C8': ['200', '250', '180'],
        #     'C9': ['250', '180', '200'],
        #     'C10': ['80', '120', '160'],
        #     'C11': ['120', '160', '80'],
        #     'C12': ['160', '80', '120']
        # }
        'variations': {
            'V1': ['Ryzen7'],
            'V2': ['i9'],
            'V3': ['Xeon'],
            'V4': ['RTX4060'],
            'V5': ['RTX3090'],
            'V6': ['Quadro'],
            'V7': ['X670'],
            'V8': ['Z690'],
            'V9': ['C621',],
            'V10': ['Bronze',],
            'V11': ['Gold'],
            'V12': ['Platinum'],
            'C1': ['300',],
            'C2': ['400',],
            'C3': ['500',],
            'C4': ['350',],
            'C5': ['700',],
            'C6': ['800',],
            'C7': ['180',],
            'C8': ['200',],
            'C9': ['250',],
            'C10': ['80',],
            'C11': ['120',],
            'C12': ['160',]
        }
    }
]

def generate_programs(theme_sets):
    programs = []
    for theme in theme_sets:
        p = ASPProgram()

        # CPU group
        cpu = p.add_line(
            '{P1}("^V1^", ^C1^; "^V2^", ^C2^; "^V3^", ^C3^).'.format(**theme),
            {'simple': 'Select one {P1} from ^V1^, ^V2^, ^V3^, with costs: ^V1^ = ^C1^, ^V2^ = ^C2^, ^V3^ = ^C3^.'.format(**theme)},
            {'nl1': 'Choose a {P1}: ^V1^, ^V2^, or ^V3^. Their costs are ^C1^, ^C2^, and ^C3^.'.format(**theme)}
        )
        cpu_choice = p.add_line(
            '1 {{ {P2}(C) : {P1}(C, _) }} 1.'.format(**theme),
            {'simple': 'Pick only one {P1}.'.format(**theme)},
            {'nl1': 'You must select exactly one {P1} for your {verb}.'.format(**theme)}
        )
        p.add_group(
            [cpu, cpu_choice],
            {
                'nl1/2': 'Choose a {P1} (^V1^, ^V2^, ^V3^) for your {verb}. You must select exactly one. Costs: ^V1^=^C1^, ^V2^=^C2^, ^V3^=^C3^.'.format(**theme)
            }
        )

        # GPU group
        gpu = p.add_line(
            '{P3}("^V4^", ^C4^; "^V5^", ^C5^; "^V6^", ^C6^).'.format(**theme),
            {'simple': 'Select one {P3} from ^V4^, ^V5^, ^V6^, with costs: ^V4^ = ^C4^, ^V5^ = ^C5^, ^V6^ = ^C6^.'.format(**theme)},
            {'nl1': 'Choose a {P3}: ^V4^, ^V5^, or ^V6^. Their costs are ^C4^, ^C5^, and ^C6^.'.format(**theme)}
        )
        gpu_choice = p.add_line(
            '1 {{ {P4}(G) : {P3}(G, _) }} 1.'.format(**theme),
            {'simple': 'Pick only one {P3}.'.format(**theme)},
            {'nl1': 'You must select exactly one {P3} for your {verb}.'.format(**theme)}
        )
        p.add_group(
            [gpu, gpu_choice],
            {
                'nl1/2': 'Choose a {P3} (^V4^, ^V5^, ^V6^) for your {verb}. You must select exactly one. Costs: ^V4^=^C4^, ^V5^=^C5^, ^V6^=^C6^.'.format(**theme)
            }
        )

        # MOBO group
        mobo = p.add_line(
            '{P5}("^V7^", ^C7^; "^V8^", ^C8^; "^V9^", ^C9^).'.format(**theme),
            {'simple': 'Select one {P5} from ^V7^, ^V8^, ^V9^, with costs: ^V7^ = ^C7^, ^V8^ = ^C8^, ^V9^ = ^C9^.'.format(**theme)},
            {'nl1': 'Choose a {P5}: ^V7^, ^V8^, or ^V9^. Their costs are ^C7^, ^C8^, and ^C9^.'.format(**theme)}
        )
        mobo_choice = p.add_line(
            '1 {{ {P6}(M) : {P5}(M, _) }} 1.'.format(**theme),
            {'simple': 'Pick only one {P5}.'.format(**theme)},
            {'nl1': 'You must select exactly one {P5} for your {verb}.'.format(**theme)}
        )
        p.add_group(
            [mobo, mobo_choice],
            {
                'nl1/2': 'Choose a {P5} (^V7^, ^V8^, ^V9^) for your {verb}. You must select exactly one. Costs: ^V7^=^C7^, ^V8^=^C8^, ^V9^=^C9^.'.format(**theme)
            }
        )

        # PSU group
        psu = p.add_line(
            '{P7}("^V10^", ^C10^; "^V11^", ^C11^; "^V12^", ^C12^).'.format(**theme),
            {'simple': 'Select one {P7} from ^V10^, ^V11^, ^V12^, with costs: ^V10^ = ^C10^, ^V11^ = ^C11^, ^V12^ = ^C12^.'.format(**theme)},
            {'nl1': 'Choose a {P7}: ^V10^, ^V11^, or ^V12^. Their costs are ^C10^, ^C11^, and ^C12^.'.format(**theme)}
        )
        psu_choice = p.add_line(
            '1 {{ {P8}(P) : {P7}(P, _) }} 1.'.format(**theme),
            {'simple': 'Pick only one {P7}.'.format(**theme)},
            {'nl1': 'You must select exactly one {P7} for your {verb}.'.format(**theme)}
        )
        p.add_group(
            [psu, psu_choice],
            {
                'nl1/2': 'Choose a {P7} (^V10^, ^V11^, ^V12^) for your {verb}. You must select exactly one. Costs: ^V10^=^C10^, ^V11^=^C11^, ^V12^=^C12^.'.format(**theme)
            }
        )

        # Constraints group
        high_power = p.add_line(
            '{P9}("^V5^"; "^V6^").'.format(**theme),
            {'simple': '^V5^ and ^V6^ are high-power {P3}s.'.format(**theme)},
            {'nl1': 'The ^V5^ and ^V6^ {P3}s use a lot of power.'.format(**theme)}
        )
        constraint1 = p.add_line(
            ':- {P4}(G), {P9}(G), {P8}("^V10^").'.format(**theme),
            {'simple': 'High-power {P3}s require {P7} ∈ ^V11^, ^V12^.'.format(**theme)},
            {'nl1': 'If you pick a high-power {P3}, you must use a ^V11^ or ^V12^ {P7}.'.format(**theme)}
        )
        constraint2 = p.add_line(
            ':- {P2}("^V3^"), {P6}(M), M != "^V9^".'.format(**theme),
            {'simple': '^V3^ requires {P5} ^V9^.'},
            {'nl1': 'The ^V3^ {P1} only works with the ^V9^ {P5}.'.format(**theme)}
        )
        constraint3 = p.add_line(
            ':- {P2}("^V1^"), {P6}(M), M != "^V7^".'.format(**theme),
            {'simple': '^V1^ requires {P5} ^V7^.'},
            {'nl1': 'The ^V1^ {P1} only works with the ^V7^ {P5}.'.format(**theme)}
        )
        constraint4 = p.add_line(
            ':- {P2}("^V2^"), {P6}("^V7^").'.format(**theme),
            {'simple': '^V2^ is incompatible with {P5} ^V7^.'},
            {'nl1': 'The ^V2^ {P1} cannot be paired with the ^V7^ {P5}.'.format(**theme)}
        )
        constraint5 = p.add_line(
            ':- {P4}("^V6^"), {P2}(C), C != "^V3^".'.format(**theme),
            {'simple': '^V6^ requires ^V3^ {P1}.'},
            {'nl1': 'The ^V6^ {P3} requires the ^V3^ {P1}.'.format(**theme)}
        )
        constraint6 = p.add_line(
            ':- {P4}("^V6^"), {P6}("^V8^").'.format(**theme),
            {'simple': '^V6^ is incompatible with {P5} ^V8^.'},
            {'nl1': 'The ^V6^ {P3} cannot be used with the ^V8^ {P5}.'.format(**theme)}
        )
        p.add_group(
            [high_power, constraint1, constraint2, constraint3, constraint4, constraint5, constraint6],
            {
                'nl1/7': (
                    'Compatibility rules: '
                    '^V5^ and ^V6^ are high-power {P3}s and require a ^V11^ or ^V12^ {P7}. '
                    '^V3^ {P1} only works with ^V9^ {P5}. '
                    '^V1^ {P1} only works with ^V7^ {P5}. '
                    '^V2^ {P1} cannot be paired with ^V7^ {P5}. '
                    '^V6^ {P3} requires the ^V3^ {P1}. '
                    '^V6^ {P3} cannot be used with ^V8^ {P5}.'
                ).format(**theme)
            }
        )

        # Cost/minimize group
        cost = p.add_line(
            'total_cost(Cost) :- {P2}(C), {P1}(C, CCost), {P4}(G), {P3}(G, GCost), {P6}(M), {P5}(M, MCost), {P8}(P), {P7}(P, PCost), Cost = CCost + GCost + MCost + PCost.'.format(**theme),
            {'simple': 'Total cost is the sum of all selected component costs.'},
            {'nl1': 'The total cost is calculated by adding up the prices of your selected {P1}, {P3}, {P5}, and {P7}.'.format(**theme)}
        )
        minimize = p.add_line(
            '#minimize { C : total_cost(C) }.',
            {'simple': 'Minimize total cost.'},
            {'nl1': 'Your goal is to minimize the total cost of your {verb}.'.format(**theme)}
        )
        p.add_group(
            [cost, minimize],
            {
                'nl1/2': 'The total cost is the sum of your selected {P1}, {P3}, {P5}, and {P7}. Minimize this cost for your {verb}.'.format(**theme)
            }
        )

        # Add variations for the theme
        p.add_variations(theme['variations'])
        programs.append(p)
    return programs

programs = generate_programs(theme_sets)

# Data generation setup
cnl_levels = {'simple': ['simple']}
nl_levels = {'nl1': ['nl1']}

for p in programs:
    dg = DataGenerator(p, splice_params='whole')
    dg.generate_data(cnl_levels=cnl_levels, nl_levels=nl_levels)
    dg.get_all_data()