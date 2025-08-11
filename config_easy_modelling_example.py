from AspPy2 import ASPProgram, DataGenerator

# Theme-specific dictionary for predicate names and variable names


theme_sets = [
    # Theme 1 - Computer Building
    {
        'P1': 'cpu',
        'P2': 'selected_cpu',
        'P3': 'gpu',
        'P4': 'selected_gpu',
        'P6': 'C',
        'P7': 'G',
        'variations': {
            'V1': ['Ryzen5', 'Ryzen4'],
            'V2': ['i5'],
            'V3': ['GTX1660'],
            'V4': ['RX580']
        }
    }, 
    {
        'P1': 'speaker',
        'P2': 'selected_speaker',
        'P3': 'amplifier',
        'P4': 'selected_amplifier',
        'P6': 'S',
        'P7': 'A',
        'variations': {
            'V1': ['Alpha', 'AAAA'],
            'V2': ['BETA'],
            'V3': ['AMPY'],
            'V4': ['AMPX']
        }, 
    }
]


def generate_programs(theme_sets):

    generated_programs = []

    for theme in theme_sets:
        p = ASPProgram()

        cpu_fact = p.add_line(
            '{P1}("^V1^"; "^V2^").'.format(**theme),
            {'simple': '^V1^ and ^V2^ are {P1}s.'.format(**theme)},
            {'simple': 'There are two {P1}s: ^V1^ and ^V2^.'.format(**theme)},
            label='cpu'
        )
        cpu_choice = p.add_line(
            '1 {{ {P2}({P6}) : {P1}({P6}) }} 1.'.format(**theme),
            {'simple': 'Select exactly one {P1} from ^V1^, ^V2^.'.format(**theme)},
            {'simple': 'You must choose one {P1}: ^V1^ or ^V2^.'.format(**theme)},
            label='cpu_choice'
        )
        gpu_fact = p.add_line(
            '{P3}("^V3^"; "^V4^").'.format(**theme),
            {'simple': '^V3^ and ^V4^ are {P3}s.'.format(**theme)},
            {'simple': 'There are two {P3}s: ^V3^ and ^V4^.'.format(**theme)},
            label='gpu'
        )
        gpu_choice = p.add_line(
            '1 {{ {P4}({P7}) : {P3}({P7}) }} 1.'.format(**theme),
            {'simple': 'Select exactly one {P3} from ^V3^, ^V4^.'.format(**theme)},
            {'simple': 'You must choose one {P3}: ^V3^ or ^V4^.'.format(**theme)},
            label='gpu_choice'
        )

        p.add_group(
            [cpu_fact, cpu_choice, gpu_fact, gpu_choice],
            {'simple/4': 'You must select exactly one {P1} and one {P3} for your build.'.format(**theme)}
        )

        # Register only the value variations with AspPy2
        p.add_variations(theme['variations'])
        generated_programs.append(p)

    return generated_programs


# Set up CNL and NL levels
cnl_levels = {'simple': ['simple']}
nl_levels = {'simple': ['simple']}

# Generate the programs from the theme sets
programs = generate_programs(theme_sets)

# Set up the DataGenerator (using 'whole' to generate the full program)
for p in programs:
    dg = DataGenerator(p, splice_params='whole')
    dg.generate_data(cnl_levels=cnl_levels, nl_levels=nl_levels)
    dg.get_all_data()


# How this was done: 
from AspPy2 import ASPProgram, DataGenerator

