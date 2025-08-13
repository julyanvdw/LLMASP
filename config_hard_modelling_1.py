from AspPy2 import ASPProgram, DataGenerator
import random
import json

theme_sets = [
    {
        'P1': 'cpu',
        'P2': 'selected_cpu',
        'P3': 'gpu',
        'P4': 'selected_gpu',
        'P5': 'storage',
        'P6': 'selected_storage',
        'P7': 'cost',
        'P8': 'perf',
        'P9': 'selected',
        'P10': 'max_cost',
        'P11': 'max_perf',
        'P12': 'top_cpu',
        'P13': 'top_gpu',
        'P14': 'top_storage',
        'theme': 'High-End Workstation',
        'verb': 'configuration',
        'variations': {
            'V1': ['X9'],
            'V1b': ['ZetaCore'],
            'V1c': ['Alpha8'],
            'V2': ['QuasarRTX'],
            'V2b': ['NovaX'],
            'V2c': ['GammaGTX'],
            'V3': ['UltraSSD'],
            'V3b': ['MegaHDD'],
            'V3c': ['FusionDrive'],
            'C1': ['300'],
            'C1b': ['500'],
            'C1c': ['450'],
            'C2': ['700'],
            'C2b': ['600'],
            'C2c': ['450'],
            'C3': ['250'],
            'C3b': ['200'],
            'C3c': ['300'],
            'P1_perf': ['95'],
            'P1b_perf': ['120'],
            'P1c_perf': ['110'],
            'P2_perf': ['130'],
            'P2b_perf': ['125'],
            'P2c_perf': ['90'],
            'P3_perf': ['100'],
            'P3b_perf': ['60'],
            'P3c_perf': ['95']
        }
    }
]

