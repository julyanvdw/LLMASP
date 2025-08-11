from AspPy2 import ASPProgram, DataGenerator
import json
import random

# MODULAR ASP FACTS MODELING - Generate balanced training data for CNL->ASP
# Target: ~10k balanced CNL:ASP pairs across different fact categories

# =============================================================================
# PROGRAM 1: ATOMIC FACTS (0-arity predicates)
# =============================================================================
p_atomic = ASPProgram()

# Weather and environmental states
p_atomic.add_line('^weather^.',
               {'simple': 'It is ^weather^',
                'variant1': '^weather^',
                'variant2': 'The weather condition is ^weather^'})

# Temporal states
p_atomic.add_line('^time_period^.',
               {'simple': 'It is ^time_period^',
                'variant1': '^time_period^',
                'variant2': 'The current period is ^time_period^'})

# System states
p_atomic.add_line('^system_status^.',
               {'simple': 'System is ^system_status^',
                'variant1': '^system_status^',
                'variant2': 'The system status is ^system_status^'})

# Emergency states
p_atomic.add_line('^emergency^.',
               {'simple': 'There is ^emergency^',
                'variant1': '^emergency^',
                'variant2': 'Emergency state: ^emergency^'})

atomic_variations = {
    'weather': ['sunny', 'raining', 'cloudy', 'snowing', 'windy'],
    'time_period': ['morning', 'afternoon', 'evening', 'night', 'dawn'],
    'system_status': ['online', 'offline', 'maintenance', 'error', 'ready'],
    'emergency': ['fire_alarm', 'flood_warning', 'security_breach', 'medical_emergency']
}
p_atomic.add_variations(atomic_variations)

# =============================================================================
# PROGRAM 2: UNARY FACTS (1-arity predicates)
# =============================================================================
p_unary = ASPProgram()

# Entity classifications
p_unary.add_line('^entity_type^("^name^").',
               {'simple': '^name^ is a ^entity_type^',
                'variant1': '^name^ is ^entity_type^',
                'variant2': 'The entity ^name^ is of type ^entity_type^'})

# Location classifications
p_unary.add_line('^location_type^("^place^").',
               {'simple': '^place^ is a ^location_type^',
                'variant1': '^place^ is ^location_type^',
                'variant2': 'The location ^place^ is a ^location_type^'})

# Mathematical properties
p_unary.add_line('^math_property^(^number^).',
               {'simple': '^number^ is ^math_property^',
                'variant1': 'The number ^number^ is ^math_property^',
                'variant2': 'Number ^number^ has property ^math_property^'})

# Object properties
p_unary.add_line('^object_state^("^object^").',
               {'simple': '^object^ is ^object_state^',
                'variant1': 'The object ^object^ is ^object_state^',
                'variant2': 'Object ^object^ has state ^object_state^'})

unary_variations = {
    'entity_type': ['person', 'student', 'teacher'],
    'name': ['Alice', 'Bob', 'Charlie'],
    'location_type': ['city', 'country'],
    'place': ['Paris', 'London', 'France'],
    'math_property': ['prime', 'even'],
    'number': ['2', '3', '4'],
    'object_state': ['active', 'inactive'],
    'object': ['computer', 'phone', 'car']
}
p_unary.add_variations(unary_variations)

# =============================================================================
# PROGRAM 3: BINARY FACTS (2-arity predicates)
# =============================================================================
p_binary = ASPProgram()

# Family relationships
p_binary.add_line('^family_relation^("^person1^", "^person2^").',
               {'simple': '^person1^ is the ^family_relation^ of ^person2^',
                'variant1': '^person1^ is ^person2^\'s ^family_relation^',
                'variant2': 'The ^family_relation^ relationship exists between ^person1^ and ^person2^'})

# Preferences and opinions
p_binary.add_line('^preference^("^person^", "^item^").',
               {'simple': '^person^ ^preference^ ^item^',
                'variant1': '^person^ ^preference^s ^item^',
                'variant2': 'The person ^person^ has preference ^preference^ for ^item^'})

# Geographic relationships
p_binary.add_line('^geo_relation^("^location1^", "^location2^").',
               {'simple': '^location1^ is ^geo_relation^ ^location2^',
                'variant1': '^location1^ ^geo_relation^ ^location2^',
                'variant2': 'The geographic relation between ^location1^ and ^location2^ is ^geo_relation^'})

# Ownership relationships
p_binary.add_line('owns("^owner^", "^possession^").',
               {'simple': '^owner^ owns ^possession^',
                'variant1': 'The owner of ^possession^ is ^owner^',
                'variant2': 'Ownership relation: ^owner^ possesses ^possession^'})

