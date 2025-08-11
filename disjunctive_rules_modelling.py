from AspPy2 import ASPProgram, DataGenerator
import json
import random

# MODULAR ASP DISJUNCTIVE RULES MODELING - Generate balanced training data for CNL->ASP
# Target: ~10k balanced CNL:ASP pairs for disjunctive rules

# =============================================================================
# CATEGORY 1: SIMPLE DISJUNCTION (two atoms in head)
# =============================================================================
p_disj2 = ASPProgram()
p_disj2.add_line(
    '^head_pred1^("^X^"); ^head_pred2^("^X^") :- ^body_pred^("^X^").',
    {
        'simple': 'If ^X^ is ^body_pred^, then ^X^ is either ^head_pred1^ or ^head_pred2^',
        'variant1': 'Whenever ^X^ is ^body_pred^, ^X^ must be ^head_pred1^ or ^head_pred2^',
        'variant2': 'If ^X^ is ^body_pred^, then ^X^ is at least one of ^head_pred1^ or ^head_pred2^'
    }
)
disj2_variations = {
    'head_pred1': ['red', 'trusted', 'approved', 'active', 'reachable'],
    'head_pred2': ['blue', 'banned', 'pending', 'inactive', 'blocked'],
    'body_pred': ['object', 'member', 'person', 'applicant', 'node'],
    'X': ['alice', 'bob', 'charlie', 'john', 'mary', 'sam'],
}
p_disj2.add_variations(disj2_variations)

# =============================================================================
# CATEGORY 2: THREE-WAY DISJUNCTION (three atoms in head)
# =============================================================================
p_disj3 = ASPProgram()
p_disj3.add_line(
    '^head_pred1^("^X^"); ^head_pred2^("^X^"); ^head_pred3^("^X^") :- ^body_pred^("^X^").',
    {
        'simple': 'If ^X^ is ^body_pred^, then ^X^ is ^head_pred1^, ^head_pred2^, or ^head_pred3^',
        'variant1': 'Whenever ^X^ is ^body_pred^, ^X^ must be at least one of ^head_pred1^, ^head_pred2^, or ^head_pred3^',
        'variant2': 'If ^X^ is ^body_pred^, then ^X^ is one of ^head_pred1^, ^head_pred2^, or ^head_pred3^'
    }
)
disj3_variations = {
    'head_pred1': ['red', 'trusted', 'approved', 'active', 'reachable'],
    'head_pred2': ['blue', 'banned', 'pending', 'inactive', 'blocked'],
    'head_pred3': ['green', 'verified', 'confirmed', 'available', 'qualified'],
    'body_pred': ['object', 'member', 'person', 'applicant', 'node'],
    'X': ['alice', 'bob', 'charlie', 'john', 'mary', 'sam'],
}
p_disj3.add_variations(disj3_variations)

# =============================================================================
# CATEGORY 3: DISJUNCTION WITH CONSTANTS
# =============================================================================
p_const = ASPProgram()
p_const.add_line(
    '^head_pred1^("^C^"); ^head_pred2^("^C^") :- ^body_pred^("^C^").',
    {
        'simple': 'If ^C^ is ^body_pred^, then ^C^ is either ^head_pred1^ or ^head_pred2^',
        'variant1': 'Whenever ^C^ is ^body_pred^, ^C^ must be ^head_pred1^ or ^head_pred2^',
        'variant2': 'If ^C^ is ^body_pred^, then ^C^ is at least one of ^head_pred1^ or ^head_pred2^'
    }
)
const_variations = {
    'head_pred1': ['admin', 'trusted', 'approved', 'active', 'reachable'],
    'head_pred2': ['manager', 'banned', 'pending', 'inactive', 'blocked'],
    'body_pred': ['employee', 'member', 'person', 'applicant', 'node'],
    # Disjoint C and X for all constant-based rules
    'C': ['john', 'mary', 'eve', 'zoe'],
}
p_const.add_variations(const_variations)

