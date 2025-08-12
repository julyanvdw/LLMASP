from AspPy2 import ASPProgram, DataGenerator
import random
import json

theme_sets = [
    {
        'P1': 'cpu',
        'P2': 'selected_cpu',
        'P3': 'gpu',
        'P4': 'selected_gpu',
        'P5': 'mobo',
        'P6': 'selected_mobo',
        'P7': 'psu',
        'P8': 'selected_psu',
        'P9': 'high_power',
        'theme': 'Workstation Build',
        'verb': 'assemble',
        # 'variations': {
        #     'V1': ['Ryzen7', 'i9', 'Xeon'],
        #     'V2': ['i9', 'Xeon', 'Ryzen7'],
        #     'V3': ['Xeon', 'Ryzen7', 'i9'],
        #     'V4': ['RTX4060', 'RTX3090', 'Quadro'],
        #     'V5': ['RTX3090', 'Quadro', 'RTX4060'],
        #     'V6': ['Quadro', 'RTX4060', 'RTX3090'],
        #     'V7': ['X670', 'Z690', 'C621'],
        #     'V8': ['Z690', 'C621', 'X670'],
        #     'V9': ['C621', 'X670', 'Z690'],
        #     'V10': ['Bronze', 'Gold', 'Platinum'],
        #     'V11': ['Gold', 'Platinum', 'Bronze'],
        #     'V12': ['Platinum', 'Bronze', 'Gold'],
        #     'C1': ['300', '400', '500'],
        #     'C2': ['400', '500', '300'],
        #     'C3': ['500', '300', '400'],
        #     'C4': ['350', '700', '800'],
        #     'C5': ['700', '800', '350'],
        #     'C6': ['800', '350', '700'],
        #     'C7': ['180', '200', '250'],
        #     'C8': ['200', '250', '180'],
        #     'C9': ['250', '180', '200'],
        #     'C10': ['80', '120', '160'],
        #     'C11': ['120', '160', '80'],
        #     'C12': ['160', '80', '120']
        # }
        'variations': {
            'V1': ['Ryzen7'],
            'V2': ['i9'],
            'V3': ['Xeon'],
            'V4': ['RTX4060'],
            'V5': ['RTX3090'],
            'V6': ['Quadro'],
            'V7': ['X670'],
            'V8': ['Z690'],
            'V9': ['C621',],
            'V10': ['Bronze',],
            'V11': ['Gold'],
            'V12': ['Platinum'],
            'C1': ['300',],
            'C2': ['400',],
            'C3': ['500',],
            'C4': ['350',],
            'C5': ['700',],
            'C6': ['800',],
            'C7': ['180',],
            'C8': ['200',],
            'C9': ['250',],
            'C10': ['80',],
            'C11': ['120',],
            'C12': ['160',]
        }
    }
]

