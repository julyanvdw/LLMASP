from AspPy2 import ASPProgram, DataGenerator
import json
import random

# MODULAR ASP INTEGRITY CONSTRAINTS MODELING - Generate balanced training data for CNL->ASP
# Target: ~10k balanced CNL:ASP pairs for integrity constraints

# =============================================================================
# CATEGORY 1: SIMPLE CONSTRAINTS (single literal)
# =============================================================================
p_simple = ASPProgram()
p_simple.add_line(
    ':- ^body_pred^("^X^").',
    {
        'simple': 'It is forbidden for ^X^ to be ^body_pred^',
        'variant1': '^X^ must not be ^body_pred^',
        'variant2': 'No answer set may contain ^X^ as ^body_pred^'
    }
)
p_simple.add_line(
    ':- not ^body_pred^("^X^").',
    {
        'simple': 'It is forbidden for ^X^ to not be ^body_pred^',
        'variant1': '^X^ must always be ^body_pred^',
        'variant2': 'No answer set may contain ^X^ not being ^body_pred^'
    }
)
p_simple.add_line(
    ':- ^body_pred^("^X^", ^Y^).',
    {
        'simple': 'It is forbidden for ^X^ to be ^body_pred^ with ^Y^',
        'variant1': '^X^ must not be ^body_pred^ with ^Y^',
        'variant2': 'No answer set may contain ^X^ as ^body_pred^ with ^Y^'
    }
)
simple_variations = {
    'body_pred': [
        'banned', 'blocked', 'forbidden', 'excluded', 'blacklisted',
        'inactive', 'pending', 'guest', 'temporary', 'visitor'
    ],
    'X': ['Alice', 'Bob', 'Charlie', 'john', 'mary', 'sam'],
    'Y': ['eve', 'zoe', 'lucas', 'oliver', 'mia', 'noah'],
}
p_simple.add_variations(simple_variations)

# =============================================================================
# CATEGORY 2: CONJUNCTION CONSTRAINTS (multiple literals)
# =============================================================================
p_conj = ASPProgram()
p_conj.add_line(
    ':- ^body_pred1^("^X^"), ^body_pred2^("^X^").',
    {
        'simple': 'It is forbidden for ^X^ to be both ^body_pred1^ and ^body_pred2^',
        'variant1': '^X^ cannot be both ^body_pred1^ and ^body_pred2^',
        'variant2': 'No answer set may contain ^X^ as both ^body_pred1^ and ^body_pred2^'
    }
)
p_conj.add_line(
    ':- ^body_pred1^("^X^"), ^body_pred2^("^Y^").',
    {
        'simple': 'It is forbidden for ^X^ to be ^body_pred1^ and ^Y^ to be ^body_pred2^',
        'variant1': '^X^ cannot be ^body_pred1^ if ^Y^ is ^body_pred2^',
        'variant2': 'No answer set may contain ^X^ as ^body_pred1^ and ^Y^ as ^body_pred2^'
    }
)
p_conj.add_line(
    ':- ^body_pred1^("^X^"), ^body_pred2^("^X^"), ^body_pred3^("^X^").',
    {
        'simple': 'It is forbidden for ^X^ to be ^body_pred1^, ^body_pred2^, and ^body_pred3^',
        'variant1': '^X^ cannot be ^body_pred1^, ^body_pred2^, and ^body_pred3^ at the same time',
        'variant2': 'No answer set may contain ^X^ as ^body_pred1^, ^body_pred2^, and ^body_pred3^'
    }
)
conj_variations = {
    'body_pred1': [
        'banned', 'blocked', 'forbidden', 'excluded', 'blacklisted',
        'inactive', 'pending', 'guest', 'temporary', 'visitor'
    ],
    'body_pred2': [
        'active', 'member', 'trusted', 'admin', 'manager',
        'verified', 'approved', 'registered', 'confirmed'
    ],
    'body_pred3': [
        'pending', 'inactive', 'guest', 'temporary', 'visitor', 'blocked'
    ],
    # Disjoint X and Y for all conjunctions involving both
    'X': ['Alice', 'Bob', 'Charlie', 'john', 'mary', 'sam'],
    'Y': ['eve', 'zoe', 'lucas', 'oliver', 'mia', 'noah'],
}
p_conj.add_variations(conj_variations)