def model_program_1():
    p = ASPProgram()

    # Add lines for each component and selection constraint
    cpu = p.add_line(
        'cpu("^CPU1^"; "i5").',
        {'simple': '^CPU1^ and i5 are CPUs.'},
        {'simple': 'There are two CPUs available: ^CPU1^ and i5.'},
        label='cpu'
    )
    cpu_choice = p.add_line(
        '1 { selected_cpu(C) : cpu(C) } 1.',
        {'simple': 'Select exactly one CPU from ^CPU1^, i5.'},
        {'simple': 'You must choose one CPU: ^CPU1^ or i5.'},
        label='cpu_choice'
    )

    gpu = p.add_line(
        'gpu("GTX1660"; "RX580").',
        {'simple': 'GTX1660 and RX580 are GPUs.'},
        {'simple': 'There are two GPUs available: GTX1660 and RX580.'},
        label='gpu'
    )
    gpu_choice = p.add_line(
        '1 { selected_gpu(G) : gpu(G) } 1.',
        {'simple': 'Select exactly one GPU from GTX1660, RX580.'},
        {'simple': 'You must choose one GPU: GTX1660 or RX580.'},
        label='gpu_choice'
    )

    p.add_group(
        [cpu, gpu, cpu_choice, gpu_choice],
        {
            'simple/4': 'You must select only one of the available CPUs: ^CPU1^, i5 and one of the availale GPUS GTX1660 or RX580: '
        }
    )

    mobo = p.add_line(
        'mobo("B450"; "Z390").',
        {'simple': 'B450 and Z390 are motherboards.'},
        {'simple': 'There are two motherboards available: B450 and Z390.'},
        label='mobo'
    )
    mobo_choice = p.add_line(
        '1 { selected_mobo(M) : mobo(M) } 1.',
        {'simple': 'Select exactly one motherboard from {B450, Z390}.'},
        {'simple': 'You must choose one motherboard: B450 or Z390.'},
        label='mobo_choice'
    )

    p.add_group(
        [mobo, mobo_choice],
        {
            'simple/2': 'You must select only one of the availbe Motherboards: B450 or Z390.'
        }
    ) 

    # Add compatibility constraints
    req1 = p.add_line(
        ':- selected_cpu("^CPU1^"), selected_mobo(M), M != "B450".',
        {'simple': 'The ^CPU1^ CPU requires the B450 motherboard.'},
        {'simple': 'If you select ^CPU1^, you must use B450 as the motherboard.'},
        label='req1'
    )
    req2 = p.add_line(
        ':- selected_cpu("i5"), selected_mobo(M), M != "Z390".',
        {'simple': 'The i5 CPU requires the Z390 motherboard.'},
        {'simple': 'If you select i5, you must use Z390 as the motherboard.'},
        label='req2'
    )
    req3 = p.add_line(
        ':- selected_gpu("RX580"), selected_mobo("Z390").',
        {'simple': 'The RX580 GPU is incompatible with the Z390 motherboard.'},
        {'simple': 'You cannot use RX580 with Z390.'},
        label='req3'
    )

    variations = {
        'CPU1': ['Ryzen5', 'Ryzen4']
    }

    p.add_variations(variations)

    return p

p = model_program_1()

cnl_levels = {'simple': ['simple']}
nl_levels = {'simple': ['simple']}

dg = DataGenerator(p, splice_params='whole')
dg.generate_data(cnl_levels=cnl_levels, nl_levels=nl_levels)
dg.get_all_data()

# okay I'm going to show you an example of how I want you to model the data

# We need to convert the given example to placeholders 
# This means we take all teh theme-specific information out, and encapsulate that somewhere else
# here is an example of a program going from theme specific, to palceholder notation:

'''
cpu("Ryzen5"; "i5").
1 { selected_cpu(C) : cpu(C) } 1.

gpu("GTX1660"; "RX580").
1 { selected_gpu(G) : gpu(G) } 1.

goes to

{P1}("{V1}"; "{V2}").
1 { {P2}({P6}) : {P1}({P6}) } 1.

{P3}("{V3}"; "{V4}").
1 { {P4}({P7}) : {P3}({P7}) } 1.
'''

# Now we can substitude theme-sepcific information in and the ASP code will still make sense
# For examples, for P1, we can substitute 'cpu'

# We can incapsulate theme specific information like this: 

'''
theme_sets = [
    # Theme1 - computer themes
    {
        'P1': 'cpu',
        'P2': 'selected_cpu'
        etc
    }
    etc
]
'''

# Now we can easily move between themes - retaining the underlying problem pattern
# Now we can also make use of AspPy2's variations within that. 
# If we now include that functionaity, the program becomes

'''
{P1}("{V1}"; "{V2}").
1 { {P2}({P6}) : {P1}({P6}) } 1.

{P3}("GTX1660"; "RX580").
1 { {P4}({P7}) : {P3}({P7}) } 1.

to 

{P1}("^{V1}^"; "^{V2}^").
1 { {P2}({P6}) : {P1}({P6}) } 1.

{P3}("^{V3}^"; "^{V4}^").
1 { {P4}({P7}) : {P3}({P7}) } 1.
'''

# in our theme_sets, we can also pass a dictionary of variations for each of these placeholders
'''
theme_sets = [
    # Theme1 - computer themes
    {
        'P1': 'cpu',
        'P2': 'selected_cpu'
        'variations': {'V1': [etc etc], 'V2': [etc etc]}
    }
    etc
]
'''

# We cna then iterate over theme sets and dynamically create multiple programs