def generate_programs(theme_sets):
    programs = []
    for theme in theme_sets:
        p = ASPProgram()

        # CPU group
        cpu = p.add_line(
            '{P1}("^V1^", ^C1^; "^V2^", ^C2^; "^V3^", ^C3^).'.format(**theme),
            {
                'simple': 'Select one {P1} from ^V1^, ^V2^, ^V3^, with costs: ^V1^ = ^C1^, ^V2^ = ^C2^, ^V3^ = ^C3^.'.format(**theme),
                'simple2': 'Available {P1}s: ^V1^ (^C1^), ^V2^ (^C2^), ^V3^ (^C3^).'.format(**theme),
                'simple3': 'Pick from these {P1}s for your {verb}: ^V1^ (^C1^), ^V2^ (^C2^), or ^V3^ (^C3^).'.format(**theme)
            },
            {
                'nl1': 'Pick a {P1}: ^V1^, ^V2^, or ^V3^.',
                'nl2': 'Choose one {P1} for your {verb}: ^V1^, ^V2^, ^V3^.',
                'nl3': 'Select a {P1} from the following options: ^V1^, ^V2^, ^V3^.',
                'nl4': 'For your {verb}, you need to choose a {P1}. The options are ^V1^, ^V2^, and ^V3^.',
                'nl5': 'You must select a {P1} for your {verb}. Available choices: ^V1^, ^V2^, ^V3^.',
                'nl6': 'Pick one {P1} for your {verb}. The available models are ^V1^, ^V2^, and ^V3^, each with its own price.',
                'nl7': 'To begin your {verb}, select a {P1}. ^V1^ costs ^C1^, ^V2^ costs ^C2^, and ^V3^ costs ^C3^.',
                'nl8': 'Start your {verb} by picking a {P1}. You can choose between ^V1^, ^V2^, or ^V3^, with prices ^C1^, ^C2^, and ^C3^ respectively.',
                'nl9': 'The first step in your {verb} is to decide on a {P1}. Consider ^V1^ (^C1^), ^V2^ (^C2^), or ^V3^ (^C3^).',
                'nl10': 'When assembling your {verb}, your first decision is which {P1} to use. The available options are ^V1^, ^V2^, and ^V3^, with costs of ^C1^, ^C2^, and ^C3^. Think about your needs and budget before making a choice.'
            }
        )
        cpu_choice = p.add_line(
            '1 {{ {P2}(C) : {P1}(C, _) }} 1.'.format(**theme),
            {
                'simple': 'Pick only one {P1}.'.format(**theme),
                'simple2': 'Only one {P1} can be selected for your {verb}.'.format(**theme),
                'simple3': 'Exactly one {P1} must be chosen for your {verb}.'.format(**theme)
            },
            {
                'nl1': 'Pick just one {P1}.',
                'nl2': 'Only one {P1} can be chosen.',
                'nl3': 'You must select exactly one {P1}.',
                'nl4': 'For your {verb}, only a single {P1} is allowed.',
                'nl5': 'Make sure you do not pick more than one {P1} for your {verb}.',
                'nl6': 'Your {verb} requires you to choose only one {P1}.',
                'nl7': 'Selecting more than one {P1} is not permitted for your {verb}.',
                'nl8': 'You are only allowed to select one {P1} for your {verb}.',
                'nl9': 'Be sure to pick just one {P1} for your {verb}. Multiple selections will result in an error.',
                'nl10': 'Exactly one {P1} must be chosen for your {verb}. Double-check your selection before proceeding.'
            }
        )

        p.add_group(
            [cpu, cpu_choice],
            {
                'nl1/2': 'Pick a {P1} for your {verb}. The available options are ^V1^, ^V2^, and ^V3^, with costs ^C1^, ^C2^, and ^C3^ respectively.',
                'nl2/2': 'Choose one {P1} from ^V1^, ^V2^, or ^V3^ for your {verb}. Each {P1} has a price: ^V1^ is ^C1^, ^V2^ is ^C2^, and ^V3^ is ^C3^.',
                'nl3/2': 'You need to select a {P1} for your {verb}. The options are ^V1^ (cost: ^C1^), ^V2^ (cost: ^C2^), and ^V3^ (cost: ^C3^).',
                'nl4/2': 'For your {verb}, you must pick exactly one {P1}. Your choices are ^V1^, ^V2^, and ^V3^, which cost ^C1^, ^C2^, and ^C3^.',
                'nl5/2': 'Start your {verb} by selecting a {P1}. Only one can be chosen: ^V1^ (^C1^), ^V2^ (^C2^), or ^V3^ (^C3^).',
                'nl6/2': 'The first step in your {verb} is to decide on a {P1}. Consider ^V1^, ^V2^, or ^V3^, each with a price of ^C1^, ^C2^, or ^C3^.',
                'nl7/2': 'You are required to pick exactly one {P1} for your {verb}. The available {P1}s are ^V1^ (cost: ^C1^), ^V2^ (cost: ^C2^), and ^V3^ (cost: ^C3^).',
                'nl8/2': 'When starting your {verb}, you must select a single {P1}. Each option—^V1^, ^V2^, or ^V3^—has a different price: ^C1^, ^C2^, or ^C3^.',
                'nl9/2': 'As you begin your {verb}, remember that you can only pick one {P1}. The choices are ^V1^, ^V2^, and ^V3^, with costs ^C1^, ^C2^, and ^C3^.',
                'nl10/2': 'To start your {verb}, select one {P1} from the following: ^V1^ (cost: ^C1^), ^V2^ (cost: ^C2^), or ^V3^ (cost: ^C3^). Review your options and choose the one that best fits your needs and budget.'
            }
        )

        # GPU group
        gpu = p.add_line(
            '{P3}("^V4^", ^C4^; "^V5^", ^C5^; "^V6^", ^C6^).'.format(**theme),
            {
                'simple': '^V4^, ^V5^, ^V6^, with costs: ^V4^ = ^C4^, ^V5^ = ^C5^, ^V6^ = ^C6^ are {P3}s.'.format(**theme),
                'simple2': 'Available {P3}s: ^V4^ (^C4^), ^V5^ (^C5^), ^V6^ (^C6^).'.format(**theme),
                'simple3': 'These are {P3}s for your {verb}: ^V4^ (^C4^), ^V5^ (^C5^), or ^V6^ (^C6^).'.format(**theme)
            },
            {
                'nl1': 'The available {P3}s are ^V4^ (^C4^), ^V5^ (^C5^), and ^V6^ (^C6^).',
                'nl2': 'For your {verb}, there are three {P3} options: ^V4^, ^V5^, and ^V6^, with costs ^C4^, ^C5^, and ^C6^ respectively.',
                'nl3': 'You will find {P3}s such as ^V4^ (cost: ^C4^), ^V5^ (cost: ^C5^), and ^V6^ (cost: ^C6^) available for your {verb}.',
                'nl4': 'Among the choices for {P3}s in your {verb} are ^V4^, ^V5^, and ^V6^, each with a price tag of ^C4^, ^C5^, and ^C6^.',
                'nl5': 'There exist several {P3} options for your {verb}: ^V4^ for ^C4^, ^V5^ for ^C5^, and ^V6^ for ^C6^.',
                'nl6': 'The models ^V4^, ^V5^, and ^V6^ are all available {P3}s for your {verb}, costing ^C4^, ^C5^, and ^C6^ respectively.',
                'nl7': 'In the context of your {verb}, the {P3}s ^V4^, ^V5^, and ^V6^ are present, with associated costs of ^C4^, ^C5^, and ^C6^.',
                'nl8': 'For assembling your {verb}, you will encounter {P3} options including ^V4^ (cost: ^C4^), ^V5^ (cost: ^C5^), and ^V6^ (cost: ^C6^).',
                'nl9': 'The set of {P3}s for your {verb} consists of ^V4^, ^V5^, and ^V6^, each priced at ^C4^, ^C5^, and ^C6^.',
                'nl10': 'When considering your {verb}, the {P3} components available are ^V4^, ^V5^, and ^V6^, with respective costs of ^C4^, ^C5^, and ^C6^.'
            }
        )
        gpu_choice = p.add_line(
            '1 {{ {P4}(G) : {P3}(G, _) }} 1.'.format(**theme),
            {
                'simple': 'Pick only one {P3}.'.format(**theme),
                'simple2': 'Only one {P3} can be selected for your {verb}.'.format(**theme),
                'simple3': 'Exactly one {P3} must be chosen for your {verb}.'.format(**theme)
            },
            {
                'nl1': 'Pick just one {P3} from ^V4^, ^V5^, or ^V6^ for your {verb}.',
                'nl2': 'Only one {P3} can be chosen: ^V4^, ^V5^, or ^V6^.',
                'nl3': 'You must select exactly one {P3} for your {verb} from ^V4^, ^V5^, ^V6^.',
                'nl4': 'For your {verb}, only a single {P3} is allowed. Choose from ^V4^, ^V5^, or ^V6^.',
                'nl5': 'Make sure you do not pick more than one {P3} for your {verb}. The options are ^V4^, ^V5^, and ^V6^.',
                'nl6': 'Your {verb} requires you to choose only one {P3}. Select from ^V4^, ^V5^, or ^V6^.',
                'nl7': 'Selecting more than one {P3} is not permitted for your {verb}. Choose either ^V4^, ^V5^, or ^V6^.',
                'nl8': 'You are only allowed to select one {P3} for your {verb}. The available choices are ^V4^, ^V5^, and ^V6^.',
                'nl9': 'Be sure to pick just one {P3} for your {verb}. Multiple selections from ^V4^, ^V5^, ^V6^ will result in an error.',
                'nl10': 'Exactly one {P3} must be chosen for your {verb}. Double-check your selection among ^V4^, ^V5^, and ^V6^ before proceeding.'
            }
        )
        p.add_group(
            [gpu, gpu_choice],
            {
                'nl1/2': 'Pick a {P3} for your {verb}. The available options are ^V4^, ^V5^, and ^V6^, with costs ^C4^, ^C5^, and ^C6^ respectively.',
                'nl2/2': 'Choose one {P3} from ^V4^, ^V5^, or ^V6^ for your {verb}. Each {P3} has a price: ^V4^ is ^C4^, ^V5^ is ^C5^, and ^V6^ is ^C6^.',
                'nl3/2': 'You need to select a {P3} for your {verb}. The options are ^V4^ (cost: ^C4^), ^V5^ (cost: ^C5^), and ^V6^ (cost: ^C6^).',
                'nl4/2': 'For your {verb}, you must pick exactly one {P3}. Your choices are ^V4^, ^V5^, and ^V6^, which cost ^C4^, ^C5^, and ^C6^.',
                'nl5/2': 'Continue your {verb} by selecting a {P3}. Only one can be chosen: ^V4^ (^C4^), ^V5^ (^C5^), or ^V6^ (^C6^).',
                'nl6/2': 'The next step in your {verb} is to decide on a {P3}. Consider ^V4^, ^V5^, or ^V6^, each with a price of ^C4^, ^C5^, or ^C6^.',
                'nl7/2': 'You are required to pick exactly one {P3} for your {verb}. The available {P3}s are ^V4^ (cost: ^C4^), ^V5^ (cost: ^C5^), and ^V6^ (cost: ^C6^).',
                'nl8/2': 'When building your {verb}, you must select a single {P3}. Each option—^V4^, ^V5^, or ^V6^—has a different price: ^C4^, ^C5^, or ^C6^.',
                'nl9/2': 'As you continue your {verb}, remember that you can only pick one {P3}. The choices are ^V4^, ^V5^, and ^V6^, with costs ^C4^, ^C5^, and ^C6^.',
                'nl10/2': 'To proceed with your {verb}, select one {P3} from the following: ^V4^ (cost: ^C4^), ^V5^ (cost: ^C5^), or ^V6^ (cost: ^C6^). Review your options and choose the one that best fits your needs and budget.'
            }
        )

        # MOBO group
        mobo = p.add_line(
            '{P5}("^V7^", ^C7^; "^V8^", ^C8^; "^V9^", ^C9^).'.format(**theme),
            {
                'simple': 'Available {P5}s: ^V7^ (^C7^), ^V8^ (^C8^), ^V9^ (^C9^).'.format(**theme),
                'simple2': 'Select {P5} from ^V7^, ^V8^, ^V9^, with costs: ^V7^ = ^C7^, ^V8^ = ^C8^, ^V9^ = ^C9^.'.format(**theme),
                'simple3': 'Pick from these {P5}s for your {verb}: ^V7^ (^C7^), ^V8^ (^C8^), or ^V9^ (^C9^).'.format(**theme)
            },
            {
                'nl1': 'There are {P5} options: ^V7^ (^C7^), ^V8^ (^C8^), ^V9^ (^C9^).',
                'nl2': 'For your {verb}, the available {P5}s are ^V7^, ^V8^, and ^V9^, with costs ^C7^, ^C8^, and ^C9^.',
                'nl3': 'You will find {P5}s such as ^V7^ (cost: ^C7^), ^V8^ (cost: ^C8^), and ^V9^ (cost: ^C9^) available for your {verb}.',
                'nl4': 'Among the choices for {P5}s in your {verb} are ^V7^, ^V8^, and ^V9^, each with a price tag of ^C7^, ^C8^, and ^C9^.',
                'nl5': 'There exist several {P5} options for your {verb}: ^V7^ for ^C7^, ^V8^ for ^C8^, and ^V9^ for ^C9^.',
                'nl6': 'The models ^V7^, ^V8^, and ^V9^ are all available {P5}s for your {verb}, costing ^C7^, ^C8^, and ^C9^ respectively.',
                'nl7': 'In the context of your {verb}, the {P5}s ^V7^, ^V8^, and ^V9^ are present, with associated costs of ^C7^, ^C8^, and ^C9^.',
                'nl8': 'For assembling your {verb}, you will encounter {P5} options including ^V7^ (cost: ^C7^), ^V8^ (cost: ^C8^), and ^V9^ (cost: ^C9^).',
                'nl9': 'The set of {P5}s for your {verb} consists of ^V7^, ^V8^, and ^V9^, each priced at ^C7^, ^C8^, and ^C9^.',
                'nl10': 'When considering your {verb}, the {P5} components available are ^V7^, ^V8^, and ^V9^, with respective costs of ^C7^, ^C8^, and ^C9^.'
            }
        )
        mobo_choice = p.add_line(
            '1 {{ {P6}(M) : {P5}(M, _) }} 1.'.format(**theme),
            {
                'simple': 'Pick only one {P5}.'.format(**theme),
                'simple2': 'Only one {P5} can be selected for your {verb}.'.format(**theme),
                'simple3': 'Exactly one {P5} must be chosen for your {verb}.'.format(**theme)
            },
            {
                'nl1': 'Pick just one {P5} from ^V7^, ^V8^, or ^V9^ for your {verb}.',
                'nl2': 'Only one {P5} can be chosen: ^V7^, ^V8^, or ^V9^.',
                'nl3': 'You must select exactly one {P5} for your {verb} from ^V7^, ^V8^, ^V9^.',
                'nl4': 'For your {verb}, only a single {P5} is allowed. Choose from ^V7^, ^V8^, or ^V9^.',
                'nl5': 'Make sure you do not pick more than one {P5} for your {verb}. The options are ^V7^, ^V8^, and ^V9^.',
                'nl6': 'Your {verb} requires you to choose only one {P5}. Select from ^V7^, ^V8^, or ^V9^.',
                'nl7': 'Selecting more than one {P5} is not permitted for your {verb}. Choose either ^V7^, ^V8^, or ^V9^.',
                'nl8': 'You are only allowed to select one {P5} for your {verb}. The available choices are ^V7^, ^V8^, and ^V9^.',
                'nl9': 'Be sure to pick just one {P5} for your {verb}. Multiple selections from ^V7^, ^V8^, ^V9^ will result in an error.',
                'nl10': 'Exactly one {P5} must be chosen for your {verb}. Double-check your selection before proceeding.'
            }
        )
        p.add_group(
            [mobo, mobo_choice],
            {
                'nl1/2': 'There are {P5} options for your {verb}: ^V7^ (^C7^), ^V8^ (^C8^), and ^V9^ (^C9^). You must select exactly one.',
                'nl2/2': 'For your {verb}, you can choose one {P5} from ^V7^, ^V8^, or ^V9^. Each has a price: ^V7^ is ^C7^, ^V8^ is ^C8^, and ^V9^ is ^C9^, and only one can be selected.',
                'nl3/2': 'You need to select a {P5} for your {verb}. The available options are ^V7^ (cost: ^C7^), ^V8^ (cost: ^C8^), and ^V9^ (cost: ^C9^). Only one {P5} is allowed.',
                'nl4/2': 'Among the choices for {P5}s in your {verb} are ^V7^, ^V8^, and ^V9^, each with a price tag of ^C7^, ^C8^, and ^C9^. You must pick exactly one.',
                'nl5/2': 'There exist several {P5} options for your {verb}: ^V7^ for ^C7^, ^V8^ for ^C8^, and ^V9^ for ^C9^. Only one can be chosen.',
                'nl6/2': 'The models ^V7^, ^V8^, and ^V9^ are all available {P5}s for your {verb}, costing ^C7^, ^C8^, and ^C9^ respectively. Select just one.',
                'nl7/2': 'For assembling your {verb}, you will encounter {P5} options including ^V7^ (cost: ^C7^), ^V8^ (cost: ^C8^), and ^V9^ (cost: ^C9^). Only one {P5} is permitted.',
                'nl8/2': 'The set of {P5}s for your {verb} consists of ^V7^, ^V8^, and ^V9^, each priced at ^C7^, ^C8^, and ^C9^. You are required to select exactly one.',
                'nl9/2': 'When considering your {verb}, the {P5} components available are ^V7^, ^V8^, and ^V9^, with respective costs of ^C7^, ^C8^, and ^C9^. Only one {P5} can be chosen.',
                'nl10/2': 'For your {verb}, review the available {P5}s: ^V7^ (cost: ^C7^), ^V8^ (cost: ^C8^), and ^V9^ (cost: ^C9^). Make sure to select exactly one option for your build.'
            }
        )

        # PSU group
        psu = p.add_line(
            '{P7}("^V10^", ^C10^; "^V11^", ^C11^; "^V12^", ^C12^).'.format(**theme),
            {
                'simple': 'Available {P7}s: ^V10^ (^C10^), ^V11^ (^C11^), ^V12^ (^C12^).'.format(**theme),
                'simple2': 'Select {P7} from ^V10^, ^V11^, ^V12^, with costs: ^V10^ = ^C10^, ^V11^ = ^C11^, ^V12^ = ^C12^.'.format(**theme),
                'simple3': 'Pick from these {P7}s for your {verb}: ^V10^ (^C10^), ^V11^ (^C11^), or ^V12^ (^C12^).'.format(**theme)
            },
            {
                'nl1': 'There are {P7} options: ^V10^ (^C10^), ^V11^ (^C11^), ^V12^ (^C12^).',
                'nl2': 'For your {verb}, the available {P7}s are ^V10^, ^V11^, and ^V12^, with costs ^C10^, ^C11^, and ^C12^.',
                'nl3': 'You will find {P7}s such as ^V10^ (cost: ^C10^), ^V11^ (cost: ^C11^), and ^V12^ (cost: ^C12^) available for your {verb}.',
                'nl4': 'Among the choices for {P7}s in your {verb} are ^V10^, ^V11^, and ^V12^, each with a price tag of ^C10^, ^C11^, and ^C12^.',
                'nl5': 'There exist several {P7} options for your {verb}: ^V10^ for ^C10^, ^V11^ for ^C11^, and ^V12^ for ^C12^.',
                'nl6': 'The models ^V10^, ^V11^, and ^V12^ are all available {P7}s for your {verb}, costing ^C10^, ^C11^, and ^C12^ respectively.',
                'nl7': 'In the context of your {verb}, the {P7}s ^V10^, ^V11^, and ^V12^ are present, with associated costs of ^C10^, ^C11^, and ^C12^.',
                'nl8': 'For assembling your {verb}, you will encounter {P7} options including ^V10^ (cost: ^C10^), ^V11^ (cost: ^C11^), and ^V12^ (cost: ^C12^).',
                'nl9': 'The set of {P7}s for your {verb} consists of ^V10^, ^V11^, and ^V12^, each priced at ^C10^, ^C11^, and ^C12^.',
                'nl10': 'When considering your {verb}, the {P7} components available are ^V10^, ^V11^, and ^V12^, with respective costs of ^C10^, ^C11^, and ^C12^.'
            }
        )
        psu_choice = p.add_line(
            '1 {{ {P8}(P) : {P7}(P, _) }} 1.'.format(**theme),
            {
                'simple': 'Pick only one {P7}.'.format(**theme),
                'simple2': 'Only one {P7} can be selected for your {verb}.'.format(**theme),
                'simple3': 'Exactly one {P7} must be chosen for your {verb}.'.format(**theme)
            },
            {
                'nl1': 'Pick just one {P7} from ^V10^, ^V11^, or ^V12^ for your {verb}.',
                'nl2': 'Only one {P7} can be chosen: ^V10^, ^V11^, or ^V12^.',
                'nl3': 'You must select exactly one {P7} for your {verb} from ^V10^, ^V11^, ^V12^.',
                'nl4': 'For your {verb}, only a single {P7} is allowed. Choose from ^V10^, ^V11^, or ^V12^.',
                'nl5': 'Make sure you do not pick more than one {P7} for your {verb}. The options are ^V10^, ^V11^, and ^V12^.',
                'nl6': 'Your {verb} requires you to choose only one {P7}. Select from ^V10^, ^V11^, or ^V12^.',
                'nl7': 'Selecting more than one {P7} is not permitted for your {verb}. Choose either ^V10^, ^V11^, or ^V12^.',
                'nl8': 'You are only allowed to select one {P7} for your {verb}. The available choices are ^V10^, ^V11^, and ^V12^.',
                'nl9': 'Be sure to pick just one {P7} for your {verb}. Multiple selections from ^V10^, ^V11^, ^V12^ will result in an error.',
                'nl10': 'Exactly one {P7} must be chosen for your {verb}. Double-check your selection before proceeding.'
            }
        )
        p.add_group(
            [psu, psu_choice],
            {
                'nl1/2': 'There are {P7} options for your {verb}: ^V10^ (^C10^), ^V11^ (^C11^), and ^V12^ (^C12^). You must select exactly one.',
                'nl2/2': 'For your {verb}, you can choose one {P7} from ^V10^, ^V11^, or ^V12^. Each has a price: ^V10^ is ^C10^, ^V11^ is ^C11^, and ^V12^ is ^C12^, and only one can be selected.',
                'nl3/2': 'You need to select a {P7} for your {verb}. The available options are ^V10^ (cost: ^C10^), ^V11^ (cost: ^C11^), and ^V12^ (cost: ^C12^). Only one {P7} is allowed.',
                'nl4/2': 'Among the choices for {P7}s in your {verb} are ^V10^, ^V11^, and ^V12^, each with a price tag of ^C10^, ^C11^, and ^C12^. You must pick exactly one.',
                'nl5/2': 'There exist several {P7} options for your {verb}: ^V10^ for ^C10^, ^V11^ for ^C11^, and ^V12^ for ^C12^. Only one can be chosen.',
                'nl6/2': 'The models ^V10^, ^V11^, and ^V12^ are all available {P7}s for your {verb}, costing ^C10^, ^C11^, and ^C12^ respectively. Select just one.',
                'nl7/2': 'For assembling your {verb}, you will encounter {P7} options including ^V10^ (cost: ^C10^), ^V11^ (cost: ^C11^), and ^V12^ (cost: ^C12^). Only one {P7} is permitted.',
                'nl8/2': 'The set of {P7}s for your {verb} consists of ^V10^, ^V11^, and ^V12^, each priced at ^C10^, ^C11^, and ^C12^. You are required to select exactly one.',
                'nl9/2': 'When considering your {verb}, the {P7} components available are ^V10^, ^V11^, and ^V12^, with respective costs of ^C10^, ^C11^, and ^C12^. Only one {P7} can be chosen.',
                'nl10/2': 'For your {verb}, review the available {P7}s: ^V10^ (cost: ^C10^), ^V11^ (cost: ^C11^), and ^V12^ (cost: ^C12^). Make sure to select exactly one option for your build.'
            }
        )

        # Constraints group
        high_power = p.add_line(
            '{P9}("^V5^"; "^V6^").'.format(**theme),
            {
                'simple': '{P9}: ^V5^ and ^V6^ are {P9} {P3}s.'.format(**theme),
                'simple2': 'The {P3}s ^V5^ and ^V6^ are classified as {P9}.'.format(**theme),
                'simple3': '{P9} {P3}s include ^V5^ and ^V6^.'.format(**theme)
            },
            {
                'nl1': '^V5^ and ^V6^ are {P9} {P3}s.',
                'nl2': 'The {P3}s ^V5^ and ^V6^ are considered {P9} options.',
                'nl3': 'Among the available {P3}s, ^V5^ and ^V6^ are categorized as {P9}.',
                'nl4': 'For your {verb}, the {P3}s ^V5^ and ^V6^ are identified as {P9} components.',
                'nl5': 'The {P3} models ^V5^ and ^V6^ are recognized for their {P9} consumption.',
                'nl6': 'Within the set of {P3}s, ^V5^ and ^V6^ stand out as {P9} choices.',
                'nl7': 'If you are considering power usage, note that ^V5^ and ^V6^ {P3}s are {P9}.',
                'nl8': 'In the context of your {verb}, the {P3}s ^V5^ and ^V6^ are known to require more power and are thus considered {P9}.',
                'nl9': 'The {P3} options ^V5^ and ^V6^ are classified as {P9}, meaning they consume more electricity compared to other {P3}s.',
                'nl10': 'When assembling your {verb}, keep in mind that the {P3}s ^V5^ and ^V6^ are {P9} components, which may impact your overall system requirements and energy consumption.'
            }
        )
        
        constraint1 = p.add_line(
            ':- {P4}(G), {P9}(G), {P8}("^V10^").'.format(**theme),
            {
                'simple': '{P9} {P3}s require {P7} ∈ ^V11^, ^V12^.'.format(**theme),
                'simple2': 'If a {P9} {P3} is selected, the {P7} must be ^V11^ or ^V12^.'.format(**theme),
                'simple3': 'Selecting a {P9} {P3} means you must use a ^V11^ or ^V12^ {P7}.'.format(**theme)
            },
            {
                'nl1': 'If you pick a {P9} {P3}, you must use a ^V11^ or ^V12^ {P7}.'.format(**theme),
                'nl2': 'Selecting a {P9} {P3} requires your {verb} to include a {P7} of type ^V11^ or ^V12^.'.format(**theme),
                'nl3': 'Whenever a {P9} {P3} is chosen, only a ^V11^ or ^V12^ {P7} is compatible with your build.'.format(**theme),
                'nl4': 'For your {verb}, if you select a {P9} {P3}, you are restricted to using a {P7} that is either ^V11^ or ^V12^.'.format(**theme),
                'nl5': 'A {P9} {P3} such as ^V5^ or ^V6^ can only be used if your {verb} includes a {P7} of type ^V11^ or ^V12^.'.format(**theme),
                'nl6': 'Your {verb} cannot include a {P9} {P3} unless the {P7} is ^V11^ or ^V12^, ensuring compatibility and safety.'.format(**theme),
                'nl7': 'If you want to use a {P9} {P3} (like ^V5^ or ^V6^), your {verb} must feature a {P7} that is either ^V11^ or ^V12^, as other types are not sufficient.'.format(**theme),
                'nl8': 'In the context of your {verb}, selecting a {P9} {P3} mandates that the {P7} you use is either ^V11^ or ^V12^, due to power requirements.'.format(**theme),
                'nl9': 'To ensure your {verb} functions correctly, any {P9} {P3} (such as ^V5^ or ^V6^) must be paired with a {P7} of type ^V11^ or ^V12^, as lower-rated options are not allowed.'.format(**theme),
                'nl10': 'When assembling your {verb}, remember that choosing a {P9} {P3} (like ^V5^ or ^V6^) strictly requires the use of a {P7} that is either ^V11^ or ^V12^, to meet the necessary power demands and avoid incompatibility.'.format(**theme)
            }
        )
        constraint2 = p.add_line(
            ':- {P2}("^V3^"), {P6}(M), M != "^V9^".'.format(**theme),
            {
                'simple': '^V3^ requires {P5} ^V9^.',
                'simple2': 'If ^V3^ is selected as {P1}, the {P5} must be ^V9^.',
                'simple3': 'Selecting ^V3^ as your {P1} means you must use {P5} ^V9^.'
            },
            {
                'nl1': 'The ^V3^ {P1} only works with the ^V9^ {P5}.'.format(**theme),
                'nl2': 'If you select ^V3^ as your {P1}, you must use ^V9^ as your {P5}.'.format(**theme),
                'nl3': 'Choosing ^V3^ for your {P1} requires that your {verb} includes the ^V9^ {P5}.'.format(**theme),
                'nl4': 'For your {verb}, if you pick ^V3^ as your {P1}, only the ^V9^ {P5} is compatible.'.format(**theme),
                'nl5': 'Your {verb} cannot include ^V3^ as the {P1} unless the {P5} is ^V9^, as other options are not supported.'.format(**theme),
                'nl6': 'Selecting ^V3^ as your {P1} restricts your {verb} to using the ^V9^ {P5} for compatibility.'.format(**theme),
                'nl7': 'If you want to use ^V3^ as your {P1}, your {verb} must feature the ^V9^ {P5}, since other motherboards are incompatible.'.format(**theme),
                'nl8': 'In the context of your {verb}, choosing ^V3^ as the {P1} mandates the use of the ^V9^ {P5}.'.format(**theme),
                'nl9': 'To ensure your {verb} works, selecting ^V3^ as the {P1} means you must pair it with the ^V9^ {P5}.'.format(**theme),
                'nl10': 'When assembling your {verb}, remember that if you choose ^V3^ as your {P1}, you are required to use the ^V9^ {P5} for proper compatibility.'.format(**theme)
            }
        )
        constraint3 = p.add_line(
            ':- {P2}("^V1^"), {P6}(M), M != "^V7^".'.format(**theme),
            {
                'simple': '^V1^ requires {P5} ^V7^.',
                'simple2': 'If ^V1^ is selected as {P1}, the {P5} must be ^V7^.',
                'simple3': 'Selecting ^V1^ as your {P1} means you must use {P5} ^V7^.'
            },
            {
                'nl1': 'The ^V1^ {P1} only works with the ^V7^ {P5}.'.format(**theme),
                'nl2': 'If you select ^V1^ as your {P1}, you must use ^V7^ as your {P5}.'.format(**theme),
                'nl3': 'Choosing ^V1^ for your {P1} requires that your {verb} includes the ^V7^ {P5}.'.format(**theme),
                'nl4': 'For your {verb}, if you pick ^V1^ as your {P1}, only the ^V7^ {P5} is compatible.'.format(**theme),
                'nl5': 'Your {verb} cannot include ^V1^ as the {P1} unless the {P5} is ^V7^, as other options are not supported.'.format(**theme),
                'nl6': 'Selecting ^V1^ as your {P1} restricts your {verb} to using the ^V7^ {P5} for compatibility.'.format(**theme),
                'nl7': 'If you want to use ^V1^ as your {P1}, your {verb} must feature the ^V7^ {P5}, since other motherboards are incompatible.'.format(**theme),
                'nl8': 'In the context of your {verb}, choosing ^V1^ as the {P1} mandates the use of the ^V7^ {P5}.'.format(**theme),
                'nl9': 'To ensure your {verb} works, selecting ^V1^ as the {P1} means you must pair it with the ^V7^ {P5}.'.format(**theme),
                'nl10': 'When assembling your {verb}, remember that if you choose ^V1^ as your {P1}, you are required to use the ^V7^ {P5} for proper compatibility.'.format(**theme)
            }
        )
        constraint4 = p.add_line(
            ':- {P2}("^V2^"), {P6}("^V7^").'.format(**theme),
            {
                'simple': '^V2^ is incompatible with {P5} ^V7^.',
                'simple2': 'If ^V2^ is selected as {P1}, {P5} ^V7^ cannot be used.',
                'simple3': 'Selecting ^V2^ as your {P1} means you cannot use {P5} ^V7^.'
            },
            {
                'nl1': 'The ^V2^ {P1} cannot be paired with the ^V7^ {P5}.'.format(**theme),
                'nl2': 'If you select ^V2^ as your {P1}, you cannot use ^V7^ as your {P5}.'.format(**theme),
                'nl3': 'Choosing ^V2^ for your {P1} means the ^V7^ {P5} is not compatible with your {verb}.'.format(**theme),
                'nl4': 'For your {verb}, if you pick ^V2^ as your {P1}, the ^V7^ {P5} cannot be included.'.format(**theme),
                'nl5': 'Your {verb} cannot include both ^V2^ as the {P1} and ^V7^ as the {P5}, as they are incompatible.'.format(**theme),
                'nl6': 'Selecting ^V2^ as your {P1} restricts your {verb} from using the ^V7^ {P5}.'.format(**theme),
                'nl7': 'If you want to use ^V2^ as your {P1}, your {verb} must not feature the ^V7^ {P5}, since they do not work together.'.format(**theme),
                'nl8': 'In the context of your {verb}, choosing ^V2^ as the {P1} excludes the use of the ^V7^ {P5}.'.format(**theme),
                'nl9': 'To ensure your {verb} works, selecting ^V2^ as the {P1} means you cannot pair it with the ^V7^ {P5}.'.format(**theme),
                'nl10': 'When assembling your {verb}, remember that if you choose ^V2^ as your {P1}, you are not allowed to use the ^V7^ {P5} due to incompatibility.'.format(**theme)
            }
        )
        constraint5 = p.add_line(
            ':- {P4}("^V6^"), {P2}(C), C != "^V3^".'.format(**theme),
            {
                'simple': '^V6^ requires ^V3^ {P1}.',
                'simple2': 'If ^V6^ is selected as {P3}, the {P1} must be ^V3^.',
                'simple3': 'Selecting ^V6^ as your {P3} means you must use {P1} ^V3^.'
            },
            {
                'nl1': 'The ^V6^ {P3} requires the ^V3^ {P1}.'.format(**theme),
                'nl2': 'If you select ^V6^ as your {P3}, you must use ^V3^ as your {P1}.'.format(**theme),
                'nl3': 'Choosing ^V6^ for your {P3} requires that your {verb} includes the ^V3^ {P1}.'.format(**theme),
                'nl4': 'For your {verb}, if you pick ^V6^ as your {P3}, only the ^V3^ {P1} is compatible.'.format(**theme),
                'nl5': 'Your {verb} cannot include ^V6^ as the {P3} unless the {P1} is ^V3^, as other options are not supported.'.format(**theme),
                'nl6': 'Selecting ^V6^ as your {P3} restricts your {verb} to using the ^V3^ {P1} for compatibility.'.format(**theme),
                'nl7': 'If you want to use ^V6^ as your {P3}, your {verb} must feature the ^V3^ {P1}, since other CPUs are incompatible.'.format(**theme),
                'nl8': 'In the context of your {verb}, choosing ^V6^ as the {P3} mandates the use of the ^V3^ {P1}.'.format(**theme),
                'nl9': 'To ensure your {verb} works, selecting ^V6^ as the {P3} means you must pair it with the ^V3^ {P1}.'.format(**theme),
                'nl10': 'When assembling your {verb}, remember that if you choose ^V6^ as your {P3}, you are required to use the ^V3^ {P1} for proper compatibility.'.format(**theme)
            }
        )
        constraint6 = p.add_line(
            ':- {P4}("^V6^"), {P6}("^V8^").'.format(**theme),
            {
                'simple': '^V6^ is incompatible with {P5} ^V8^.',
                'simple2': 'If ^V6^ is selected as {P3}, {P5} ^V8^ cannot be used.',
                'simple3': 'Selecting ^V6^ as your {P3} means you cannot use {P5} ^V8^.'
            },
            {
                'nl1': 'The ^V6^ {P3} cannot be used with the ^V8^ {P5}.'.format(**theme),
                'nl2': 'If you select ^V6^ as your {P3}, you cannot use ^V8^ as your {P5}.'.format(**theme),
                'nl3': 'Choosing ^V6^ for your {P3} means the ^V8^ {P5} is not compatible with your {verb}.'.format(**theme),
                'nl4': 'For your {verb}, if you pick ^V6^ as your {P3}, the ^V8^ {P5} cannot be included.'.format(**theme),
                'nl5': 'Your {verb} cannot include both ^V6^ as the {P3} and ^V8^ as the {P5}, as they are incompatible.'.format(**theme),
                'nl6': 'Selecting ^V6^ as your {P3} restricts your {verb} from using the ^V8^ {P5}.'.format(**theme),
                'nl7': 'If you want to use ^V6^ as your {P3}, your {verb} must not feature the ^V8^ {P5}, since they do not work together.'.format(**theme),
                'nl8': 'In the context of your {verb}, choosing ^V6^ as the {P3} excludes the use of the ^V8^ {P5}.'.format(**theme),
                'nl9': 'To ensure your {verb} works, selecting ^V6^ as the {P3} means you cannot pair it with the ^V8^ {P5}.'.format(**theme),
                'nl10': 'When assembling your {verb}, remember that if you choose ^V6^ as your {P3}, you are not allowed to use the ^V8^ {P5} due to incompatibility.'.format(**theme)
            }
        )
        
        p.add_group(
            [high_power, constraint1, constraint2, constraint3, constraint4, constraint5, constraint6],
            {
                'nl1/7': (
                    'Some compatibility rules apply: '
                    '^V5^ and ^V6^ are {P9} {P3}s and need a ^V11^ or ^V12^ {P7}. '
                    '^V3^ {P1} only works with ^V9^ {P5}. '
                    '^V1^ {P1} only works with ^V7^ {P5}. '
                    '^V2^ {P1} cannot be paired with ^V7^ {P5}. '
                    '^V6^ {P3} requires the ^V3^ {P1}. '
                    '^V6^ {P3} cannot be used with ^V8^ {P5}.'
                ).format(**theme),
                'nl2/7': (
                    'There are several compatibility constraints: '
                    'If you select a {P9} {P3} (^V5^ or ^V6^), you must use a ^V11^ or ^V12^ {P7}. '
                    'The ^V3^ {P1} is only compatible with the ^V9^ {P5}, and ^V1^ {P1} only with ^V7^ {P5}. '
                    'The ^V2^ {P1} cannot be used with ^V7^ {P5}. '
                    'If you choose ^V6^ as your {P3}, you must also select ^V3^ as your {P1}, and you cannot use ^V8^ as your {P5}.'
                ).format(**theme),
                'nl3/7': (
                    'Pay attention to these compatibility rules: '
                    '{P9} {P3}s (^V5^ and ^V6^) require a {P7} of type ^V11^ or ^V12^. '
                    'The ^V3^ {P1} only works with the ^V9^ {P5}, while ^V1^ {P1} only works with ^V7^ {P5}. '
                    'You cannot pair ^V2^ {P1} with ^V7^ {P5}. '
                    'Selecting ^V6^ as your {P3} means you must use ^V3^ as your {P1} and cannot use ^V8^ as your {P5}.'
                ).format(**theme),
                'nl4/7': (
                    'Compatibility requirements: '
                    'If you choose a {P9} {P3} (either ^V5^ or ^V6^), your {verb} must include a {P7} of type ^V11^ or ^V12^. '
                    'The ^V3^ {P1} is only compatible with the ^V9^ {P5}, and ^V1^ {P1} is only compatible with the ^V7^ {P5}. '
                    'The ^V2^ {P1} cannot be used with the ^V7^ {P5}. '
                    'If you select ^V6^ as your {P3}, you must also select ^V3^ as your {P1}, and you cannot use ^V8^ as your {P5}.'
                ).format(**theme),
                'nl5/7': (
                    'When assembling your {verb}, keep in mind: '
                    '{P9} {P3}s (^V5^, ^V6^) require a {P7} of type ^V11^ or ^V12^. '
                    'The ^V3^ {P1} only works with the ^V9^ {P5}, and ^V1^ {P1} only with ^V7^ {P5}. '
                    'You cannot use ^V2^ {P1} with ^V7^ {P5}. '
                    'If you select ^V6^ as your {P3}, you must also select ^V3^ as your {P1}, and you cannot use ^V8^ as your {P5}.'
                ).format(**theme),
                'nl6/7': (
                    'For your {verb}, observe these compatibility rules: '
                    'Selecting a {P9} {P3} (either ^V5^ or ^V6^) means you must use a {P7} of type ^V11^ or ^V12^. '
                    'The ^V3^ {P1} is only compatible with the ^V9^ {P5}, and ^V1^ {P1} is only compatible with the ^V7^ {P5}. '
                    'The ^V2^ {P1} cannot be used with the ^V7^ {P5}. '
                    'If you select ^V6^ as your {P3}, you must also select ^V3^ as your {P1}, and you cannot use ^V8^ as your {P5}.'
                ).format(**theme),
                'nl7/7': (
                    'The following compatibility rules must be followed for your {verb}: '
                    'If you select a {P9} {P3} (such as ^V5^ or ^V6^), you must use a {P7} of type ^V11^ or ^V12^ to meet power requirements. '
                    'The ^V3^ {P1} is only compatible with the ^V9^ {P5}, and ^V1^ {P1} is only compatible with the ^V7^ {P5}. '
                    'The ^V2^ {P1} cannot be paired with the ^V7^ {P5}. '
                    'If you select ^V6^ as your {P3}, you must also select ^V3^ as your {P1}, and you cannot use ^V8^ as your {P5}. '
                    'These rules ensure your build is compatible and functional.'
                ).format(**theme)
            }
        )

        # Cost/minimize group
        cost = p.add_line(
            'total_cost(Cost) :- {P2}(C), {P1}(C, CCost), {P4}(G), {P3}(G, GCost), {P6}(M), {P5}(M, MCost), {P8}(P), {P7}(P, PCost), Cost = CCost + GCost + MCost + PCost.'.format(**theme),
            {
                'simple': 'Total cost is the sum of all selected component costs.',
                'simple2': 'Add up the costs of your chosen {P1}, {P3}, {P5}, and {P7} to get the total cost.'.format(**theme),
                'simple3': 'The total cost equals the sum of the prices for your selected {P1}, {P3}, {P5}, and {P7}.'.format(**theme)
            },
            {
                'nl1': 'The total cost is calculated by adding up the prices of your selected {P1}, {P3}, {P5}, and {P7}.'.format(**theme),
                'nl2': 'To find the total cost, sum the prices of the {P1}, {P3}, {P5}, and {P7} you have chosen for your {verb}.'.format(**theme),
                'nl3': 'Your {verb} will have a total cost equal to the combined prices of the selected {P1}, {P3}, {P5}, and {P7}.'.format(**theme),
                'nl4': 'The total cost for your {verb} is the sum of the costs of the {P1}, {P3}, {P5}, and {P7} you select.'.format(**theme),
                'nl5': 'Add together the prices of your chosen {P1}, {P3}, {P5}, and {P7} to determine the total cost for your {verb}.'.format(**theme),
                'nl6': 'For your {verb}, the total cost is obtained by summing the costs of the selected {P1}, {P3}, {P5}, and {P7}.'.format(**theme),
                'nl7': 'The total price of your {verb} is the sum of the costs of each selected component: {P1}, {P3}, {P5}, and {P7}.'.format(**theme),
                'nl8': 'To calculate the total cost for your {verb}, add up the prices of the selected {P1}, {P3}, {P5}, and {P7}.'.format(**theme),
                'nl9': 'Your {verb} will cost the total of the prices for your chosen {P1}, {P3}, {P5}, and {P7}.'.format(**theme),
                'nl10': 'When assembling your {verb}, the total cost is determined by adding together the prices of your selected {P1}, {P3}, {P5}, and {P7}. Make sure to consider each component\'s price to get the final sum.'.format(**theme)
            }
        )
        minimize = p.add_line(
            '#minimize { C : total_cost(C) }.',
            {
                'simple': 'Minimize total cost.',
                'simple2': 'Try to keep the total cost as low as possible.',
                'simple3': 'Your objective is to minimize the total cost of your {verb}.'.format(**theme)
            },
            {
                'nl1': 'Your goal is to minimize the total cost of your {verb}.'.format(**theme),
                'nl2': 'Aim to keep the total cost of your {verb} as low as possible.'.format(**theme),
                'nl3': 'Try to minimize the sum of the prices for your selected {P1}, {P3}, {P5}, and {P7}.'.format(**theme),
                'nl4': 'The objective is to assemble your {verb} at the lowest possible total cost.'.format(**theme),
                'nl5': 'You should aim to select components for your {verb} that result in the smallest total cost.'.format(**theme),
                'nl6': 'When choosing parts for your {verb}, try to minimize the overall cost by selecting less expensive options.'.format(**theme),
                'nl7': 'The best {verb} is one that meets your needs while also minimizing the total cost of {P1}, {P3}, {P5}, and {P7}.'.format(**theme),
                'nl8': 'To optimize your {verb}, focus on minimizing the total cost by carefully selecting each component.'.format(**theme),
                'nl9': 'Your {verb} should be assembled with the goal of achieving the lowest total cost possible for all selected components.'.format(**theme),
                'nl10': 'When assembling your {verb}, always consider the total cost and try to minimize it by choosing the most cost-effective {P1}, {P3}, {P5}, and {P7} available.'.format(**theme)
            }
        )
        p.add_group(
        [cost, minimize],
        {
            'nl1/2': 'The total cost is the sum of your selected {P1}, {P3}, {P5}, and {P7}. Minimize this cost for your {verb}.'.format(**theme),
            'nl2/2': 'Add up the prices of your chosen {P1}, {P3}, {P5}, and {P7} to get the total cost, and aim to keep this as low as possible for your {verb}.'.format(**theme),
            'nl3/2': 'For your {verb}, the total cost is calculated by summing the prices of the selected {P1}, {P3}, {P5}, and {P7}. Your objective is to minimize this total.'.format(**theme),
            'nl4/2': 'The total cost for your {verb} is determined by adding together the costs of your selected {P1}, {P3}, {P5}, and {P7}. Try to minimize this sum when choosing your components.'.format(**theme),
            'nl5/2': 'When assembling your {verb}, the total cost is the sum of the prices for your selected {P1}, {P3}, {P5}, and {P7}. Select components to keep this total as low as possible.'.format(**theme),
            'nl6/2': 'To optimize your {verb}, calculate the total cost by adding up the prices of your chosen {P1}, {P3}, {P5}, and {P7}, and aim to minimize this value.'.format(**theme),
            'nl7/2': 'The goal for your {verb} is to select {P1}, {P3}, {P5}, and {P7} such that the total cost, which is the sum of their prices, is minimized.'.format(**theme),
            'nl8/2': 'For your {verb}, the total cost is the combined price of your selected {P1}, {P3}, {P5}, and {P7}. Make your selections to achieve the lowest possible total cost.'.format(**theme),
            'nl9/2': 'When building your {verb}, remember that the total cost is the sum of the prices of your {P1}, {P3}, {P5}, and {P7}. Your aim should be to minimize this sum.'.format(**theme),
            'nl10/2': 'As you assemble your {verb}, the total cost is calculated by adding the prices of your selected {P1}, {P3}, {P5}, and {P7}. Carefully choose each component to ensure the overall cost is as low as possible.'.format(**theme)
        }
    )