# =============================================================================
# CATEGORY 3: NEGATION AS FAILURE CONSTRAINTS
# =============================================================================
p_naf = ASPProgram()
p_naf.add_line(
    ':- ^body_pred1^("^X^"), not ^body_pred2^("^X^").',
    {
        'simple': 'It is forbidden for ^X^ to be ^body_pred1^ and not ^body_pred2^',
        'variant1': '^X^ must not be ^body_pred1^ without being ^body_pred2^',
        'variant2': 'No answer set may contain ^X^ as ^body_pred1^ unless ^X^ is also ^body_pred2^'
    }
)
p_naf.add_line(
    ':- not ^body_pred1^("^X^"), ^body_pred2^("^X^").',
    {
        'simple': 'It is forbidden for ^X^ to not be ^body_pred1^ and be ^body_pred2^',
        'variant1': '^X^ must not be ^body_pred2^ unless ^X^ is also ^body_pred1^',
        'variant2': 'No answer set may contain ^X^ as ^body_pred2^ unless also ^body_pred1^'
    }
)
naf_variations = {
    'body_pred1': ['active', 'member', 'trusted', 'admin', 'manager'],
    'body_pred2': ['verified', 'approved', 'registered', 'confirmed'],
    'X': ['Alice', 'Bob', 'Charlie', 'john', 'mary', 'sam'],
}
p_naf.add_variations(naf_variations)

# =============================================================================
# CATEGORY 4: CONSTANTS IN CONSTRAINTS
# =============================================================================
p_const = ASPProgram()
p_const.add_line(
    ':- ^body_pred^("^C^").',
    {
        'simple': 'It is forbidden for ^C^ to be ^body_pred^',
        'variant1': '^C^ must not be ^body_pred^',
        'variant2': 'No answer set may contain ^C^ as ^body_pred^'
    }
)
p_const.add_line(
    ':- ^body_pred^("^C^"), ^body_pred2^("^X^").',
    {
        'simple': 'It is forbidden for ^C^ to be ^body_pred^ and ^X^ to be ^body_pred2^',
        'variant1': '^C^ must not be ^body_pred^ if ^X^ is ^body_pred2^',
        'variant2': 'No answer set may contain ^C^ as ^body_pred^ and ^X^ as ^body_pred2^'
    }
)
const_variations = {
    'body_pred': ['banned', 'blocked', 'forbidden', 'excluded', 'blacklisted'],
    'body_pred2': [
        'active', 'member', 'trusted', 'admin', 'manager',
        'verified', 'approved', 'registered', 'confirmed'
    ],
    # Disjoint C and X
    'C': ['john', 'mary', 'admin', 'manager'],
    'X': ['Alice', 'Bob', 'Charlie', 'sam'],
}
p_const.add_variations(const_variations)

# =============================================================================
# CATEGORY 5: ARITHMETIC COMPARISON CONSTRAINTS
# =============================================================================
p_arith = ASPProgram()
p_arith.add_line(
    ':- ^attr_pred^("^X^", ^A^), ^A^ < ^N^.',
    {
        'simple': 'It is forbidden for ^X^ to have ^attr_pred^ less than ^N^',
        'variant1': '^X^ must not have ^attr_pred^ below ^N^',
        'variant2': 'No answer set may contain ^X^ with ^attr_pred^ less than ^N^'
    }
)
p_arith.add_line(
    ':- ^attr_pred^("^X^", ^A^), ^A^ > ^N^.',
    {
        'simple': 'It is forbidden for ^X^ to have ^attr_pred^ greater than ^N^',
        'variant1': '^X^ must not have ^attr_pred^ above ^N^',
        'variant2': 'No answer set may contain ^X^ with ^attr_pred^ greater than ^N^'
    }
)
p_arith.add_line(
    ':- ^attr_pred^("^X^", ^A^), ^A^ = ^N^.',
    {
        'simple': 'It is forbidden for ^X^ to have ^attr_pred^ equal to ^N^',
        'variant1': '^X^ must not have ^attr_pred^ equal to ^N^',
        'variant2': 'No answer set may contain ^X^ with ^attr_pred^ equal to ^N^'
    }
)
p_arith.add_line(
    ':- ^attr_pred^("^X^", ^A^), ^A^ != ^N^.',
    {
        'simple': 'It is forbidden for ^X^ to have ^attr_pred^ not equal to ^N^',
        'variant1': '^X^ must not have ^attr_pred^ not equal to ^N^',
        'variant2': 'No answer set may contain ^X^ with ^attr_pred^ not equal to ^N^'
    }
)
arith_variations = {
    'attr_pred': [
        'age', 'score', 'years', 'level', 'points', 'rank', 'grade'
    ],
    'A': ['A', 'Score', 'Years', 'Level'],
    'N': [
        '18', '21', '5', '10', '0', '100', '50', '65', '30', '40', '60', '75'
    ],
    'X': ['Alice', 'Bob', 'Charlie', 'john', 'mary', 'sam', 'eve', 'zoe', 'lucas', 'oliver', 'mia', 'noah'],
}
p_arith.add_variations(arith_variations)