def generate_programs(theme_sets):
    programs = []
    for theme in theme_sets:
        p = ASPProgram()

        # Components (all 3 options for each)
        cpu = p.add_line(
            '{P1}("^V1^"; "^V1b^"; "^V1c^").'.format(**theme),
            {'simple': '{P1}s: ^V1^, ^V1b^, ^V1c^.'.format(**theme)},
            {'nl1': 'Available {P1}s are ^V1^, ^V1b^, and ^V1c^.'.format(**theme)}
        )
        gpu = p.add_line(
            '{P3}("^V2^"; "^V2b^"; "^V2c^").'.format(**theme),
            {'simple': '{P3}s: ^V2^, ^V2b^, ^V2c^.'.format(**theme)},
            {'nl1': 'Available {P3}s are ^V2^, ^V2b^, and ^V2c^.'.format(**theme)}
        )
        storage = p.add_line(
            '{P5}("^V3^"; "^V3b^"; "^V3c^").'.format(**theme),
            {'simple': '{P5}: ^V3^, ^V3b^, ^V3c^.'.format(**theme)},
            {'nl1': 'Available {P5} devices are ^V3^, ^V3b^, and ^V3c^.'.format(**theme)}
        )

        p.add_group(
            [cpu, gpu, storage],
            {
                'nl1/2': 'The available components for your {verb} are: {P1}s (^V1^, ^V1b^, ^V1c^), {P3}s (^V2^, ^V2b^, ^V2c^), and {P5} devices (^V3^, ^V3b^, ^V3c^).'.format(**theme),
                'nl2/2': 'You can choose from three {P1}s, three {P3}s, and three {P5} devices for your {verb}.'.format(**theme)
            }
        )


        # Selection constraints
        cpu_choice = p.add_line(
            '1 { {P2}(C) : {P1}(C) } 1.'.format(**theme),
            {'simple': 'Pick one {P1}.' .format(**theme)},
            {'nl1': 'Select exactly one {P1}.' .format(**theme)}
        )
        gpu_choice = p.add_line(
            '1 { {P4}(G) : {P3}(G) } 1.'.format(**theme),
            {'simple': 'Pick one {P3}.' .format(**theme)},
            {'nl1': 'Select exactly one {P3}.' .format(**theme)}
        )
        storage_choice = p.add_line(
            '1 { {P6}(S) : {P5}(S) } 1.'.format(**theme),
            {'simple': 'Pick one {P5}.' .format(**theme)},
            {'nl1': 'Select exactly one {P5} device.' .format(**theme)}
        )

        p.add_group(
            [cpu_choice, gpu_choice, storage_choice],
            {
                'nl1/2': 'You must select exactly one {P1}, one {P3}, and one {P5} device for your {verb}.'.format(**theme),
                'nl2/2': 'Choose a single {P1}, {P3}, and {P5} from the available options to complete your {verb}.'.format(**theme)
            }
        ) 

        # Cost 
        cpu_cost = p.add_line(
            '{P7}("^V1^", ^C1^; "^V1b^", ^C1b^; "^V1c^", ^C1c^).'.format(**theme),
            {'simple': '{P1} costs: ^V1^=^C1^, ^V1b^=^C1b^, ^V1c^=^C1c^.' .format(**theme)},
            {'nl1': '{P1} costs are ^V1^: ^C1^, ^V1b^: ^C1b^, ^V1c^: ^C1c^.' .format(**theme)}
        )
        gpu_cost = p.add_line(
            '{P7}("^V2^", ^C2^; "^V2b^", ^C2b^; "^V2c^", ^C2c^).'.format(**theme),
            {'simple': '{P3} costs: ^V2^=^C2^, ^V2b^=^C2b^, ^V2c^=^C2c^.' .format(**theme)},
            {'nl1': '{P3} costs are ^V2^: ^C2^, ^V2b^: ^C2b^, ^V2c^: ^C2c^.' .format(**theme)}
        )
        storage_cost = p.add_line(
            '{P7}("^V3^", ^C3^; "^V3b^", ^C3b^; "^V3c^", ^C3c^).'.format(**theme),
            {'simple': '{P5} costs: ^V3^=^C3^, ^V3b^=^C3b^, ^V3c^=^C3c^.' .format(**theme)},
            {'nl1': '{P5} costs are ^V3^: ^C3^, ^V3b^: ^C3b^, ^V3c^: ^C3c^.' .format(**theme)}
        )

        p.add_group(
            [cpu_cost, gpu_cost, storage_cost],
            {
                'nl1/6': (
                    '{P1} costs: ^V1^ (^C1^), ^V1b^ (^C1b^), ^V1c^ (^C1c^); '
                    '{P3} costs: ^V2^ (^C2^), ^V2b^ (^C2b^), ^V2c^ (^C2c^); '
                    '{P5} costs: ^V3^ (^C3^), ^V3b^ (^C3b^), ^V3c^ (^C3c^).'
                ).format(**theme),
                'nl2/6': (
                    'Each {P1}, {P3}, and {P5} device has an associated cost: '
                    '{P1}s (^V1^: ^C1^, ^V1b^: ^C1b^, ^V1c^: ^C1c^), '
                    '{P3}s (^V2^: ^C2^, ^V2b^: ^C2b^, ^V2c^: ^C2c^), '
                    '{P5}s (^V3^: ^C3^, ^V3b^: ^C3b^, ^V3c^: ^C3c^).'
                ).format(**theme)
            }
        )

        # Performance

        cpu_perf = p.add_line(
            '{P8}("^V1^", ^P1_perf^; "^V1b^", ^P1b_perf^; "^V1c^", ^P1c_perf^).'.format(**theme),
            {'simple': '{P1} performance: ^V1^=^P1_perf^, ^V1b^=^P1b_perf^, ^V1c^=^P1c_perf^.' .format(**theme)},
            {'nl1': '{P1} performance: ^V1^: ^P1_perf^, ^V1b^: ^P1b_perf^, ^V1c^: ^P1c_perf^.' .format(**theme)}
        )
        gpu_perf = p.add_line(
            '{P8}("^V2^", ^P2_perf^; "^V2b^", ^P2b_perf^; "^V2c^", ^P2c_perf^).'.format(**theme),
            {'simple': '{P3} performance: ^V2^=^P2_perf^, ^V2b^=^P2b_perf^, ^V2c^=^P2c_perf^.' .format(**theme)},
            {'nl1': '{P3} performance: ^V2^: ^P2_perf^, ^V2b^: ^P2b_perf^, ^V2c^: ^P2c_perf^.' .format(**theme)}
        )
        storage_perf = p.add_line(
            '{P8}("^V3^", ^P3_perf^; "^V3b^", ^P3b_perf^; "^V3c^", ^P3c_perf^).'.format(**theme),
            {'simple': '{P5} performance: ^V3^=^P3_perf^, ^V3b^=^P3b_perf^, ^V3c^=^P3c_perf^.' .format(**theme)},
            {'nl1': '{P5} performance: ^V3^: ^P3_perf^, ^V3b^: ^P3b_perf^, ^V3c^: ^P3c_perf^.' .format(**theme)}
        )

        p.add_group(
            [cpu_perf, gpu_perf, storage_perf],
            {
                'nl1/6': (
                    '{P1} performance: ^V1^ (^P1_perf^), ^V1b^ (^P1b_perf^), ^V1c^ (^P1c_perf^); '
                    '{P3} performance: ^V2^ (^P2_perf^), ^V2b^ (^P2b_perf^), ^V2c^ (^P2c_perf^); '
                    '{P5} performance: ^V3^ (^P3_perf^), ^V3b^ (^P3b_perf^), ^V3c^ (^P3c_perf^).'
                ).format(**theme),
                'nl2/6': (
                    'Each {P1}, {P3}, and {P5} device has a performance rating: '
                    '{P1}s (^V1^: ^P1_perf^, ^V1b^: ^P1b_perf^, ^V1c^: ^P1c_perf^), '
                    '{P3}s (^V2^: ^P2_perf^, ^V2b^: ^P2b_perf^, ^V2c^: ^P2c_perf^), '
                    '{P5}s (^V3^: ^P3_perf^, ^V3b^: ^P3b_perf^, ^V3c^: ^P3c_perf^).'
                ).format(**theme)
            }
        )

        # Constraints - The most expensive selected component must also be the one with the highest performance among selected parts.
        selected_cpu_union = p.add_line(
            '{P9}(X) :- {P2}(X).'.format(**theme),
            {'simple': '{P9} includes all selected {P1}.' .format(**theme)},
            {'nl1': '{P9} includes any {P1} that is selected.' .format(**theme)}
        )
        selected_gpu_union = p.add_line(
            '{P9}(X) :- {P4}(X).'.format(**theme),
            {'simple': '{P9} includes all selected {P3}.' .format(**theme)},
            {'nl1': '{P9} includes any {P3} that is selected.' .format(**theme)}
        )
        selected_storage_union = p.add_line(
            '{P9}(X) :- {P6}(X).'.format(**theme),
            {'simple': '{P9} includes all selected {P5}.' .format(**theme)},
            {'nl1': '{P9} includes any {P5} that is selected.' .format(**theme)}
        )

        max_cost = p.add_line(
            '{P10}(C) :- {P7}(C, V), V = #max {{V1 : {P7}(C1, V1), {P9}(C1)}}.'.format(**theme),
            {'simple': '{P10} is true for the selected component with the highest cost.'.format(**theme)},
            {'nl1': '{P10} marks the selected part with the highest cost among your choices.'.format(**theme)}
        )
        max_perf = p.add_line(
            '{P11}(C) :- {P8}(C, V), V = #max {{V1 : {P8}(C1, V1), {P9}(C1)}}.'.format(**theme),
            {'simple': '{P11} is true for the selected component with the highest performance.'.format(**theme)},
            {'nl1': '{P11} marks the selected part with the highest performance among your choices.'.format(**theme)}
        )
        expensive_perf_constraint = p.add_line(
            ':- {P9}(C), {P10}(C), not {P11}(C).'.format(**theme),
            {'simple': 'The most expensive selected component must also be the one with the highest performance.'},
            {'nl1': 'The most expensive selected part must also be the highest performing among your choices.'}
        )

        p.add_group(
            [
                selected_cpu_union,
                selected_gpu_union,
                selected_storage_union,
                max_cost,
                max_perf,
                expensive_perf_constraint
            ],
            {
                'nl1/6': (
                    'First, all selected {P1}, {P3}, and {P5} devices are grouped as {P9}. '
                    '{P10} marks the selected component with the highest cost, and {P11} marks the one with the highest performance. '
                    'It is required that the most expensive selected component is also the highest performing among your choices.'
                ).format(**theme),
                'nl2/6': (
                    'After you select your {P1}, {P3}, and {P5}, they are all considered as {P9}. '
                    '{P10} identifies which selected part is the most expensive, and {P11} identifies the highest performing part. '
                    'You must ensure that the most expensive part you select is also the one with the highest performance.'
                ).format(**theme)
            }
        )

        # You may not select all three top-performing components.
        
        top_cpu = p.add_line(
            '{P12}(C) :- {P1}(C), {P8}(C, V), V = #max {{V1 : {P8}(C1, V1), {P1}(C1)}}.'.format(**theme),
            {'simple': '{P12} is true for the {P1} with the highest performance.'.format(**theme)},
            {'nl1': '{P12} marks the {P1} with the highest performance.'.format(**theme)}
        )
        top_gpu = p.add_line(
            '{P13}(C) :- {P3}(C), {P8}(C, V), V = #max {{V1 : {P8}(C1, V1), {P3}(C1)}}.'.format(**theme),
            {'simple': '{P13} is true for the {P3} with the highest performance.'.format(**theme)},
            {'nl1': '{P13} marks the {P3} with the highest performance.'.format(**theme)}
        )
        top_storage = p.add_line(
            '{P14}(C) :- {P5}(C), {P8}(C, V), V = #max {{V1 : {P8}(C1, V1), {P5}(C1)}}.'.format(**theme),
            {'simple': '{P14} is true for the {P5} with the highest performance.'.format(**theme)},
            {'nl1': '{P14} marks the {P5} with the highest performance.'.format(**theme)}
        )
        no_all_top_constraint = p.add_line(
            ':- {P2}(C), {P12}(C), {P4}(G), {P13}(G), {P6}(S), {P14}(S).'.format(**theme),
            {'simple': 'You may not select all three top-performing components.'},
            {'nl1': 'You cannot select the highest performing {P1}, {P3}, and {P5} all at once.'.format(**theme)}
        )

        p.add_group(
            [top_cpu, top_gpu, top_storage, no_all_top_constraint],
            {
                'nl1/6': (
                    '{P12} marks the {P1} with the highest performance (^V1^: ^P1_perf^, ^V1b^: ^P1b_perf^, ^V1c^: ^P1c_perf^); '
                    '{P13} marks the {P3} with the highest performance (^V2^: ^P2_perf^, ^V2b^: ^P2b_perf^, ^V2c^: ^P2c_perf^); '
                    '{P14} marks the {P5} with the highest performance (^V3^: ^P3_perf^, ^V3b^: ^P3b_perf^, ^V3c^: ^P3c_perf^). '
                    'You cannot select the highest performing {P1}, {P3}, and {P5} all at once.'
                ).format(**theme),
                'nl2/6': (
                    'For each component type, the top performer is identified: '
                    '{P1} (^V1^: ^P1_perf^, ^V1b^: ^P1b_perf^, ^V1c^: ^P1c_perf^), '
                    '{P3} (^V2^: ^P2_perf^, ^V2b^: ^P2b_perf^, ^V2c^: ^P2c_perf^), '
                    '{P5} (^V3^: ^P3_perf^, ^V3b^: ^P3b_perf^, ^V3c^: ^P3c_perf^). '
                    'It is not allowed to select all three top-performing devices together.'
                ).format(**theme)
            }
        )

        # 
        cost_diff = p.add_line(
            ':- {P9}(C1), {P9}(C2), {P7}(C1, V1), {P7}(C2, V2), V1 - 250 >= V2.'.format(**theme),
            {'simple': 'No two selected components may differ in cost by more than 250.'},
            {'nl1': 'The cost difference between any two selected parts must not exceed 250.'}
        )
        gpu_cpu_perf = p.add_line(
            ':- {P2}(C), {P4}(G), {P8}(C, PC), {P8}(G, PG), PG > PC.'.format(**theme),
            {'simple': 'The selected {P3} must not have higher performance than the selected {P1}.' .format(**theme)},
            {'nl1': 'Your {P3} cannot outperform your {P1}.' .format(**theme)}
        )
        alpha8_novax = p.add_line(
            ':- {P2}("Alpha8"), {P4}("NovaX").'.format(**theme),
            {'simple': 'Alpha8 is incompatible with NovaX.'},
            {'nl1': 'Alpha8 {P1} cannot be used with NovaX {P3}.' .format(**theme)}
        )
        fusiondrive_zetacore = p.add_line(
            ':- {P6}("FusionDrive"), not {P2}("ZetaCore").'.format(**theme),
            {'simple': 'FusionDrive can only be used with ZetaCore.'},
            {'nl1': 'FusionDrive {P5} is only available if ZetaCore {P1} is selected.' .format(**theme)}
        )

    

        p.add_variations(theme['variations'])
        programs.append(p)
    return programs

