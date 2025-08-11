from AspPy2 import ASPProgram, DataGenerator
import json
import random

# MODULAR ASP CHOICE RULES MODELING - Generate balanced training data for CNL->ASP
# Target: ~10k balanced CNL:ASP pairs for choice rules

# =============================================================================
# CATEGORY 1: UNBOUNDED CHOICE WITH CONDITION LITERAL
# =============================================================================
p_unbounded = ASPProgram()
p_unbounded.add_line(
    '{ ^head_pred^("^X^") : ^body_pred^("^X^") }.',
    {
        'simple': '^X^ can be ^head_pred^ if ^X^ is ^body_pred^, but it is optional.',
        'variant1': 'For each ^X^ that is ^body_pred^, it is possible for ^X^ to be ^head_pred^.',
        'variant2': 'Any ^X^ who is ^body_pred^ may or may not be ^head_pred^.'
    }
)
unbounded_variations = {
    'head_pred': [
        'assigned', 'trusted', 'approved', 'active', 'reachable',
        'flagged', 'selected', 'chosen', 'included', 'marked'
    ],
    'body_pred': [
        'eligible', 'member', 'person', 'applicant', 'node',
        'participant', 'candidate', 'student', 'object', 'user'
    ],
    'X': [
        'alice', 'bob', 'charlie', 'john', 'mary', 'sam',
        'eve', 'zoe', 'lucas', 'oliver', 'mia', 'noah'
    ],
}
p_unbounded.add_variations(unbounded_variations)

# =============================================================================
# CATEGORY 2: CHOICE RULE WITH BODY
# =============================================================================
p_body = ASPProgram()
p_body.add_line(
    '{ ^head_pred^("^X^") } :- ^body_pred^("^X^").',
    {
        'simple': 'If ^X^ is ^body_pred^, then ^X^ might be ^head_pred^.',
        'variant1': 'Whenever ^X^ is ^body_pred^, ^X^ could be ^head_pred^.',
        'variant2': '^X^ is allowed to be ^head_pred^ if ^X^ is ^body_pred^.'
    }
)
body_variations = {
    'head_pred': [
        'assigned', 'trusted', 'approved', 'active', 'reachable',
        'flagged', 'selected', 'chosen', 'included', 'marked'
    ],
    'body_pred': [
        'eligible', 'member', 'person', 'applicant', 'node',
        'participant', 'candidate', 'student', 'object', 'user'
    ],
    'X': [
        'alice', 'bob', 'charlie', 'john', 'mary', 'sam',
        'eve', 'zoe', 'lucas', 'oliver', 'mia', 'noah'
    ],
}
p_body.add_variations(body_variations)

# =============================================================================
# CATEGORY 3: CHOICE RULE WITH EXPLICIT ATOMS
# =============================================================================
p_explicit = ASPProgram()
p_explicit.add_line(
    '{ ^head_pred1^("^X^"); ^head_pred2^("^X^") } :- ^body_pred^("^X^").',
    {
        'simple': 'If ^X^ is ^body_pred^, then ^X^ can be ^head_pred1^, ^head_pred2^, both, or neither.',
        'variant1': 'Whenever ^X^ is ^body_pred^, ^X^ may be ^head_pred1^, ^head_pred2^, both, or neither.',
        'variant2': '^X^ could be ^head_pred1^ or ^head_pred2^ if ^X^ is ^body_pred^.'
    }
)
explicit_variations = {
    'head_pred1': [
        'red', 'trusted', 'approved', 'active', 'reachable',
        'flagged', 'selected', 'chosen', 'included', 'marked'
    ],
    'head_pred2': [
        'blue', 'banned', 'pending', 'inactive', 'blocked',
        'excluded', 'removed', 'untrusted', 'waiting', 'absent'
    ],
    'body_pred': [
        'object', 'member', 'person', 'applicant', 'node',
        'participant', 'candidate', 'student', 'user', 'item'
    ],
    'X': [
        'alice', 'bob', 'charlie', 'john', 'mary', 'sam',
        'eve', 'zoe', 'lucas', 'oliver', 'mia', 'noah'
    ],
}
p_explicit.add_variations(explicit_variations)

