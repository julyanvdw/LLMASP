from AspPy2 import ASPProgram, DataGenerator
import json
import random

# MODULAR ASP RULES MODELING - Generate balanced training data for CNL->ASP
# Target: ~10k balanced CNL:ASP pairs for rules

# =============================================================================
# CATEGORY 1: SIMPLE IMPLICATION RULES
# =============================================================================
p_simple = ASPProgram()
p_simple.add_line(
    '^head_pred^("^X^") :- ^body_pred1^("^X^").',
    {
        'simple': 'If ^X^ is ^body_pred1^, then ^X^ is ^head_pred^',
        'variant1': '^X^ being ^body_pred1^ implies ^X^ is ^head_pred^',
        'variant2': 'Whenever ^X^ is ^body_pred1^, ^X^ is also ^head_pred^'
    }
)
# For all single-variable templates, keep as is:
simple_variations = {
    'head_pred': ['eligible', 'can_vote', 'adult', 'reachable', 'trusted', 'qualified'],
    'body_pred1': ['citizen', 'student', 'person', 'connected', 'employee', 'member'],
    'X': ['Alice', 'Bob', 'Charlie', 'john', 'mary', 'sam'],
}
p_simple.add_variations(simple_variations)

# =============================================================================
# CATEGORY 2: CONJUNCTION RULES
# =============================================================================
p_conj2 = ASPProgram()
p_conj2.add_line(
    '^head_pred^("^X^") :- ^body_pred1^("^X^"), ^body_pred2^("^X^").',
    {
        'simple': 'If ^X^ is ^body_pred1^ and ^body_pred2^, then ^X^ is ^head_pred^',
        'variant1': '^X^ being both ^body_pred1^ and ^body_pred2^ means ^X^ is ^head_pred^',
        'variant2': 'Whenever ^X^ is ^body_pred1^ and ^body_pred2^, ^X^ is also ^head_pred^'
    }
)
conj2_variations = {
    'head_pred': ['eligible', 'can_vote', 'adult', 'reachable', 'trusted', 'qualified'],
    'body_pred1': ['citizen', 'student', 'person', 'connected', 'employee', 'member'],
    'body_pred2': ['blacklisted', 'registered', 'blocked', 'manager', 'admin', 'senior'],
    'X': ['Alice', 'Bob', 'Charlie', 'john', 'mary', 'sam'],
}
p_conj2.add_variations(conj2_variations)

p_conj3 = ASPProgram()
p_conj3.add_line(
    '^head_pred^("^X^") :- ^body_pred1^("^X^"), ^body_pred2^("^X^"), ^body_pred3^("^X^").',
    {
        'simple': 'If ^X^ is ^body_pred1^, ^body_pred2^, and ^body_pred3^, then ^X^ is ^head_pred^',
        'variant1': '^X^ being ^body_pred1^, ^body_pred2^, and ^body_pred3^ means ^X^ is ^head_pred^',
        'variant2': 'Whenever ^X^ is ^body_pred1^, ^body_pred2^, and ^body_pred3^, ^X^ is also ^head_pred^'
    }
)
conj3_variations = {
    'head_pred': ['eligible', 'can_vote', 'adult', 'reachable', 'trusted', 'qualified'],
    'body_pred1': ['citizen', 'student', 'person', 'connected', 'employee', 'member'],
    'body_pred2': ['blacklisted', 'registered', 'blocked', 'manager', 'admin', 'senior'],
    'body_pred3': ['senior', 'junior', 'active', 'inactive'],
    'X': ['Alice', 'Bob', 'Charlie', 'john', 'mary', 'sam'],
}
p_conj3.add_variations(conj3_variations)

# =============================================================================
# CATEGORY 3: NEGATION AS FAILURE (NAF)
# =============================================================================
p_naf = ASPProgram()
p_naf.add_line(
    '^head_pred^("^X^") :- ^body_pred1^("^X^"), not ^body_pred2^("^X^").',
    {
        'simple': 'If ^X^ is ^body_pred1^ and not ^body_pred2^, then ^X^ is ^head_pred^',
        'variant1': '^X^ being ^body_pred1^ and not ^body_pred2^ implies ^X^ is ^head_pred^',
        'variant2': 'Whenever ^X^ is ^body_pred1^ and not ^body_pred2^, ^X^ is also ^head_pred^'
    }
)
naf_variations = {
    'head_pred': ['eligible', 'can_vote', 'adult', 'reachable', 'trusted', 'qualified'],
    'body_pred1': ['citizen', 'student', 'person', 'connected', 'employee', 'member'],
    'body_pred2': ['blacklisted', 'registered', 'blocked', 'manager', 'admin', 'senior'],
    'X': ['Alice', 'Bob', 'Charlie', 'john', 'mary', 'sam'],
}
p_naf.add_variations(naf_variations)

