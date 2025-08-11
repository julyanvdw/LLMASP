from AspPy2 import ASPProgram, DataGenerator

# Define the theme set for the computer build problem
theme_sets = [
    # THEME 1 - computer building
    {
        'P1': 'cpu',
        'P2': 'selected_cpu',
        'P3': 'gpu',
        'P4': 'selected_gpu',
        'P5': 'mobotherboard',
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
            'V1': ['Ryzen5', 'Ryzen7'],
            'V2': ['i5', 'Pentium'],
            'V3': ['GTX1660', 'RTX2060'],
            'V4': ['RX580', 'R7 240'],
            'V5': ['B450', 'X570'],
            'V6': ['Z390', 'Z490']
        },
        'theme': 'PC',
        'verb': 'build',
    }
]

def generate_programs(theme_sets):
    generated_programs = []

    for theme in theme_sets:
        p = ASPProgram()

        # CPU
        cpu_fact = p.add_line(
            '{P1}("^V1^"; "^V2^").'.format(**theme),
            {
                'simple': '^V1^, ^V2^ are {P1}.'.format(**theme),
                'alt1': 'Choose a {P1}: ^V1^ or ^V2^.'.format(**theme),
                'alt2': 'Available {P1}s: ^V1^, ^V2^.'.format(**theme)
            },
            {
                'nl1': 'You can pick either ^V1^ or ^V2^ as your {P1}.'.format(**theme),
                'nl2': 'For your {theme}, select a {P1} from the options ^V1^ and ^V2^.'.format(**theme),
                'nl3': 'The {P1} choices are ^V1^ and ^V2^.'.format(**theme),
                'nl4': 'Pick one {P1}: ^V1^ or ^V2^.'.format(**theme),
                'nl5': 'You have two {P1} options: ^V1^ and ^V2^.'.format(**theme),
                'nl6': 'Select your preferred {P1}, either ^V1^ or ^V2^.'.format(**theme),
                'nl7': 'Choose between ^V1^ and ^V2^ for the {P1} slot.'.format(**theme),
                'nl8': 'Your {P1} must be one of the following: ^V1^, ^V2^.'.format(**theme),
                'nl9': 'For this {theme}, you may use ^V1^ or ^V2^ as the {P1}.'.format(**theme),
                'nl10': 'The available {P1}s for this build are ^V1^ and ^V2^.'.format(**theme)
            },
            label='{P1}'.format(**theme)
        )
        cpu_choice = p.add_line(
            '1 {{ {P2}({C}) : {P1}({C}) }} 1.'.format(**theme),
            {
                'simple': 'Exactly one {P1} must be selected.'.format(**theme),
                'alt1': 'Pick only one {P1}.'.format(**theme),
                'alt2': 'You must choose a single {P1}.'.format(**theme)
            },
            {
                'nl1': 'Make sure to select just one {P1} for your {theme}.'.format(**theme),
                'nl2': 'Only one {P1} can be chosen.'.format(**theme),
                'nl3': 'You are required to pick a single {P1}.'.format(**theme),
                'nl4': 'Select one and only one {P1}.'.format(**theme),
                'nl5': 'Choose exactly one {P1} for this {theme}.'.format(**theme),
                'nl6': 'Your {theme} must include only one {P1}.'.format(**theme),
                'nl7': 'Ensure that you do not select more than one {P1}.'.format(**theme),
                'nl8': 'Pick a single {P1} from the available options.'.format(**theme),
                'nl9': 'One {P1} must be chosen for the configuration.'.format(**theme),
                'nl10': 'You cannot select more than one {P1} for this {theme}.'.format(**theme)
            },
            label='{P2}'.format(**theme)
        )
        
        p.add_group(
            [cpu_fact, cpu_choice],
            {
                'nl1/2': 'Select exactly one {P1} from ^V1^, ^V2^.'.format(**theme),
                'nl2/2': 'Pick a {P1} for your {theme}: ^V1^ or ^V2^.'.format(**theme),
                'nl3/2': 'Choose one {P1} from the available options.'.format(**theme),
                'nl4/2': 'For your {theme}, select a {P1} from ^V1^ and ^V2^.'.format(**theme),
                'nl5/2': 'You must pick a single {P1}: ^V1^ or ^V2^.'.format(**theme),
                'nl6/2': 'Exactly one {P1} is required for your {theme}.'.format(**theme),
                'nl7/2': 'Choose between ^V1^ and ^V2^ as your {P1}.'.format(**theme),
                'nl8/2': 'Select your {P1} from the following: ^V1^, ^V2^.'.format(**theme),
                'nl9/2': 'Your {theme} must include one {P1}: ^V1^ or ^V2^.'.format(**theme),
                'nl10/2': 'Pick either ^V1^ or ^V2^ as your {P1} for this {theme}.'.format(**theme)
            }
        )

        # GPU
        gpu_fact = p.add_line(
            '{P3}("^V3^"; "^V4^").'.format(**theme),
            {
                'simple': '^V3^, ^V4^ are {P3}.'.format(**theme),
                'alt1': 'Choose a {P3}: ^V3^ or ^V4^.'.format(**theme),
                'alt2': 'Available {P3}s: ^V3^, ^V4^.'.format(**theme)
            },
            {
                'nl1': 'You can pick either ^V3^ or ^V4^ as your {P3}.'.format(**theme),
                'nl2': 'For your {theme}, select a {P3} from the options ^V3^ and ^V4^.'.format(**theme),
                'nl3': 'The {P3} choices are ^V3^ and ^V4^.'.format(**theme),
                'nl4': 'Pick one {P3}: ^V3^ or ^V4^.'.format(**theme),
                'nl5': 'You have two {P3} options: ^V3^ and ^V4^.'.format(**theme),
                'nl6': 'Select your preferred {P3}, either ^V3^ or ^V4^.'.format(**theme),
                'nl7': 'Choose between ^V3^ and ^V4^ for the {P3} slot.'.format(**theme),
                'nl8': 'Your {P3} must be one of the following: ^V3^, ^V4^.'.format(**theme),
                'nl9': 'For this {theme}, you may use ^V3^ or ^V4^ as the {P3}.'.format(**theme),
                'nl10': 'The available {P3}s for this build are ^V3^ and ^V4^.'.format(**theme)
            },
            label='{P3}'.format(**theme)
        )
        gpu_choice = p.add_line(
            '1 {{ {P4}({G}) : {P3}({G}) }} 1.'.format(**theme),
            {
                'simple': 'Exactly one {P3} must be selected.'.format(**theme),
                'alt1': 'Pick only one {P3}.'.format(**theme),
                'alt2': 'You must choose a single {P3}.'.format(**theme)
            },
            {
                'nl1': 'Make sure to select just one {P3} for your {theme}.'.format(**theme),
                'nl2': 'Only one {P3} can be chosen.'.format(**theme),
                'nl3': 'You are required to pick a single {P3}.'.format(**theme),
                'nl4': 'Select one and only one {P3}.'.format(**theme),
                'nl5': 'Choose exactly one {P3} for this {theme}.'.format(**theme),
                'nl6': 'Your {theme} must include only one {P3}.'.format(**theme),
                'nl7': 'Ensure that you do not select more than one {P3}.'.format(**theme),
                'nl8': 'Pick a single {P3} from the available options.'.format(**theme),
                'nl9': 'One {P3} must be chosen for the configuration.'.format(**theme),
                'nl10': 'You cannot select more than one {P3} for this {theme}.'.format(**theme)
            },
            label='{P4}'.format(**theme)
        )
        
        p.add_group(
            [gpu_fact, gpu_choice],
            {
                'nl1/2': 'Select exactly one {P3} from ^V3^, ^V4^.'.format(**theme),
                'nl2/2': 'Pick a {P3} for your {theme}: ^V3^ or ^V4^.'.format(**theme),
                'nl3/2': 'Choose one {P3} from the available options.'.format(**theme),
                'nl4/2': 'For your {theme}, select a {P3} from ^V3^ and ^V4^.'.format(**theme),
                'nl5/2': 'You must pick a single {P3}: ^V3^ or ^V4^.'.format(**theme),
                'nl6/2': 'Exactly one {P3} is required for your {theme}.'.format(**theme),
                'nl7/2': 'Choose between ^V3^ and ^V4^ as your {P3}.'.format(**theme),
                'nl8/2': 'Select your {P3} from the following: ^V3^, ^V4^.'.format(**theme),
                'nl9/2': 'Your {theme} must include one {P3}: ^V3^ or ^V4^.'.format(**theme),
                'nl10/2': 'Pick either ^V3^ or ^V4^ as your {P3} for this {theme}.'.format(**theme)
            }
        )

        # Motherboard
        mobo_fact = p.add_line(
            '{P5}("^V5^"; "^V6^").'.format(**theme),
            {
                'simple': '^V5^, ^V6^ are {P5}.'.format(**theme),
                'alt1': 'Choose a {P5}: ^V5^ or ^V6^.'.format(**theme),
                'alt2': 'Available {P5}s: ^V5^, ^V6^.'.format(**theme)
            },
            {
                'nl1': 'You can pick either ^V5^ or ^V6^ as your {P5}.'.format(**theme),
                'nl2': 'For your {theme}, select a {P5} from the options ^V5^ and ^V6^.'.format(**theme),
                'nl3': 'The {P5} choices are ^V5^ and ^V6^.'.format(**theme),
                'nl4': 'Pick one {P5}: ^V5^ or ^V6^.'.format(**theme),
                'nl5': 'You have two {P5} options: ^V5^ and ^V6^.'.format(**theme),
                'nl6': 'Select your preferred {P5}, either ^V5^ or ^V6^.'.format(**theme),
                'nl7': 'Choose between ^V5^ and ^V6^ for the {P5} slot.'.format(**theme),
                'nl8': 'Your {P5} must be one of the following: ^V5^, ^V6^.'.format(**theme),
                'nl9': 'For this {theme}, you may use ^V5^ or ^V6^ as the {P5}.'.format(**theme),
                'nl10': 'The available {P5}s for this build are ^V5^ and ^V6^.'.format(**theme)
            },
            label='{P5}'.format(**theme)
        )
        mobo_choice = p.add_line(
            '1 {{ {P6}({M}) : {P5}({M}) }} 1.'.format(**theme),
            {
                'simple': 'Exactly one {P5} must be selected.'.format(**theme),
                'alt1': 'Pick only one {P5}.'.format(**theme),
                'alt2': 'You must choose a single {P5}.'.format(**theme)
            },
            {
                'nl1': 'Make sure to select just one {P5} for your {theme}.'.format(**theme),
                'nl2': 'Only one {P5} can be chosen.'.format(**theme),
                'nl3': 'You are required to pick a single {P5}.'.format(**theme),
                'nl4': 'Select one and only one {P5}.'.format(**theme),
                'nl5': 'Choose exactly one {P5} for this {theme}.'.format(**theme),
                'nl6': 'Your {theme} must include only one {P5}.'.format(**theme),
                'nl7': 'Ensure that you do not select more than one {P5}.'.format(**theme),
                'nl8': 'Pick a single {P5} from the available options.'.format(**theme),
                'nl9': 'One {P5} must be chosen for the configuration.'.format(**theme),
                'nl10': 'You cannot select more than one {P5} for this {theme}.'.format(**theme)
            },
            label='{P6}'.format(**theme)
        )
        
        p.add_group(
            [mobo_fact, mobo_choice],
            {
                'nl1/2': 'Select exactly one {P5} from ^V5^, ^V6^.'.format(**theme),
                'nl2/2': 'Pick a {P5} for your {theme}: ^V5^ or ^V6^.'.format(**theme),
                'nl3/2': 'Choose one {P5} from the available options.'.format(**theme),
                'nl4/2': 'For your {theme}, select a {P5} from ^V5^ and ^V6^.'.format(**theme),
                'nl5/2': 'You must pick a single {P5}: ^V5^ or ^V6^.'.format(**theme),
                'nl6/2': 'Exactly one {P5} is required for your {theme}.'.format(**theme),
                'nl7/2': 'Choose between ^V5^ and ^V6^ as your {P5}.'.format(**theme),
                'nl8/2': 'Select your {P5} from the following: ^V5^, ^V6^.'.format(**theme),
                'nl9/2': 'Your {theme} must include one {P5}: ^V5^ or ^V6^.'.format(**theme),
                'nl10/2': 'Pick either ^V5^ or ^V6^ as your {P5} for this {theme}.'.format(**theme)
            }
        )

        # ALL selection group
        p.add_group(
            [cpu_fact, cpu_choice, gpu_fact, gpu_choice, mobo_fact, mobo_choice],
            {
                'nl1/6': "You are assembling a basic custom {theme} using three components: a {P1}, a {P3}, and a {P5}. Each final build must include exactly one {P1}, one {P3}, and one {P5}.".format(**theme),
                'nl2/6': "To {verb} your {theme}, select one {P1}, one {P3}, and one {P5} from the available options.".format(**theme),
                'nl3/6': "For this configuration, you must pick exactly one {P1}, {P3}, and {P5} for your system.".format(**theme),
                'nl4/6': "Build your {theme} by choosing a {P1}, a {P3}, and a {P5}.".format(**theme),
                'nl5/6': "Your {theme} requires one {P1}, one {P3}, and one {P5}.".format(**theme),
                'nl6/6': "Select a {P1}, {P3}, and {P5} to complete your {theme}.".format(**theme),
                'nl7/6': "Exactly one {P1}, {P3}, and {P5} must be chosen for this {theme}.".format(**theme),
                'nl8/6': "Pick your preferred {P1}, {P3}, and {P5} for the build.".format(**theme),
                'nl9/6': "Choose one of each: {P1}, {P3}, and {P5}.".format(**theme),
                'nl10/6': "Your build is only valid with one {P1}, one {P3}, and one {P5}.".format(**theme)
            }
        )

        # Compatibility constraints
        req1 = p.add_line(
            ':- {P2}("^V1^"), {P6}(M), M != "^V5^".'.format(**theme),
            {
                'simple': 'The ^V1^ {P1} requires the ^V5^ {P5}.'.format(**theme),
                'alt1': '^V1^ can only be used with ^V5^.'.format(**theme),
                'alt2': 'If you pick ^V1^, you must also pick ^V5^ as the {P5}.'.format(**theme)
            },
            {
                'nl1': 'If you select ^V1^ as your {P1}, you must use ^V5^ as your {P5}.'.format(**theme),
                'nl2': '^V1^ is only compatible with ^V5^ as a {P5}.'.format(**theme),
                'nl3': 'Choosing ^V1^ restricts you to ^V5^ for the {P5}.'.format(**theme),
                'nl4': 'You cannot pair ^V1^ with any {P5} except ^V5^.'.format(**theme),
                'nl5': 'Selecting ^V1^ means you must select ^V5^ as your {P5}.'.format(**theme),
                'nl6': 'The ^V1^ {P1} only works with the ^V5^ {P5}.'.format(**theme),
                'nl7': 'If you want ^V1^, your only {P5} option is ^V5^.'.format(**theme),
                'nl8': 'The ^V1^ {P1} is not compatible with any {P5} other than ^V5^.'.format(**theme),
                'nl9': 'Only ^V5^ can be used with ^V1^ as the {P1}.'.format(**theme),
                'nl10': 'Selecting ^V1^ forces you to pick ^V5^ as your {P5}.'.format(**theme)
            },
            label='req1'
        )
        
        req2 = p.add_line(
            ':- {P2}("^V2^"), {P6}(M), M != "^V6^".'.format(**theme),
            {
                'simple': 'The ^V2^ {P1} requires the ^V6^ {P5}.'.format(**theme),
                'alt1': '^V2^ can only be used with ^V6^.'.format(**theme),
                'alt2': 'If you pick ^V2^, you must also pick ^V6^ as the {P5}.'.format(**theme)
            },
            {
                'nl1': 'If you select ^V2^ as your {P1}, you must use ^V6^ as your {P5}.'.format(**theme),
                'nl2': '^V2^ is only compatible with ^V6^ as a {P5}.'.format(**theme),
                'nl3': 'Choosing ^V2^ restricts you to ^V6^ for the {P5}.'.format(**theme),
                'nl4': 'You cannot pair ^V2^ with any {P5} except ^V6^.'.format(**theme),
                'nl5': 'Selecting ^V2^ means you must select ^V6^ as your {P5}.'.format(**theme),
                'nl6': 'The ^V2^ {P1} only works with the ^V6^ {P5}.'.format(**theme),
                'nl7': 'If you want ^V2^, your only {P5} option is ^V6^.'.format(**theme),
                'nl8': 'The ^V2^ {P1} is not compatible with any {P5} other than ^V6^.'.format(**theme),
                'nl9': 'Only ^V6^ can be used with ^V2^ as the {P1}.'.format(**theme),
                'nl10': 'Selecting ^V2^ forces you to pick ^V6^ as your {P5}.'.format(**theme)
            },
            label='req2'
        )
        
        req3 = p.add_line(
            ':- {P4}("^V4^"), {P6}("^V6^").'.format(**theme),
            {
                'simple': 'The ^V4^ {P3} is incompatible with the ^V6^ {P5}.'.format(**theme),
                'alt1': 'You cannot use ^V4^ with ^V6^.'.format(**theme),
                'alt2': '^V4^ and ^V6^ are not compatible.'.format(**theme)
            },
            {
                'nl1': 'You cannot use ^V4^ as your {P3} with ^V6^ as your {P5}.'.format(**theme),
                'nl2': '^V4^ is not compatible with ^V6^ as a {P5}.'.format(**theme),
                'nl3': 'If you pick ^V4^, do not pick ^V6^ as your {P5}.'.format(**theme),
                'nl4': 'Avoid pairing ^V4^ with ^V6^ in your {theme}.'.format(**theme),
                'nl5': 'Selecting ^V4^ means you cannot select ^V6^ as your {P5}.'.format(**theme),
                'nl6': 'The ^V4^ {P3} does not work with the ^V6^ {P5}.'.format(**theme),
                'nl7': 'If you want ^V4^, you cannot use ^V6^ as your {P5}.'.format(**theme),
                'nl8': 'The ^V4^ {P3} is not compatible with any {theme} using ^V6^.'.format(**theme),
                'nl9': 'Only builds without ^V6^ can use ^V4^ as the {P3}.'.format(**theme),
                'nl10': 'Selecting ^V4^ forces you to avoid ^V6^ as your {P5}.'.format(**theme)
            },
            label='req3'
        )

        p.add_variations(theme['variations'])
        generated_programs.append(p)

    return generated_programs