# =============================================================================
# CATEGORY 4: CHOICE RULE WITH BOUNDS
# =============================================================================
p_bounds = ASPProgram()
p_bounds.add_line(
    '^L^ { ^head_pred^("^X^", "^Y^") : ^body_pred^("^Y^") } ^U^ :- ^body_pred2^("^X^").',
    {
        'simple': 'If ^X^ is ^body_pred2^, then ^X^ can be ^head_pred^ of at least ^L^ and at most ^U^ different ^Y^s who are ^body_pred^.',
        'variant1': 'Whenever ^X^ is ^body_pred2^, ^X^ may be ^head_pred^ of between ^L^ and ^U^ ^Y^s that are ^body_pred^.',
        'variant2': 'For each ^X^ that is ^body_pred2^, ^X^ is allowed to be ^head_pred^ of some ^Y^s who are ^body_pred^, with the number between ^L^ and ^U^.'
    }
)
bounds_variations = {
    'head_pred': [
        'assigned', 'trusted', 'approved', 'active', 'reachable',
        'flagged', 'selected', 'chosen', 'included', 'marked'
    ],
    'body_pred': [
        'eligible', 'member', 'person', 'applicant', 'node',
        'participant', 'candidate', 'student', 'object', 'user'
    ],
    'body_pred2': [
        'employee', 'manager', 'supervisor', 'teacher',
        'coach', 'leader', 'director', 'instructor'
    ],
    'L': ['1', '2', '3'],
    'U': ['2', '3', '4'],
    # Disjoint X and Y
    'X': ['alice', 'bob', 'charlie', 'john', 'lucas', 'oliver'],
    'Y': ['mary', 'sam', 'eve', 'zoe', 'mia', 'noah'],
}
p_bounds.add_variations(bounds_variations)

# =============================================================================
# CATEGORY 5: CHOICE RULE WITH CONSTANTS
# =============================================================================
p_const = ASPProgram()
p_const.add_line(
    '{ ^head_pred1^("^C^"); ^head_pred2^("^C^") }.',
    {
        'simple': '^C^ can be ^head_pred1^, ^head_pred2^, both, or neither.',
        'variant1': 'It is possible for ^C^ to be ^head_pred1^, ^head_pred2^, both, or neither.',
        'variant2': '^C^ may be ^head_pred1^ or ^head_pred2^, or even both or neither.'
    }
)
const_variations = {
    'head_pred1': [
        'admin', 'trusted', 'approved', 'active', 'reachable',
        'flagged', 'selected', 'chosen', 'included', 'marked'
    ],
    'head_pred2': [
        'manager', 'banned', 'pending', 'inactive', 'blocked',
        'excluded', 'removed', 'untrusted', 'waiting', 'absent'
    ],
    # Disjoint C and X for all constant-based rules
    'C': ['john', 'mary', 'eve', 'zoe', 'lucas', 'oliver', 'mia', 'noah'],
}
p_const.add_variations(const_variations)

# =============================================================================
# CATEGORY 6: CHOICE RULE WITH MULTIPLE BODY LITERALS
# =============================================================================
p_multibody = ASPProgram()
p_multibody.add_line(
    '{ ^head_pred^("^X^") } :- ^body_pred1^("^X^"), ^body_pred2^("^X^").',
    {
        'simple': 'If ^X^ is both ^body_pred1^ and ^body_pred2^, then ^X^ might be ^head_pred^.',
        'variant1': 'Whenever ^X^ is both ^body_pred1^ and ^body_pred2^, ^X^ could be ^head_pred^.',
        'variant2': '^X^ is allowed to be ^head_pred^ if ^X^ is both ^body_pred1^ and ^body_pred2^.'
    }
)
multibody_variations = {
    'head_pred': [
        'trusted', 'approved', 'active', 'reachable',
        'flagged', 'selected', 'chosen', 'included', 'marked'
    ],
    'body_pred1': [
        'member', 'person', 'applicant', 'node',
        'participant', 'candidate', 'student', 'object', 'user', 'item'
    ],
    'body_pred2': [
        'verified', 'confirmed', 'registered', 'qualified',
        'accepted', 'enrolled', 'approved', 'checked'
    ],
    'X': [
        'alice', 'bob', 'charlie', 'john', 'mary', 'sam',
        'eve', 'zoe', 'lucas', 'oliver', 'mia', 'noah'
    ],
}
p_multibody.add_variations(multibody_variations)