# =============================================================================
# CATEGORY 4: ARITHMETIC COMPARISON RULES
# =============================================================================
arith_templates = [
    ('>=', 'at least'),
    ('>', 'greater than'),
    ('<', 'less than'),
    ('==', 'equal to'),
    ('!=', 'not equal to')
]
arith_programs = []
for op, phrase in arith_templates:
    prog = ASPProgram()
    prog.add_line(
        f'^head_pred^("^X^") :- ^body_pred1^("^X^"), ^attr_pred^("^X^", ^A^), ^A^ {op} ^N^.',
        {
            'simple': f'If ^X^ is ^body_pred1^ and ^attr_pred^ of ^X^ is {phrase} ^N^, then ^X^ is ^head_pred^',
            'variant1': f'^X^ being ^body_pred1^ and having ^attr_pred^ {phrase} ^N^ means ^X^ is ^head_pred^',
            'variant2': f'Whenever ^X^ is ^body_pred1^ and ^attr_pred^ is {phrase} ^N^, ^X^ is also ^head_pred^'
        }
    )
    prog.add_variations({
        'head_pred': ['eligible', 'can_vote', 'adult', 'reachable', 'trusted', 'qualified'],
        'body_pred1': ['citizen', 'student', 'person', 'connected', 'employee', 'member'],
        'attr_pred': ['age', 'score', 'years', 'level'],
        'A': ['A', 'Score', 'Years', 'Level'],
        'N': ['18', '21', '5', '10'],
        'X': ['Alice', 'Bob', 'Charlie', 'john', 'mary', 'sam'],
    })
    arith_programs.append(prog)

# =============================================================================
# CATEGORY 5: CONSTANTS IN BODY & MIXED VARIABLE/CONSTANT/ARITHMETIC
# =============================================================================
p_const = ASPProgram()
p_const.add_line(
    '^head_pred^("^X^") :- ^body_pred1^("^X^"), ^body_pred2^("^C^").',
    {
        'simple': 'If ^X^ is ^body_pred1^ and ^C^ is ^body_pred2^, then ^X^ is ^head_pred^',
        'variant1': '^X^ being ^body_pred1^ and ^C^ being ^body_pred2^ implies ^X^ is ^head_pred^',
        'variant2': 'Whenever ^X^ is ^body_pred1^ and ^C^ is ^body_pred2^, ^X^ is also ^head_pred^'
    }
)
p_const.add_line(
    '^head_pred^("^X^") :- ^body_pred1^("^X^"), ^body_pred2^("^C^"), ^attr_pred^("^X^", ^A^), ^A^ > ^N^.',
    {
        'simple': 'If ^X^ is ^body_pred1^, ^C^ is ^body_pred2^, and ^attr_pred^ of ^X^ is greater than ^N^, then ^X^ is ^head_pred^',
        'variant1': '^X^ being ^body_pred1^, ^C^ being ^body_pred2^, and ^attr_pred^ greater than ^N^ means ^X^ is ^head_pred^',
        'variant2': 'Whenever ^X^ is ^body_pred1^, ^C^ is ^body_pred2^, and ^attr_pred^ is greater than ^N^, ^X^ is also ^head_pred^'
    }
)
const_variations = {
    'head_pred': ['eligible', 'can_vote', 'adult', 'reachable', 'trusted', 'qualified'],
    'body_pred1': ['citizen', 'student', 'person', 'connected', 'employee', 'member'],
    'body_pred2': ['blacklisted', 'registered', 'blocked', 'manager', 'admin', 'senior'],
    'attr_pred': ['age', 'score', 'years', 'level'],
    'A': ['A', 'Score', 'Years', 'Level'],
    'N': ['18', '21', '5', '10'],
    'C': ['john', 'mary', 'admin', 'manager'],
    'X': ['Alice', 'Bob', 'Charlie', 'john', 'mary', 'sam'],
}
p_const.add_variations(const_variations)

# =============================================================================
# CATEGORY 6: RECURSIVE RULES
# =============================================================================
p_rec = ASPProgram()
p_rec.add_line(
    '^head_pred^("^X^", "^Y^") :- ^body_pred1^("^X^", "^Y^").',
    {
        'simple': 'If ^X^ and ^Y^ are ^body_pred1^, then ^X^ and ^Y^ are ^head_pred^',
        'variant1': '^X^ and ^Y^ being ^body_pred1^ implies they are ^head_pred^',
        'variant2': 'Whenever ^X^ and ^Y^ are ^body_pred1^, they are also ^head_pred^'
    }
)
p_rec.add_line(
    '^head_pred^("^X^", "^Z^") :- ^head_pred^("^X^", "^Y^"), ^body_pred1^("^Y^", "^Z^").',
    {
        'simple': 'If ^X^ and ^Y^ are ^head_pred^ and ^Y^ and ^Z^ are ^body_pred1^, then ^X^ and ^Z^ are ^head_pred^',
        'variant1': '^X^ and ^Y^ being ^head_pred^ and ^Y^ and ^Z^ being ^body_pred1^ implies ^X^ and ^Z^ are ^head_pred^',
        'variant2': 'Whenever ^X^ and ^Y^ are ^head_pred^ and ^Y^ and ^Z^ are ^body_pred1^, ^X^ and ^Z^ are also ^head_pred^'
    }
)
rec_variations = {
    'head_pred': ['reachable', 'trusted'],
    'body_pred1': ['connected', 'friend'],
    # Disjoint sets for X, Y, Z
    'X': ['Alice', 'Bob', 'Charlie', 'john'],
    'Y': ['mary', 'sam', 'eve', 'zoe'],
    'Z': ['lucas', 'oliver', 'mia', 'noah'],
}
p_rec.add_variations(rec_variations)

