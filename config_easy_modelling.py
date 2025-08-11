from AspPy2 import ASPProgram, DataGenerator
import random
import json

# Define the theme set for the computer build problem
theme_sets = [
    # THEME 1 - computer building
    {
        'P1': 'cpu',
        'P2': 'selected_cpu',
        'P3': 'gpu',
        'P4': 'selected_gpu',
        'P5': 'motherboard',
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
            'V4': ['RX580', 'R7240'],
            'V5': ['B450', 'X570'],
            'V6': ['Z390', 'Z490']
        },
        'theme': 'PC',
        'verb': 'build',
    },
    # THEME 2 - audio system
    {
        'P1': 'speaker',
        'P2': 'selected_speaker',
        'P3': 'amplifier',
        'P4': 'selected_amplifier',
        'P5': 'player',
        'P6': 'selected_player',
        'V1': 'Alpha',
        'V2': 'Beta',
        'V3': 'AmpX',
        'V4': 'AmpY',
        'V5': 'Streamer1',
        'V6': 'Streamer2',
        'C': 'S',
        'G': 'A',
        'M': 'P',
        'variations': {
            'V1': ['Alpha', 'Beta'],
            'V2': ['Phi', 'Gamma'],
            'V3': ['AmpX', 'AmpY'],
            'V4': ['AmpZ', 'AmpW'],
            'V5': ['Streamer1', 'Streamer2'],
            'V6': ['Streamer3', 'Streamer4']
        },
        'theme': 'Audio System',
        'verb': 'assemble',
    },
    # THEME 3 - mobile plan
    {
        'P1': 'plan',
        'P2': 'selected_plan',
        'P3': 'phone',
        'P4': 'selected_phone',
        'P5': 'accessory',
        'P6': 'selected_accessory',
        'V1': 'BasicData',
        'V2': 'PremiumData',
        'V3': 'ModelX',
        'V4': 'ModelY',
        'V5': 'CaseA',
        'V6': 'CaseB',
        'C': 'P',
        'G': 'M',
        'M': 'A',
        'variations': {
            'V1': ['BasicData', 'PremiumData'],
            'V2': ['Yodata', 'GoodData'],
            'V3': ['ModelX', 'ModelY'],
            'V4': ['ModelZ', 'ModelW'],
            'V5': ['CaseA', 'CaseB'],
            'V6': ['CaseC', 'CaseD']
        },
        'theme': 'Mobile Plan',
        'verb': 'choose',
    },
    # THEME 4 - travel package
    {
        'P1': 'flight',
        'P2': 'selected_flight',
        'P3': 'hotel',
        'P4': 'selected_hotel',
        'P5': 'tour',
        'P6': 'selected_tour',
        'V1': 'FlightA',
        'V2': 'FlightB',
        'V3': 'HotelX',
        'V4': 'HotelY',
        'V5': 'Tour1',
        'V6': 'Tour2',
        'C': 'F',
        'G': 'H',
        'M': 'T',
        'variations': {
            'V1': ['FlightA', 'FlightB'],
            'V2': ['FlightC', 'FlightD'],
            'V3': ['HotelX', 'HotelY'],
            'V4': ['HotelZ', 'HotelW'],
            'V5': ['Tour1', 'Tour2'],
            'V6': ['Tour3', 'Tour4']
        },
        'theme': 'Travel Package',
        'verb': 'plan',
    },
    # THEME 5 - pizza order
    {
        'P1': 'base',
        'P2': 'selected_base',
        'P3': 'sauce',
        'P4': 'selected_sauce',
        'P5': 'topping',
        'P6': 'selected_topping',
        'V1': 'ThinCrust',
        'V2': 'DeepDish',
        'V3': 'Tomato',
        'V4': 'Pesto',
        'V5': 'Pepperoni',
        'V6': 'Mushroom',
        'C': 'B',
        'G': 'S',
        'M': 'T',
        'variations': {
            'V1': ['ThinCrust', 'DeepDish'],
            'V2': ['StuffedCrust', 'Flatbread'],
            'V3': ['Tomato', 'Pesto'],
            'V4': ['Alfredo', 'BBQ'],
            'V5': ['Pepperoni', 'Mushroom'],
            'V6': ['Onion', 'Olive']
        },
        'theme': 'Pizza Order',
        'verb': 'order',
    },  
    # THEME 6 - car rental
    {
        'P1': 'car',
        'P2': 'selected_car',
        'P3': 'insurance',
        'P4': 'selected_insurance',
        'P5': 'gps',
        'P6': 'selected_gps',
        'V1': 'Sedan',
        'V2': 'SUV',
        'V3': 'BasicCover',
        'V4': 'FullCover',
        'V5': 'GPS1',
        'V6': 'GPS2',
        'C': 'C',
        'G': 'I',
        'M': 'G',
        'variations': {
            'V1': ['Sedan', 'SUV'],
            'V2': ['Convertible', 'Truck'],
            'V3': ['BasicCover', 'FullCover'],
            'V4': ['PremiumCover', 'StandardCover'],
            'V5': ['GPS1', 'GPS2'],
            'V6': ['GPS3', 'GPS4']
        },
        'theme': 'Car Rental',
        'verb': 'rent',
    },
    # THEME 7 - online course bundle
    {
        'P1': 'course',
        'P2': 'selected_course',
        'P3': 'textbook',
        'P4': 'selected_textbook',
        'P5': 'project',
        'P6': 'selected_project',
        'V1': 'Math101',
        'V2': 'CS102',
        'V3': 'TextA',
        'V4': 'TextB',
        'V5': 'ProjX',
        'V6': 'ProjY',
        'C': 'C',
        'G': 'T',
        'M': 'P',
        'variations': {
            'V1': ['Math101', 'CS102'],
            'V2': ['Bio103', 'Chem104'],
            'V3': ['TextA', 'TextB'],
            'V4': ['TextC', 'TextD'],
            'V5': ['ProjX', 'ProjY'],
            'V6': ['ProjZ', 'ProjW']
        },
        'theme': 'Course Bundle',
        'verb': 'enroll',
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
                'nl10': 'The available {P1}s for this {verb} are ^V1^ and ^V2^.'.format(**theme)
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
                'nl10': 'The available {P3}s for this {verb} are ^V3^ and ^V4^.'.format(**theme)
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
                'nl10': 'The available {P5}s for this {verb} are ^V5^ and ^V6^.'.format(**theme)
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
                'nl1/6': "You are assembling a basic custom {theme} using three components: a {P1}, a {P3}, and a {P5}. Each final {verb} must include exactly one {P1}, one {P3}, and one {P5}.".format(**theme),
                'nl2/6': "To {verb} your {theme}, select one {P1}, one {P3}, and one {P5} from the available options.".format(**theme),
                'nl3/6': "For this configuration, you must pick exactly one {P1}, {P3}, and {P5} for your system.".format(**theme),
                'nl4/6': "Build your {theme} by choosing a {P1}, a {P3}, and a {P5}.".format(**theme),
                'nl5/6': "Your {theme} requires one {P1}, one {P3}, and one {P5}.".format(**theme),
                'nl6/6': "Select a {P1}, {P3}, and {P5} to complete your {theme}.".format(**theme),
                'nl7/6': "Exactly one {P1}, {P3}, and {P5} must be chosen for this {theme}.".format(**theme),
                'nl8/6': "Pick your preferred {P1}, {P3}, and {P5} for the {verb}.".format(**theme),
                'nl9/6': "Choose one of each: {P1}, {P3}, and {P5}.".format(**theme),
                'nl10/6': "Your {verb} is only valid with one {P1}, one {P3}, and one {P5}.".format(**theme)
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
                'nl9': 'Only {verb}s without ^V6^ can use ^V4^ as the {P3}.'.format(**theme),
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

# Splice params: single lines up to full programs, 2 random samples per size
splice_params = {
    'strategy': 'multi_granularity',
    'min_size': 1,
    'max_size': 9,  # None = up to full program
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
output_cnl_asp = "easy_config_cnl_to_asp_20k.jsonl"
output_nl_cnl = "easy_config_nl_to_cnl_20k.jsonl"

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

print("Easy config modelling complete!")