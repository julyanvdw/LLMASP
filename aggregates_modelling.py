from AspPy2 import ASPProgram, DataGenerator
import json
import random

# MODULAR ASP AGGREGATES MODELING - Generate balanced training data for CNL->ASP
# Target: ~10k balanced CNL:ASP pairs for aggregates

# =============================================================================
# CATEGORY 1: COUNT AGGREGATE IN CONSTRAINT
# =============================================================================
p_count = ASPProgram()
p_count.add_line(
    ':- #count { ^X^ : ^body_pred^("^X^") } > ^N^.',
    {
        'simple': 'It is not allowed for more than ^N^ people to be ^body_pred^.',
        'variant1': 'There cannot be more than ^N^ ^body_pred^s.',
        'variant2': 'No answer set may have more than ^N^ people who are ^body_pred^.'
    }
)
p_count.add_line(
    ':- #count { ^X^ : ^body_pred^("^X^") } < ^N^.',
    {
        'simple': 'It is not allowed for fewer than ^N^ people to be ^body_pred^.',
        'variant1': 'There must be at least ^N^ ^body_pred^s.',
        'variant2': 'No answer set may have fewer than ^N^ people who are ^body_pred^.'
    }
)
count_variations = {
    'body_pred': [
        'enrolled', 'assigned', 'member', 'participant', 'selected',
        'approved', 'trusted', 'active', 'present', 'included'
    ],
    'X': [
        'alice', 'bob', 'charlie', 'john', 'mary', 'sam',
        'eve', 'zoe', 'lucas', 'oliver', 'mia', 'noah'
    ],
    'N': ['2', '3', '4', '5', '6', '7', '8'],
}
p_count.add_variations(count_variations)

# =============================================================================
# CATEGORY 2: SUM AGGREGATE IN CONSTRAINT
# =============================================================================
p_sum = ASPProgram()
p_sum.add_line(
    ':- #sum { ^S^, ^X^ : ^score_pred^("^X^", ^S^) } > ^N^.',
    {
        'simple': 'The total score of all people cannot be more than ^N^.',
        'variant1': 'It is not allowed for the sum of all scores to exceed ^N^.',
        'variant2': 'No answer set may have a total score greater than ^N^ for all people.'
    }
)
p_sum.add_line(
    ':- #sum { ^S^, ^X^ : ^score_pred^("^X^", ^S^) } < ^N^.',
    {
        'simple': 'The total score of all people cannot be less than ^N^.',
        'variant1': 'It is not allowed for the sum of all scores to be below ^N^.',
        'variant2': 'No answer set may have a total score less than ^N^ for all people.'
    }
)
sum_variations = {
    'score_pred': [
        'score', 'points', 'grade', 'mark', 'credit'
    ],
    'X': [
        'alice', 'bob', 'charlie', 'john', 'mary', 'sam',
        'eve', 'zoe', 'lucas', 'oliver', 'mia', 'noah'
    ],
    'S': ['S', 'P', 'G', 'M', 'C'],
    'N': ['50', '60', '70', '80', '90', '100', '120', '150'],
}
p_sum.add_variations(sum_variations)

# =============================================================================
# CATEGORY 3: MIN/MAX AGGREGATE IN CONSTRAINT
# =============================================================================
# Use only variables in the aggregate set, never constants/names.
# Remove S from variations, always use S as the score variable.
p_minmax = ASPProgram()
p_minmax.add_line(
    ':- #min { S : ^score_pred^("^X^", S) } < ^N^.',
    {
        'simple': 'The minimum score among all people must not be less than ^N^.',
        'variant1': 'No person can have a score below ^N^.',
        'variant2': 'It is not allowed for the lowest score to be less than ^N^ among all people.'
    }
)
p_minmax.add_line(
    ':- #max { S : ^score_pred^("^X^", S) } > ^N^.',
    {
        'simple': 'The maximum score among all people must not be greater than ^N^.',
        'variant1': 'No person can have a score above ^N^.',
        'variant2': 'It is not allowed for the highest score to be more than ^N^ among all people.'
    }
)
minmax_variations = {
    'score_pred': [
        'score', 'points', 'grade', 'mark', 'credit'
    ],
    # X is always a set of names, S is always the score variable
    'X': [
        'alice', 'bob', 'charlie', 'john', 'mary', 'sam',
        'eve', 'zoe', 'lucas', 'oliver', 'mia', 'noah'
    ],
    'N': ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100'],
}
p_minmax.add_variations(minmax_variations)

# =============================================================================
# CATEGORY 4: AGGREGATE IN RULE HEAD
# =============================================================================
p_head = ASPProgram()
p_head.add_line(
    '^pass_pred^("^X^") :- #sum { ^S^ : ^score_pred^("^X^", ^S^) } >= ^N^.',
    {
        'simple': '^X^ passes if their total score is at least ^N^.',
        'variant1': '^X^ is considered to have passed if the sum of their scores is at least ^N^.',
        'variant2': '^X^ will pass if their total score is greater than or equal to ^N^.'
    }
)
head_variations = {
    'pass_pred': ['passed', 'qualified', 'approved', 'successful'],
    'score_pred': ['score', 'points', 'grade', 'mark', 'credit'],
    'X': [
        'alice', 'bob', 'charlie', 'john', 'mary', 'sam',
        'eve', 'zoe', 'lucas', 'oliver', 'mia', 'noah'
    ],
    'S': ['S', 'P', 'G', 'M', 'C'],
    'N': ['40', '50', '60', '70', '80', '90', '100'],
}
p_head.add_variations(head_variations)