# =============================================================================
# CATEGORY 4: DISJUNCTION WITH VARIABLES AND CONSTANTS
# =============================================================================
p_varconst = ASPProgram()
p_varconst.add_line(
    '^head_pred1^("^X^"); ^head_pred2^("^C^") :- ^body_pred^("^X^"), not ^neg_pred^("^X^").',
    {
        'simple': 'If ^X^ is ^body_pred^ and not ^neg_pred^, then ^X^ is ^head_pred1^ or ^C^ is ^head_pred2^',
        'variant1': 'Whenever ^X^ is ^body_pred^ and not ^neg_pred^, ^X^ must be ^head_pred1^ or ^C^ must be ^head_pred2^',
        'variant2': 'If ^X^ is ^body_pred^ and not ^neg_pred^, then ^X^ is ^head_pred1^ or ^C^ is ^head_pred2^'
    }
)
varconst_variations = {
    'head_pred1': ['trusted', 'approved', 'active', 'reachable'],
    'head_pred2': ['banned', 'pending', 'inactive', 'blocked'],
    'body_pred': ['member', 'person', 'applicant', 'node'],
    'neg_pred': ['banned', 'blocked', 'inactive'],
    # Disjoint X and C
    'X': ['alice', 'bob', 'charlie', 'sam'],
    'C': ['john', 'mary', 'eve', 'zoe'],
}
p_varconst.add_variations(varconst_variations)

# =============================================================================
# CATEGORY 5: DISJUNCTION WITH MULTIPLE BODY LITERALS
# =============================================================================
p_multibody = ASPProgram()
p_multibody.add_line(
    '^head_pred1^("^X^"); ^head_pred2^("^X^") :- ^body_pred1^("^X^"), ^body_pred2^("^X^").',
    {
        'simple': 'If ^X^ is both ^body_pred1^ and ^body_pred2^, then ^X^ is ^head_pred1^ or ^head_pred2^',
        'variant1': 'Whenever ^X^ is both ^body_pred1^ and ^body_pred2^, ^X^ must be ^head_pred1^ or ^head_pred2^',
        'variant2': 'If ^X^ is both ^body_pred1^ and ^body_pred2^, then ^X^ is at least one of ^head_pred1^ or ^head_pred2^'
    }
)
multibody_variations = {
    'head_pred1': ['trusted', 'approved', 'active', 'reachable'],
    'head_pred2': ['banned', 'pending', 'inactive', 'blocked'],
    'body_pred1': ['member', 'person', 'applicant', 'node'],
    'body_pred2': ['verified', 'confirmed', 'registered', 'qualified'],
    'X': ['alice', 'bob', 'charlie', 'john', 'mary', 'sam'],
}
p_multibody.add_variations(multibody_variations)

# =============================================================================
# CATEGORY 6: DISJUNCTION WITH DIFFERENT VARIABLES (disjoint sets)
# =============================================================================
p_diffvar = ASPProgram()
p_diffvar.add_line(
    '^head_pred1^("^X^", "^Y^"); ^head_pred2^("^Y^", "^X^") :- ^body_pred^("^X^", "^Y^").',
    {
        'simple': 'If ^X^ and ^Y^ are ^body_pred^, then ^X^ is ^head_pred1^ of ^Y^ or ^Y^ is ^head_pred2^ of ^X^',
        'variant1': 'Whenever ^X^ and ^Y^ are ^body_pred^, ^X^ must be ^head_pred1^ of ^Y^ or ^Y^ must be ^head_pred2^ of ^X^',
        'variant2': 'If ^X^ and ^Y^ are ^body_pred^, then ^X^ is ^head_pred1^ of ^Y^ or ^Y^ is ^head_pred2^ of ^X^'
    }
)
diffvar_variations = {
    'head_pred1': ['parent', 'manager', 'supervisor', 'friend'],
    'head_pred2': ['colleague', 'partner', 'rival', 'mentor'],
    'body_pred': ['related', 'connected', 'linked'],
    # Disjoint X and Y
    'X': ['alice', 'bob', 'charlie', 'john'],
    'Y': ['mary', 'sam', 'eve', 'zoe'],
}
p_diffvar.add_variations(diffvar_variations)

# =============================================================================
# GENERATE BALANCED DATA FOR DISJUNCTIVE RULES
# =============================================================================

programs = [
    ("disj2", p_disj2, "simple disjunction (two atoms in head)"),
    ("disj3", p_disj3, "three-way disjunction (three atoms in head)"),
    ("const", p_const, "disjunction with constants"),
    ("varconst", p_varconst, "disjunction with variables and constants"),
    ("multibody", p_multibody, "disjunction with multiple body literals"),
    ("diffvar", p_diffvar, "disjunction with different variables"),
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

print("ASP DISJUNCTIVE RULES MODELING - Generating Balanced CNL->ASP Training Data")
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
output_file = "comprehensive_disjunctive_rules_cnl_to_asp_10k.jsonl"
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
print("Modeling complete!")