# =============================================================================
# CATEGORY 7: CHOICE RULE WITH DIFFERENT VARIABLES (disjoint sets)
# =============================================================================
p_diffvar = ASPProgram()
p_diffvar.add_line(
    '{ ^head_pred^("^X^", "^Y^") } :- ^body_pred1^("^X^"), ^body_pred2^("^Y^").',
    {
        'simple': 'If ^X^ is ^body_pred1^ and ^Y^ is ^body_pred2^, then ^X^ may be ^head_pred^ of ^Y^.',
        'variant1': 'Whenever ^X^ is ^body_pred1^ and ^Y^ is ^body_pred2^, ^X^ could be ^head_pred^ of ^Y^.',
        'variant2': '^X^ is allowed to be ^head_pred^ of ^Y^ if ^X^ is ^body_pred1^ and ^Y^ is ^body_pred2^.'
    }
)
diffvar_variations = {
    'head_pred': [
        'parent', 'manager', 'supervisor', 'friend',
        'colleague', 'partner', 'rival', 'mentor'
    ],
    'body_pred1': [
        'candidate', 'teacher', 'employee', 'applicant',
        'leader', 'director', 'coach', 'instructor'
    ],
    'body_pred2': [
        'child', 'student', 'member', 'person',
        'participant', 'user', 'trainee', 'mentee'
    ],
    # Disjoint X and Y
    'X': ['alice', 'bob', 'charlie', 'john', 'lucas', 'oliver'],
    'Y': ['mary', 'sam', 'eve', 'zoe', 'mia', 'noah'],
}
p_diffvar.add_variations(diffvar_variations)

# =============================================================================
# GENERATE BALANCED DATA FOR CHOICE RULES
# =============================================================================

programs = [
    ("unbounded", p_unbounded, "unbounded choice with condition literal"),
    ("body", p_body, "choice rule with body"),
    ("explicit", p_explicit, "choice rule with explicit atoms"),
    ("bounds", p_bounds, "choice rule with bounds"),
    ("const", p_const, "choice rule with constants"),
    ("multibody", p_multibody, "choice rule with multiple body literals"),
    ("diffvar", p_diffvar, "choice rule with different variables"),
]

# CNL levels - focusing on CNL->ASP translation
cnl_levels = {
    'simple': ['simple'],
    'variant1': ['variant1'],
    'variant2': ['variant2']
}

nl_levels = {
    'basic': ['simple']  # Not used, but required by framework
}

# Balanced splice params to get good variety without explosion
splice_params = {
    'strategy': 'multi_granularity',
    'min_size': 1,
    'max_size': 3,  # Allow up to 3 rules per program for variety
    'window_type': 'random',
    'random_samples': 4,  # Keep samples controlled
    'randomised_order': True
}

print("ASP CHOICE RULES MODELING - Generating Balanced CNL->ASP Training Data")
print("="*70)

total_generated = 0
all_cnl_asp_pairs = set()
program_stats = []

target_total = 10000
target_per_program = target_total // len(programs)

for prog_name, program, description in programs:
    print(f"\nProcessing {prog_name.upper()} ({description}):")
    
    # Calculate potential combinations
    variations = program.get_variations()
    total_variations = 1
    for key, values in variations.items():
        total_variations *= len(values)
    
    print(f"  Lines: {len(program.lines)}")
    print(f"  Variation categories: {len(variations)}")
    print(f"  Total combinations: {total_variations:,}")
    
    # Generate data
    dg = DataGenerator(program, splice_params)
    dg.generate_data(cnl_levels, nl_levels)
    
    prog_cnl_asp = len(dg.cnl_asp_set)
    print(f"  Generated unique CNL:ASP pairs: {prog_cnl_asp:,}")
    
    # Sample to target size if we have too many
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

# Show sample pairs
print(f"\nSample CNL:ASP pairs:")
sample_pairs = random.sample(list(all_cnl_asp_pairs), min(8, len(all_cnl_asp_pairs)))
for i, (cnl, asp) in enumerate(sample_pairs, 1):
    print(f"\nExample {i}:")
    print(f"  CNL: {cnl}")
    print(f"  ASP: {asp}")

# Export the final balanced dataset
output_file = "comprehensive_choice_rules_cnl_to_asp_10k.jsonl"
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

print(f"Successfully exported {len(all_cnl_asp_pairs):,} balanced CNL:ASP pairs")
print("Modeling complete.")