# =============================================================================
# CATEGORY 7: DIFFERENT ARITIES IN HEAD/BODY
# =============================================================================
p_arity = ASPProgram()
p_arity.add_line(
    '^head_pred^("^X^", "^Y^") :- ^body_pred1^("^X^"), ^body_pred2^("^Y^").',
    {
        'simple': 'If ^X^ is ^body_pred1^ and ^Y^ is ^body_pred2^, then ^X^ and ^Y^ are ^head_pred^',
        'variant1': '^X^ being ^body_pred1^ and ^Y^ being ^body_pred2^ means they are ^head_pred^',
        'variant2': 'Whenever ^X^ is ^body_pred1^ and ^Y^ is ^body_pred2^, ^X^ and ^Y^ are also ^head_pred^'
    }
)
arity_variations = {
    'head_pred': ['qualified', 'trusted'],
    'body_pred1': ['member', 'employee'],
    'body_pred2': ['admin', 'manager'],
    # Disjoint sets for X and Y
    'X': ['Alice', 'Bob', 'Charlie', 'john'],
    'Y': ['mary', 'sam', 'eve', 'zoe'],
}
p_arity.add_variations(arity_variations)

# =============================================================================
# CATEGORY 8: ANONYMOUS VARIABLE IN BODY
# =============================================================================
p_anon = ASPProgram()
p_anon.add_line(
    '^head_pred^("^X^") :- ^body_pred1^("^X^", _).',
    {
        'simple': 'If ^X^ is ^body_pred1^ with someone, then ^X^ is ^head_pred^',
        'variant1': '^X^ being ^body_pred1^ with someone implies ^X^ is ^head_pred^',
        'variant2': 'Whenever ^X^ is ^body_pred1^ with someone, ^X^ is also ^head_pred^'
    }
)
anon_variations = {
    'head_pred': ['reachable', 'trusted'],
    'body_pred1': ['connected', 'friend'],
    'X': ['Alice', 'Bob', 'Charlie', 'john', 'mary', 'sam'],
}
p_anon.add_variations(anon_variations)

# =============================================================================
# CATEGORY 9: STRING/ATOM COMPARISON
# =============================================================================
p_str = ASPProgram()
p_str.add_line(
    '^head_pred^("^X^") :- ^body_pred1^("^X^", ^S^), ^S^ == "^T^".',
    {
        'simple': 'If ^X^ is ^body_pred1^ with status ^T^, then ^X^ is ^head_pred^',
        'variant1': '^X^ being ^body_pred1^ with status ^T^ means ^X^ is ^head_pred^',
        'variant2': 'Whenever ^X^ is ^body_pred1^ with status ^T^, ^X^ is also ^head_pred^'
    }
)
str_variations = {
    'head_pred': ['trusted', 'qualified'],
    'body_pred1': ['employee', 'member'],
    'S': ['S', 'Status'],
    'T': ['admin', 'manager', 'senior', 'active'],
    'X': ['Alice', 'Bob', 'Charlie', 'john', 'mary', 'sam'],
}
p_str.add_variations(str_variations)

# =============================================================================
# GENERATE BALANCED DATA FOR RULES
# =============================================================================

programs = [
    ("simple", p_simple, "simple implication rules"),
    ("conj2", p_conj2, "conjunction rules (2 body literals)"),
    ("conj3", p_conj3, "conjunction rules (3 body literals)"),
    ("naf", p_naf, "negation as failure rules"),
    ("const", p_const, "constants in body & mixed variable/constant/arithmetic"),
    ("rec", p_rec, "recursive rules"),
    ("arity", p_arity, "different arities in head/body"),
    ("anon", p_anon, "anonymous variable in body"),
    ("str", p_str, "string/atom comparison"),
]
# Add arithmetic programs
for i, prog in enumerate(arith_programs):
    programs.append((f"arith_{i}", prog, f"arithmetic comparison rule ({arith_templates[i][0]})"))

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

print("ASP RULES MODELING - Generating Balanced CNL->ASP Training Data")
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
output_file = "comprehensive_rules_cnl_to_asp_10k.jsonl"
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