# CNL/NL levels
cnl_levels = {
    'simple': ['simple']
}
nl_levels = {
    'nl1': ['nl1'],
    'nl2': ['nl2'],
    'nl3': ['nl3'],
    'nl1/2': ['nl1/2'],
    'nl2/2': ['nl2/2'],
    'nl1/6': ['nl1/6'],
    'nl2/6': ['nl2/6']
}

programs = generate_programs(theme_sets)

splice_params = {
    'strategy': 'multi_granularity',
    'min_size': 1,
    'max_size': 9,
    'window_type': 'random',
    'random_samples': 2,
    'randomised_order': True
}

target_total = 20000
target_per_program = target_total // len(programs)

all_cnl_asp_pairs = set()
all_nl_cnl_pairs = set()
cnl_asp_stats = []
nl_cnl_stats = []

for idx, p in enumerate(programs):
    print(f"\nProcessing THEME {idx+1} ({theme_sets[idx]['theme']}):")
    variations = p.get_variations()
    total_variations = 1
    for key, values in variations.items():
        total_variations *= len(values)
    print(f"  Lines: {len(p.lines)}")
    print(f"  Variation categories: {len(variations)}")
    print(f"  Total combinations: {total_variations:,}")

    dg = DataGenerator(p, splice_params)
    dg.generate_data(cnl_levels=cnl_levels, nl_levels=nl_levels)

    # --- CNL:ASP ---
    prog_cnl_asp = len(dg.cnl_asp_set)
    print(f"  Generated unique CNL:ASP pairs: {prog_cnl_asp:,}")
    if prog_cnl_asp > target_per_program:
        sampled_cnl_asp = random.sample(list(dg.cnl_asp_set), target_per_program)
        all_cnl_asp_pairs.update(sampled_cnl_asp)
        actual_cnl_asp = target_per_program
    else:
        all_cnl_asp_pairs.update(dg.cnl_asp_set)
        actual_cnl_asp = prog_cnl_asp
    cnl_asp_stats.append((theme_sets[idx]['theme'], actual_cnl_asp))

    # --- NL:CNL ---
    prog_nl_cnl = len(dg.nl_cnl_set)
    print(f"  Generated unique NL:CNL pairs: {prog_nl_cnl:,}")
    if prog_nl_cnl > target_per_program:
        sampled_nl_cnl = random.sample(list(dg.nl_cnl_set), target_per_program)
        all_nl_cnl_pairs.update(sampled_nl_cnl)
        actual_nl_cnl = target_per_program
    else:
        all_nl_cnl_pairs.update(dg.nl_cnl_set)
        actual_nl_cnl = prog_nl_cnl
    nl_cnl_stats.append((theme_sets[idx]['theme'], actual_nl_cnl))