binary_variations = {
    'family_relation': ['parent', 'mother', 'father'],
    'person1': ['Alice', 'Bob', 'Charlie'],
    'person2': ['Eve', 'Frank', 'Grace'],
    'preference': ['likes', 'dislikes'],
    'person': ['Alice', 'Bob', 'Charlie'],
    'item': ['pizza', 'pasta', 'coffee'],
    'geo_relation': ['located_in', 'capital_of'],
    'location1': ['Paris', 'London'],
    'location2': ['France', 'England'],
    'owner': ['John', 'Mary', 'Company'],
    'possession': ['car', 'house', 'laptop']
}
p_binary.add_variations(binary_variations)

# =============================================================================
# PROGRAM 4: TERNARY FACTS (3-arity predicates)
# =============================================================================
p_ternary = ASPProgram()

# Academic grades
p_ternary.add_line('grade("^student^", "^subject^", "^grade_value^").',
               {'simple': '^student^ got ^grade_value^ in ^subject^',
                'variant1': 'The grade for ^student^ in ^subject^ is ^grade_value^',
                'variant2': 'Student ^student^ received grade ^grade_value^ for subject ^subject^'})

# Product information
p_ternary.add_line('product("^item^", "^brand^", ^price^).',
               {'simple': '^item^ by ^brand^ costs ^price^',
                'variant1': 'The ^brand^ ^item^ costs ^price^',
                'variant2': 'Product ^item^ from brand ^brand^ has price ^price^'})

# Work assignments
p_ternary.add_line('assigned("^person^", "^task^", "^deadline^").',
               {'simple': '^person^ is assigned ^task^ due ^deadline^',
                'variant1': 'The task ^task^ is assigned to ^person^ with deadline ^deadline^',
                'variant2': 'Assignment: ^person^ must complete ^task^ by ^deadline^'})

# Location activities
p_ternary.add_line('activity("^agent^", "^action^", "^location^").',
               {'simple': '^agent^ does ^action^ at ^location^',
                'variant1': 'The agent ^agent^ performs ^action^ at location ^location^',
                'variant2': 'Activity: ^agent^ engages in ^action^ at ^location^'})

ternary_variations = {
    'student': ['John', 'Mary', 'Alice'],
    'subject': ['Math', 'Physics', 'Chemistry'],
    'grade_value': ['A', 'B', 'C'],
    'item': ['laptop', 'phone', 'tablet'],
    'brand': ['Apple', 'Samsung', 'Dell'],
    'price': ['500', '800', '1200'],
    'person': ['Alice', 'Bob', 'Charlie'],
    'task': ['report', 'presentation', 'analysis'],
    'deadline': ['monday', 'friday', 'next_week'],
    'agent': ['student', 'worker', 'teacher'],
    'action': ['studying', 'working', 'meeting'],
    'location': ['library', 'office', 'classroom']
}
p_ternary.add_variations(ternary_variations)

# =============================================================================
# PROGRAM 5: QUATERNARY FACTS (4-arity predicates)
# =============================================================================
p_quaternary = ASPProgram()

# Address information
p_quaternary.add_line('address("^person^", "^street^", "^city^", "^zipcode^").',
               {'simple': '^person^ lives at ^street^ in ^city^ ^zipcode^',
                'variant1': 'The address of ^person^ is ^street^, ^city^ ^zipcode^',
                'variant2': 'Address record: ^person^ resides at ^street^, ^city^ ^zipcode^'})

# Meeting schedules
p_quaternary.add_line('meeting("^organizer^", "^topic^", "^time^", "^room^").',
               {'simple': '^organizer^ schedules meeting about ^topic^ at ^time^ in ^room^',
                'variant1': 'Meeting organized by ^organizer^ on ^topic^ scheduled for ^time^ in room ^room^',
                'variant2': 'Schedule: ^organizer^ hosts ^topic^ meeting at ^time^ in ^room^'})

# Transaction records
p_quaternary.add_line('transaction("^buyer^", "^seller^", "^item^", ^amount^).',
               {'simple': '^buyer^ bought ^item^ from ^seller^ for ^amount^',
                'variant1': 'Transaction: ^buyer^ purchased ^item^ from ^seller^ at price ^amount^',
                'variant2': 'Sale record: ^seller^ sold ^item^ to ^buyer^ for ^amount^'})

quaternary_variations = {
    'person': ['Alice', 'Bob', 'Charlie'],
    'street': ['Main_St', 'Oak_Ave', 'First_St'],
    'city': ['NewYork', 'Boston', 'Chicago'],
    'zipcode': ['10001', '02101', '60601'],
    'organizer': ['Alice', 'Bob', 'Manager'],
    'topic': ['budget', 'planning', 'review'],
    'time': ['9am', '2pm', '4pm'],
    'room': ['A101', 'B205', 'Conference'],
    'buyer': ['Alice', 'Bob', 'Company'],
    'seller': ['Store', 'Vendor', 'Market'],
    'item': ['laptop', 'software', 'service'],
    'amount': ['1000', '500', '2000']
}
p_quaternary.add_variations(quaternary_variations)