# =============================================================================
# CATEGORY 5: AGGREGATE WITH MULTIPLE CONDITIONS
# =============================================================================
p_multicond = ASPProgram()
p_multicond.add_line(
    ':- #count { ^X^ : ^body_pred1^("^X^"), ^body_pred2^("^X^") } < ^N^.',
    {
        'simple': 'There must be at least ^N^ people who are both ^body_pred1^ and ^body_pred2^.',
        'variant1': 'It is not allowed for fewer than ^N^ people to be both ^body_pred1^ and ^body_pred2^.',
        'variant2': 'No answer set may have less than ^N^ people who are both ^body_pred1^ and ^body_pred2^.'
    }
)
multicond_variations = {
    'body_pred1': [
        'enrolled', 'assigned', 'member', 'participant', 'selected',
        'approved', 'trusted', 'active', 'present', 'included'
    ],
    'body_pred2': [
        'verified', 'confirmed', 'registered', 'qualified', 'accepted',
        'enrolled', 'approved', 'checked', 'present', 'included'
    ],
    'X': [
        'alice', 'bob', 'charlie', 'john', 'mary', 'sam',
        'eve', 'zoe', 'lucas', 'oliver', 'mia', 'noah'
    ],
    'N': ['2', '3', '4', '5', '6', '7', '8'],
}
p_multicond.add_variations(multicond_variations)

# =============================================================================
# GENERATE BALANCED DATA FOR AGGREGATES
# =============================================================================

programs = [
    ("count", p_count, "count aggregate in constraint"),
    ("sum", p_sum, "sum aggregate in constraint"),
    ("minmax", p_minmax, "min/max aggregate in constraint"),
    ("head", p_head, "aggregate in rule head"),
    ("multicond", p_multicond, "aggregate with multiple conditions"),
]

cnl_levels = {
    'simple': ['simple'],
    'variant1': ['variant1'],
    'variant2': ['variant2']
}

nl_levels = {
    'basic': ['simple']
}

splice_params = {
    'strategy': 'multi_granularity',
    'min_size': 1,
    'max_size': 3,
    'window_type': 'random',
    'random_samples': 4,
    'randomised_order': True
}

print("ASP AGGREGATES MODELING - Generating Balanced CNL->ASP Training Data")
print("="*70)

total_generated = 0
all_cnl_asp_pairs = set()
program_stats = []

target_total = 10000
target_per_program = target_total // len(programs)

for prog_name, program, description in programs:
    print(f"\nProcessing {prog_name.upper()} ({description}):")
    variations = program.get_variations()
    total_variations = 1
    for key, values in variations.items():
        total_variations *= len(values)
    print(f"  Lines: {len(program.lines)}")
    print(f"  Variation categories: {len(variations)}")
    print(f"  Total combinations: {total_variations:,}")
    dg = DataGenerator(program, splice_params)
    dg.generate_data(cnl_levels, nl_levels)
    prog_cnl_asp = len(dg.cnl_asp_set)
    print(f"  Generated unique CNL:ASP pairs: {prog_cnl_asp:,}")
    if prog_cnl_asp > target_per_program:
        sampled_pairs = random.sample(list(dg.cnl_asp_set), target_per_program)
        print(f"  Sampled down to: {target_per_program:,}")
        all_cnl_asp_pairs.update(sampled_pairs)
        actual_added = target_per_program
    else:
        all_cnl_asp_pairs.update(dg.cnl_asp_set)
        actual_added = prog_cnl_asp
    program_stats.append((prog_name, actual_added, description))
    total_generated += actual_added

print(f"\n" + "="*70)
print("FINAL SUMMARY")
print("="*70)
print(f"Total unique CNL:ASP pairs generated: {len(all_cnl_asp_pairs):,}")
print(f"Total entries across all programs: {total_generated:,}")

print(f"\nBreakdown by program:")
for prog_name, count, desc in program_stats:
    percentage = (count / total_generated) * 100
    print(f"  {prog_name:12}: {count:4,} pairs ({percentage:5.1f}%) - {desc}")

print(f"\nSample CNL:ASP pairs:")
sample_pairs = random.sample(list(all_cnl_asp_pairs), min(8, len(all_cnl_asp_pairs)))
for i, (cnl, asp) in enumerate(sample_pairs, 1):
    print(f"\nExample {i}:")
    print(f"  CNL: {cnl}")
    print(f"  ASP: {asp}")

output_file = "comprehensive_aggregates_cnl_to_asp_10k.jsonl"
print(f"\nExporting to {output_file}...")

pairs_list = list(all_cnl_asp_pairs)
random.shuffle(pairs_list)
with open(output_file, "w", encoding="utf-8") as f:
    for cnl, asp in pairs_list:
        obj = {
            "instruction": "Translate this controlled natural language description to ASP code",
            "input": cnl,
            "output": asp
        }
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

print(f"Successfully exported {len(all_cnl_asp_pairs):,} balanced CNL:ASP pairs to {output_file}.")