# --- OUTPUT STATS ---
print(f"\n{'='*70}\nFINAL SUMMARY\n{'='*70}")
print(f"Total unique CNL:ASP pairs generated: {len(all_cnl_asp_pairs):,}")
print(f"Total unique NL:CNL pairs generated: {len(all_nl_cnl_pairs):,}")

print(f"\nBreakdown by theme (CNL:ASP):")
for theme, count in cnl_asp_stats:
    print(f"  {theme:16}: {count:4,} pairs")

print(f"\nBreakdown by theme (NL:CNL):")
for theme, count in nl_cnl_stats:
    print(f"  {theme:16}: {count:4,} pairs")

# --- EXPORT ---
output_cnl_asp = "hard_config_cnl_to_asp_20k.jsonl"
output_nl_cnl = "hard_config_nl_to_cnl_20k.jsonl"

print(f"\nExporting CNL:ASP to {output_cnl_asp}...")
pairs_list = list(all_cnl_asp_pairs)
random.shuffle(pairs_list)
with open(output_cnl_asp, "w", encoding="utf-8") as f:
    for cnl, asp in pairs_list:
        obj = {
            "instruction": "Translate this controlled natural language description to ASP code",
            "input": cnl,
            "output": asp
        }
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
print(f"Successfully exported {len(all_cnl_asp_pairs):,} CNL:ASP pairs")

print(f"\nExporting NL:CNL to {output_nl_cnl}...")
pairs_list = list(all_nl_cnl_pairs)
random.shuffle(pairs_list)
with open(output_nl_cnl, "w", encoding="utf-8") as f:
    for nl, cnl in pairs_list:
        obj = {
            "instruction": "Convert this natural language statement to controlled natural language",
            "input": nl,
            "output": cnl
        }
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
print(f"Successfully exported {len(all_nl_cnl_pairs):,} NL:CNL pairs")

print("Hard config modelling complete!")