# Set up CNL and NL levels
cnl_levels = {
    'simple': ['simple'],
    'alt1': ['alt1'],
    'alt2': ['alt2']
}
nl_levels = {
    'nl1': ['nl1'],
    'nl2': ['nl2'],
    'nl3': ['nl3'],
    'nl4': ['nl4'],
    'nl5': ['nl5'],
    'nl6': ['nl6'],
    'nl7': ['nl7'],
    'nl8': ['nl8'],
    'nl9': ['nl9'],
    'nl10': ['nl10'],
    'nl1/2': ['nl1/2'],
    'nl2/2': ['nl2/2'],
    'nl3/2': ['nl3/2'],
    'nl4/2': ['nl4/2'],
    'nl5/2': ['nl5/2'],
    'nl6/2': ['nl6/2'],
    'nl7/2': ['nl7/2'],
    'nl8/2': ['nl8/2'],
    'nl9/2': ['nl9/2'],
    'nl10/2': ['nl10/2'],
    'nl1/6': ['nl1/6'],
    'nl2/6': ['nl2/6'],
    'nl3/6': ['nl3/6'],
    'nl4/6': ['nl4/6'],
    'nl5/6': ['nl5/6'],
    'nl6/6': ['nl6/6'],
    'nl7/6': ['nl7/6'],
    'nl8/6': ['nl8/6'],
    'nl9/6': ['nl9/6'],
    'nl10/6': ['nl10/6']
}

# Generate the programs from the theme sets
programs = generate_programs(theme_sets)

# Generate and print all data for each program
for p in programs:
    dg = DataGenerator(p, splice_params='whole')
    dg.generate_data(cnl_levels=cnl_levels, nl_levels=nl_levels)
    dg.get_all_data()