# =============================================================================
# PROGRAM 6: MEASUREMENT FACTS
# =============================================================================
p_measurement = ASPProgram()

# Price information
p_measurement.add_line('price("^item^", ^cost^, "^currency^").',
               {'simple': '^item^ costs ^cost^ ^currency^',
                'variant1': 'The price of ^item^ is ^cost^ ^currency^',
                'variant2': 'Cost: ^item^ is priced at ^cost^ ^currency^'})

# Distance measurements
p_measurement.add_line('distance("^place1^", "^place2^", ^amount^, "^unit^").',
               {'simple': 'Distance from ^place1^ to ^place2^ is ^amount^ ^unit^',
                'variant1': 'The distance between ^place1^ and ^place2^ is ^amount^ ^unit^',
                'variant2': 'Measurement: ^place1^ to ^place2^ spans ^amount^ ^unit^'})

# Weight specifications
p_measurement.add_line('weight("^object^", ^value^, "^unit^").',
               {'simple': '^object^ weighs ^value^ ^unit^',
                'variant1': 'The weight of ^object^ is ^value^ ^unit^',
                'variant2': 'Weight specification: ^object^ has mass ^value^ ^unit^'})

measurement_variations = {
    'item': ['apple', 'coffee', 'laptop', 'book'],
    'cost': ['10', '25', '1000', '15'],
    'currency': ['USD', 'EUR', 'GBP'],
    'place1': ['NewYork', 'Paris', 'London'],
    'place2': ['Boston', 'Berlin', 'Tokyo'],
    'amount': ['100', '500', '1200', '50'],
    'unit': ['km', 'miles', 'meters'],
    'object': ['box', 'package', 'container', 'bag'],
    'value': ['5', '10', '25', '2']
}
p_measurement.add_variations(measurement_variations)

# =============================================================================
# PROGRAM 7: TEMPORAL FACTS
# =============================================================================
p_temporal = ASPProgram()

# Birth dates
p_temporal.add_line('born("^person^", ^year^).',
               {'simple': '^person^ was born in ^year^',
                'variant1': 'The birth year of ^person^ is ^year^',
                'variant2': 'Birth record: ^person^ born in year ^year^'})

# Event scheduling
p_temporal.add_line('event("^event_name^", "^date^").',
               {'simple': 'Event ^event_name^ is on ^date^',
                'variant1': 'The event ^event_name^ happens on ^date^',
                'variant2': 'Schedule: ^event_name^ is scheduled for ^date^'})

# Work schedules
p_temporal.add_line('schedule("^person^", "^activity^", "^time^").',
               {'simple': '^person^ has ^activity^ at ^time^',
                'variant1': 'The schedule for ^person^ includes ^activity^ at ^time^',
                'variant2': 'Time slot: ^person^ does ^activity^ at ^time^'})

temporal_variations = {
    'person': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'year': ['1990', '1995', '2000', '1985'],
    'event_name': ['meeting', 'conference', 'party', 'workshop'],
    'date': ['2024-01-15', '2024-06-20', '2024-12-25', '2024-03-10'],
    'activity': ['work', 'meeting', 'training', 'break'],
    'time': ['9am', '2pm', '4pm', '11am']
}
p_temporal.add_variations(temporal_variations)

# =============================================================================
# GENERATE BALANCED DATA ACROSS ALL PROGRAMS
# =============================================================================

programs = [
    ("atomic", p_atomic, "atomic facts (0-arity predicates)"),
    ("unary", p_unary, "unary facts (1-arity predicates)"),
    ("binary", p_binary, "binary facts (2-arity predicates)"),
    ("ternary", p_ternary, "ternary facts (3-arity predicates)"),
    ("quaternary", p_quaternary, "quaternary facts (4-arity predicates)"),
    ("measurement", p_measurement, "measurement facts with units"),
    ("temporal", p_temporal, "temporal facts with dates/times")
]

# CNL levels - focusing on CNL->ASP translation
cnl_levels = {
    'simple': ['simple'],
    'variant1': ['variant1'],  
    'variant2': ['variant2']
}

nl_levels = {
    'basic': ['simple']  # We don't really use NL, but needed for the framework
}

# Balanced splice params to get good variety without explosion
splice_params = {
    'strategy': 'multi_granularity',
    'min_size': 1,
    'max_size': 4,  # Increased to allow longer programs
    'window_type': 'random',
    'random_samples': 2,  # Keep samples controlled
    'randomised_order': True
}

print("ASP FACTS MODELING - Generating Balanced CNL->ASP Training Data")
print("="*70)

total_generated = 0
all_cnl_asp_pairs = set()
program_stats = []

# Target roughly equal representation per program
target_per_program = 10000 // len(programs)  # Aim for ~1400 per program

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
output_file = "comprehensive_facts_cnl_to_asp_10k.jsonl"
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