# =============================================================================
# CATEGORY 6: MULTIPLE VARIABLES CONSTRAINTS
# =============================================================================
p_multivar = ASPProgram()
p_multivar.add_line(
    ':- ^rel_pred^("^X^", "^Y^"), ^rel_pred^("^Y^", "^X^").',
    {
        'simple': 'It is forbidden for ^X^ to be ^rel_pred^ of ^Y^ and ^Y^ to be ^rel_pred^ of ^X^',
        'variant1': '^X^ and ^Y^ cannot be ^rel_pred^ of each other',
        'variant2': 'No answer set may contain ^X^ and ^Y^ as mutual ^rel_pred^'
    }
)
p_multivar.add_line(
    ':- ^rel_pred1^("^X^", "^Y^"), ^rel_pred2^("^Y^", "^Z^").',
    {
        'simple': 'It is forbidden for ^X^ to be ^rel_pred1^ of ^Y^ and ^Y^ to be ^rel_pred2^ of ^Z^',
        'variant1': '^X^ cannot be ^rel_pred1^ of ^Y^ if ^Y^ is ^rel_pred2^ of ^Z^',
        'variant2': 'No answer set may contain ^X^ as ^rel_pred1^ of ^Y^ and ^Y^ as ^rel_pred2^ of ^Z^'
    }
)
multivar_variations = {
    'rel_pred': [
        'parent', 'manager', 'supervisor', 'friend', 'colleague', 'partner', 'rival'
    ],
    'rel_pred1': [
        'parent', 'manager', 'supervisor', 'friend', 'colleague', 'partner', 'rival'
    ],
    'rel_pred2': [
        'parent', 'manager', 'supervisor', 'friend', 'colleague', 'partner', 'rival'
    ],
    # Disjoint X, Y, Z
    'X': ['Alice', 'Bob', 'Charlie', 'john'],
    'Y': ['mary', 'sam', 'eve', 'zoe'],
    'Z': ['lucas', 'oliver', 'mia', 'noah'],
}
p_multivar.add_variations(multivar_variations)

# =============================================================================
# CATEGORY 7: ANONYMOUS VARIABLE CONSTRAINTS
# =============================================================================
p_anon = ASPProgram()
p_anon.add_line(
    ':- ^body_pred^("^X^", _).',
    {
        'simple': 'It is forbidden for ^X^ to be ^body_pred^ with anyone',
        'variant1': '^X^ must not be ^body_pred^ with any person',
        'variant2': 'No answer set may contain ^X^ as ^body_pred^ with anyone'
    }
)
p_anon.add_line(
    ':- ^body_pred^(_, "^X^").',
    {
        'simple': 'It is forbidden for anyone to be ^body_pred^ with ^X^',
        'variant1': 'No person must be ^body_pred^ with ^X^',
        'variant2': 'No answer set may contain anyone as ^body_pred^ with ^X^'
    }
)
anon_variations = {
    'body_pred': ['assigned', 'connected', 'related', 'linked'],
    # Disjoint X for each role
    'X': ['Alice', 'Bob', 'Charlie', 'john', 'mary', 'sam'],
}
p_anon.add_variations(anon_variations)

# =============================================================================
# CATEGORY 8: STRONG NEGATION CONSTRAINTS
# =============================================================================
p_strongneg = ASPProgram()
p_strongneg.add_line(
    ':- -^body_pred^("^X^").',
    {
        'simple': 'It is forbidden for ^X^ to be not ^body_pred^',
        'variant1': '^X^ must not be explicitly not ^body_pred^',
        'variant2': 'No answer set may contain ^X^ as not ^body_pred^'
    }
)
p_strongneg.add_line(
    ':- -^body_pred^("^X^"), ^body_pred2^("^X^").',
    {
        'simple': 'It is forbidden for ^X^ to be not ^body_pred^ and ^body_pred2^',
        'variant1': '^X^ must not be both not ^body_pred^ and ^body_pred2^',
        'variant2': 'No answer set may contain ^X^ as not ^body_pred^ and ^body_pred2^'
    }
)
strongneg_variations = {
    'body_pred': ['alive', 'present', 'active', 'available'],
    'body_pred2': ['member', 'trusted', 'admin', 'manager'],
    # Disjoint X
    'X': ['Alice', 'Bob', 'Charlie', 'john', 'mary', 'sam'],
}
p_strongneg.add_variations(strongneg_variations)

# =============================================================================
# GENERATE BALANCED DATA FOR INTEGRITY CONSTRAINTS
# =============================================================================

programs = [
    ("simple", p_simple, "simple constraints (single literal)"),
    ("conj", p_conj, "conjunction constraints (multiple literals)"),
    ("naf", p_naf, "negation as failure constraints"),
    ("const", p_const, "constants in constraints"),
    ("arith", p_arith, "arithmetic comparison constraints"),
    ("multivar", p_multivar, "multiple variables constraints"),
    ("anon", p_anon, "anonymous variable constraints"),
    ("strongneg", p_strongneg, "strong negation constraints"),
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
    'max_size': 4,  # Allow up to 3 constraints per program for variety
    'window_type': 'random',
    'random_samples': 3,  # Keep samples controlled
    'randomised_order': True
}

print("ASP INTEGRITY CONSTRAINTS MODELING - Generating Balanced CNL->ASP Training Data")
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
output_file = "comprehensive_constraints_cnl_to_asp_10k.jsonl"
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