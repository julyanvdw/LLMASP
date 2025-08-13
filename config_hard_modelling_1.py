from AspPy2 import ASPProgram, DataGenerator
import random
import json

theme_sets = [
    # 1. Computer Workstation (keep this one)
    {
        'P1': 'cpu',
        'P2': 'selected_cpu',
        'P3': 'gpu',
        'P4': 'selected_gpu',
        'P5': 'storage',
        'P6': 'selected_storage',
        'P7': 'cost',
        'P8': 'performance',
        'P9': 'selected',
        'P10': 'max_cost',
        'P11': 'max_performance',
        'P12': 'top_cpu',
        'P13': 'top_gpu',
        'P14': 'top_storage',
        'theme': 'High-End Workstation',
        'verb': 'configuration',
        'variations': {
            'V1': ['X9', 'XeonGold'],
            'V1b': ['ZetaCore', 'Threadripper'],
            'V1c': ['Alpha8'],
            'V2': ['QuasarRTX'],
            'V2b': ['NovaX'],
            'V2c': ['GammaGTX'],
            'V3': ['UltraSSD'],
            'V3b': ['MegaHDD'],
            'V3c': ['FusionDrive'],
            'C1': ['300'],
            'C1b': ['500'],
            'C1c': ['450'],
            'C2': ['700'],
            'C2b': ['600'],
            'C2c': ['450'],
            'C3': ['250'],
            'C3b': ['200'],
            'C3c': ['300'],
            'P1_perf': ['95'],
            'P1b_perf': ['120'],
            'P1c_perf': ['110'],
            'P2_perf': ['130'],
            'P2b_perf': ['125'],
            'P2c_perf': ['90'],
            'P3_perf': ['100'],
            'P3b_perf': ['60'],
            'P3c_perf': ['95']
        }
    },
    # 2. Aquarium Ecosystem
    {
        'P1': 'fish',
        'P2': 'selected_fish',
        'P3': 'plant',
        'P4': 'selected_plant',
        'P5': 'filter',
        'P6': 'selected_filter',
        'P7': 'cost',
        'P8': 'bio_score',
        'P9': 'selected',
        'P10': 'max_cost',
        'P11': 'max_bio_score',
        'P12': 'top_fish',
        'P13': 'top_plant',
        'P14': 'top_filter',
        'theme': 'Aquarium Ecosystem',
        'verb': 'setup',
        'variations': {
            'V1': ['NeonTetra'],
            'V1b': ['Betta'],
            'V1c': ['Guppy'],
            'V2': ['JavaFern'],
            'V2b': ['Anubias'],
            'V2c': ['AmazonSword'],
            'V3': ['SpongeFilter'],
            'V3b': ['CanisterFilter'],
            'V3c': ['HangOnBack'],
            'C1': ['5'],
            'C1b': ['8'],
            'C1c': ['6'],
            'C2': ['3'],
            'C2b': ['4'],
            'C2c': ['5'],
            'C3': ['20'],
            'C3b': ['50'],
            'C3c': ['30'],
            'P1_perf': ['7'],
            'P1b_perf': ['8'],
            'P1c_perf': ['6'],
            'P2_perf': ['5'],
            'P2b_perf': ['7'],
            'P2c_perf': ['6'],
            'P3_perf': ['8'],
            'P3b_perf': ['10'],
            'P3c_perf': ['9']
        }
    },
    # 3. Fantasy Adventurer Loadout
    {
        'P1': 'weapon',
        'P2': 'selected_weapon',
        'P3': 'armor',
        'P4': 'selected_armor',
        'P5': 'companion',
        'P6': 'selected_companion',
        'P7': 'cost',
        'P8': 'power',
        'P9': 'selected',
        'P10': 'max_cost',
        'P11': 'max_power',
        'P12': 'top_weapon',
        'P13': 'top_armor',
        'P14': 'top_companion',
        'theme': 'Adventurer Loadout',
        'verb': 'equip',
        'variations': {
            'V1': ['SwordOfLight'],
            'V1b': ['AxeOfStorms'],
            'V1c': ['ShadowDagger'],
            'V2': ['DragonScale'],
            'V2b': ['ElvenCloak'],
            'V2c': ['IronPlate'],
            'V3': ['Wolf'],
            'V3b': ['Falcon'],
            'V3c': ['Golem'],
            'C1': ['100'],
            'C1b': ['80'],
            'C1c': ['60'],
            'C2': ['90'],
            'C2b': ['70'],
            'C2c': ['50'],
            'C3': ['40'],
            'C3b': ['30'],
            'C3c': ['60'],
            'P1_perf': ['30'],
            'P1b_perf': ['28'],
            'P1c_perf': ['22'],
            'P2_perf': ['25'],
            'P2b_perf': ['20'],
            'P2c_perf': ['18'],
            'P3_perf': ['15'],
            'P3b_perf': ['12'],
            'P3c_perf': ['20']
        }
    },
    # 4. Urban Garden Design
    {
        'P1': 'tree',
        'P2': 'selected_tree',
        'P3': 'shrub',
        'P4': 'selected_shrub',
        'P5': 'flower',
        'P6': 'selected_flower',
        'P7': 'cost',
        'P8': 'eco_score',
        'P9': 'selected',
        'P10': 'max_cost',
        'P11': 'max_eco_score',
        'P12': 'top_tree',
        'P13': 'top_shrub',
        'P14': 'top_flower',
        'theme': 'Urban Garden',
        'verb': 'design',
        'variations': {
            'V1': ['Maple'],
            'V1b': ['Birch'],
            'V1c': ['Oak'],
            'V2': ['Boxwood'],
            'V2b': ['Azalea'],
            'V2c': ['Hydrangea'],
            'V3': ['Tulip'],
            'V3b': ['Rose'],
            'V3c': ['Daffodil'],
            'C1': ['120'],
            'C1b': ['100'],
            'C1c': ['90'],
            'C2': ['60'],
            'C2b': ['50'],
            'C2c': ['40'],
            'C3': ['30'],
            'C3b': ['25'],
            'C3c': ['20'],
            'P1_perf': ['15'],
            'P1b_perf': ['13'],
            'P1c_perf': ['12'],
            'P2_perf': ['8'],
            'P2b_perf': ['7'],
            'P2c_perf': ['6'],
            'P3_perf': ['5'],
            'P3b_perf': ['4'],
            'P3c_perf': ['3']
        }
    },
    # 5. Space Mission Module
    {
        'P1': 'habitat',
        'P2': 'selected_habitat',
        'P3': 'propulsion',
        'P4': 'selected_propulsion',
        'P5': 'science',
        'P6': 'selected_science',
        'P7': 'cost',
        'P8': 'mission_value',
        'P9': 'selected',
        'P10': 'max_cost',
        'P11': 'max_mission_value',
        'P12': 'top_habitat',
        'P13': 'top_propulsion',
        'P14': 'top_science',
        'theme': 'Space Mission',
        'verb': 'assemble',
        'variations': {
            'V1': ['LunarDome'],
            'V1b': ['MarsPod'],
            'V1c': ['AstroCabin'],
            'V2': ['IonDrive'],
            'V2b': ['FusionThruster'],
            'V2c': ['ChemicalRocket'],
            'V3': ['Spectrometer'],
            'V3b': ['Drill'],
            'V3c': ['Telescope'],
            'C1': ['1000'],
            'C1b': ['1200'],
            'C1c': ['900'],
            'C2': ['2000'],
            'C2b': ['2500'],
            'C2c': ['1800'],
            'C3': ['500'],
            'C3b': ['700'],
            'C3c': ['600'],
            'P1_perf': ['80'],
            'P1b_perf': ['85'],
            'P1c_perf': ['75'],
            'P2_perf': ['95'],
            'P2b_perf': ['100'],
            'P2c_perf': ['90'],
            'P3_perf': ['60'],
            'P3b_perf': ['65'],
            'P3c_perf': ['70']
        }
    }
]

def generate_programs(theme_sets):
    programs = []
    for theme in theme_sets:
        p = ASPProgram()

        # Components (all 3 options for each)
        cpu = p.add_line(
            '{P1}("^V1^"; "^V1b^"; "^V1c^").'.format(**theme),
            {
                'cnl1': '{P1}s are ^V1^, ^V1b^, ^V1c^.'.format(**theme),
                'cnl2': 'Available {P1} options for this {verb}: ^V1^, ^V1b^, ^V1c^.'.format(**theme),
                'cnl3': 'Select a {P1} for your {verb} from ^V1^, ^V1b^, or ^V1c^.'.format(**theme)
            },
            {
                'nl1': 'You can choose a {P1} for your {verb}. The available {P1}s are ^V1^, ^V1b^, and ^V1c^.'.format(**theme),
                'nl2': 'For this {verb}, the {P1} options are ^V1^, ^V1b^, and ^V1c^.'.format(**theme),
                'nl3': 'Select one {P1} from the following for your {verb}: ^V1^, ^V1b^, ^V1c^.'.format(**theme),
                'nl4': 'To complete your {verb}, you must include one {P1}. Choose from ^V1^, ^V1b^, or ^V1c^.'.format(**theme),
                'nl5': 'There are three {P1}s available for your {verb}: ^V1^, ^V1b^, and ^V1c^.'.format(**theme),
                'nl6': 'Your {verb} requires a {P1}. The choices are ^V1^, ^V1b^, and ^V1c^.'.format(**theme),
                'nl7': 'Among the {P1} options for this {verb}, you can select ^V1^, ^V1b^, or ^V1c^.'.format(**theme),
                'nl8': 'To proceed with your {verb}, pick one {P1} from ^V1^, ^V1b^, or ^V1c^.'.format(**theme),
                'nl9': 'For the {theme}, select a {P1} from these options: ^V1^, ^V1b^, ^V1c^.'.format(**theme),
                'nl10': 'In this {theme} {verb}, you are required to include {P1}. The available {P1}s are ^V1^, ^V1b^, and ^V1c^.'.format(**theme)
            }
        )
        gpu = p.add_line(
            '{P3}("^V2^"; "^V2b^"; "^V2c^").'.format(**theme),
            {
                'cnl1': '{P3}s are ^V2^, ^V2b^, ^V2c^.'.format(**theme),
                'cnl2': 'Available {P3} options for this {verb}: ^V2^, ^V2b^, ^V2c^.'.format(**theme),
                'cnl3': 'Select a {P3} for your {verb} from ^V2^, ^V2b^, or ^V2c^.'.format(**theme)
            },
            {
                'nl1': 'You can choose a {P3} for your {verb}. The available {P3}s are ^V2^, ^V2b^, and ^V2c^.'.format(**theme),
                'nl2': 'For this {verb}, the {P3} options are ^V2^, ^V2b^, and ^V2c^.'.format(**theme),
                'nl3': 'Select one {P3} from the following for your {verb}: ^V2^, ^V2b^, ^V2c^.'.format(**theme),
                'nl4': 'To complete your {verb}, you must include one {P3}. Choose from ^V2^, ^V2b^, or ^V2c^.'.format(**theme),
                'nl5': 'There are three {P3}s available for your {verb}: ^V2^, ^V2b^, and ^V2c^.'.format(**theme),
                'nl6': 'Your {verb} requires a {P3}. The choices are ^V2^, ^V2b^, and ^V2c^.'.format(**theme),
                'nl7': 'Among the {P3} options for this {verb}, you can select ^V2^, ^V2b^, or ^V2c^.'.format(**theme),
                'nl8': 'To proceed with your {verb}, pick one {P3} from ^V2^, ^V2b^, or ^V2c^.'.format(**theme),
                'nl9': 'For the {theme}, select a {P3} from these options: ^V2^, ^V2b^, ^V2c^.'.format(**theme),
                'nl10': 'In this {theme} {verb}, you are required to include {P3}. The available {P3}s are ^V2^, ^V2b^, and ^V2c^.'.format(**theme)
            }
        )
        storage = p.add_line(
            '{P5}("^V3^"; "^V3b^"; "^V3c^").'.format(**theme),
            {
                'cnl1': '{P5} devices are ^V3^, ^V3b^, ^V3c^.'.format(**theme),
                'cnl2': 'Available {P5} device options for this {verb}: ^V3^, ^V3b^, ^V3c^.'.format(**theme),
                'cnl3': 'Select a {P5} device for your {verb} from ^V3^, ^V3b^, or ^V3c^.'.format(**theme)
            },
            {
                'nl1': 'You can choose a {P5} device for your {verb}. The available {P5} devices are ^V3^, ^V3b^, and ^V3c^.'.format(**theme),
                'nl2': 'For this {verb}, the {P5} device options are ^V3^, ^V3b^, and ^V3c^.'.format(**theme),
                'nl3': 'Select one {P5} device from the following for your {verb}: ^V3^, ^V3b^, ^V3c^.'.format(**theme),
                'nl4': 'To complete your {verb}, you must include one {P5} device. Choose from ^V3^, ^V3b^, or ^V3c^.'.format(**theme),
                'nl5': 'There are three {P5} devices available for your {verb}: ^V3^, ^V3b^, and ^V3c^.'.format(**theme),
                'nl6': 'Your {verb} requires a {P5} device. The choices are ^V3^, ^V3b^, and ^V3c^.'.format(**theme),
                'nl7': 'Among the {P5} device options for this {verb}, you can select ^V3^, ^V3b^, or ^V3c^.'.format(**theme),
                'nl8': 'To proceed with your {verb}, pick one {P5} device from ^V3^, ^V3b^, or ^V3c^.'.format(**theme),
                'nl9': 'For the {theme}, select a {P5} device from these options: ^V3^, ^V3b^, ^V3c^.'.format(**theme),
                'nl10': 'In this {theme} {verb}, you are required to include {P5} device. The available {P5} devices are ^V3^, ^V3b^, and ^V3c^.'.format(**theme)
            }
        )

        p.add_group(
            [cpu, gpu, storage],
            {
                'nl1/3': 'The available components for your {verb} are: {P1}s (^V1^, ^V1b^, ^V1c^), {P3}s (^V2^, ^V2b^, ^V2c^), and {P5} devices (^V3^, ^V3b^, ^V3c^).'.format(**theme),
                'nl2/3': 'You can choose from three {P1}s (^V1^, ^V1b^, ^V1c^), three {P3}s (^V2^, ^V2b^, ^V2c^), and three {P5}  (^V3^, ^V3b^, ^V3c^)devices for your {verb}.'.format(**theme),
                'nl3/3': 'For this {verb}, you must select one {P1} (^V1^, ^V1b^, ^V1c^), one {P3} (^V2^, ^V2b^, ^V2c^), and one {P5} (^V3^, ^V3b^, ^V3c^).'.format(**theme),
                'nl4/3': 'To complete your {verb}, pick a {P1} from ^V1^, ^V1b^, ^V1c^, a {P3} from ^V2^, ^V2b^, ^V2c^, and a {P5} from ^V3^, ^V3b^, ^V3c^.'.format(**theme),
                'nl5/3': 'Your {verb} requires one {P1}, one {P3}, and one {P5} device, each chosen from their respective options: ^V1^, ^V1b^, ^V1c^; ^V2^, ^V2b^, ^V2c^; ^V3^, ^V3b^, ^V3c^.'.format(**theme),
                'nl6/3': 'Among the available components for your {verb}, you must select exactly one from each: {P1} (^V1^, ^V1b^, ^V1c^), {P3} (^V2^, ^V2b^, ^V2c^), {P5} (^V3^, ^V3b^, ^V3c^).'.format(**theme),
                'nl7/3': 'To proceed with your {verb}, select a {P1} from ^V1^, ^V1b^, ^V1c^, a {P3} from ^V2^, ^V2b^, ^V2c^, and a {P5} device from ^V3^, ^V3b^, ^V3c^.'.format(**theme),
                'nl8/3': 'For the {theme}, you are required to include one {P1}, one {P3}, and one {P5} device, each from their respective sets: ^V1^, ^V1b^, ^V1c^; ^V2^, ^V2b^, ^V2c^; ^V3^, ^V3b^, ^V3c^.'.format(**theme),
                'nl9/3': 'In this {theme} {verb}, you must select exactly one {P1} (^V1^, ^V1b^, ^V1c^), one {P3} (^V2^, ^V2b^, ^V2c^), and one {P5} device (^V3^, ^V3b^, ^V3c^).'.format(**theme),
                'nl10/3': 'A valid {verb} for the {theme} requires you to choose one {P1} from ^V1^, ^V1b^, ^V1c^, one {P3} from ^V2^, ^V2b^, ^V2c^, and one {P5} device from ^V3^, ^V3b^, ^V3c^—no more, no less.'.format(**theme)
            }
        )

        # Selection constraints
        cpu_choice = p.add_line(
            '1 {{ {P2}(C) : {P1}(C) }} 1.'.format(**theme),
            {
                'cnl1': 'Select exactly one {P1} from all available {P1}s.'.format(**theme),
                'cnl2': 'You must pick one and only one {P1} for your {verb}.'.format(**theme),
                'cnl3': 'Choose a single {P1} for your {verb} from the set of all {P1}s.'.format(**theme)
            },
            {
                'nl1': 'You must select exactly one {P1} for your {verb}.'.format(**theme),
                'nl2': 'Pick one {P1} from the available options for your {verb}.'.format(**theme),
                'nl3': 'Only one {P1} can be chosen for this {verb}.'.format(**theme),
                'nl4': 'Your {verb} requires you to select a single {P1} from the list.'.format(**theme),
                'nl5': 'Exactly one {P1} must be included in your {verb}.'.format(**theme),
                'nl6': 'Among all {P1}s, you are allowed to select just one for your {verb}.'.format(**theme),
                'nl7': 'To proceed, choose one {P1} for your {verb} and no more.'.format(**theme),
                'nl8': 'You are required to pick a single {P1} for your {verb} from the available choices.'.format(**theme),
                'nl9': 'For this {verb}, ensure that you select one and only one {P1}.'.format(**theme),
                'nl10': 'A valid {verb} must include exactly one {P1} selected from all possible {P1}s.'.format(**theme)
            }
        )
        gpu_choice = p.add_line(
            '1 {{ {P4}(G) : {P3}(G) }} 1.'.format(**theme),
            {
                'cnl1': 'Select exactly one {P3} from all available {P3}s.'.format(**theme),
                'cnl2': 'You must pick one and only one {P3} for your {verb}.'.format(**theme),
                'cnl3': 'Choose a single {P3} for your {verb} from the set of all {P3}s.'.format(**theme)
            },
            {
                'nl1': 'You must select exactly one {P3} for your {verb}.'.format(**theme),
                'nl2': 'Pick one {P3} from the available options for your {verb}.'.format(**theme),
                'nl3': 'Only one {P3} can be chosen for this {verb}.'.format(**theme),
                'nl4': 'Your {verb} requires you to select a single {P3} from the list.'.format(**theme),
                'nl5': 'Exactly one {P3} must be included in your {verb}.'.format(**theme),
                'nl6': 'Among all {P3}s, you are allowed to select just one for your {verb}.'.format(**theme),
                'nl7': 'To proceed, choose one {P3} for your {verb} and no more.'.format(**theme),
                'nl8': 'You are required to pick a single {P3} for your {verb} from the available choices.'.format(**theme),
                'nl9': 'For this {verb}, ensure that you select one and only one {P3}.'.format(**theme),
                'nl10': 'A valid {verb} must include exactly one {P3} selected from all possible {P3}s.'.format(**theme)
            }
        )
        storage_choice = p.add_line(
            '1 {{ {P6}(S) : {P5}(S) }} 1.'.format(**theme),
            {
                'cnl1': 'Select exactly one {P5} device from all available {P5} devices.'.format(**theme),
                'cnl2': 'You must pick one and only one {P5} device for your {verb}.'.format(**theme),
                'cnl3': 'Choose a single {P5} device for your {verb} from the set of all {P5} devices.'.format(**theme)
            },
            {
                'nl1': 'You must select exactly one {P5} device for your {verb}.'.format(**theme),
                'nl2': 'Pick one {P5} device from the available options for your {verb}.'.format(**theme),
                'nl3': 'Only one {P5} device can be chosen for this {verb}.'.format(**theme),
                'nl4': 'Your {verb} requires you to select a single {P5} device from the list.'.format(**theme),
                'nl5': 'Exactly one {P5} device must be included in your {verb}.'.format(**theme),
                'nl6': 'Among all {P5} devices, you are allowed to select just one for your {verb}.'.format(**theme),
                'nl7': 'To proceed, choose one {P5} device for your {verb} and no more.'.format(**theme),
                'nl8': 'You are required to pick a single {P5} device for your {verb} from the available choices.'.format(**theme),
                'nl9': 'For this {verb}, ensure that you select one and only one {P5} device.'.format(**theme),
                'nl10': 'A valid {verb} must include exactly one {P5} device selected from all possible {P5} devices.'.format(**theme)
            }
        )

        p.add_group(
            [cpu_choice, gpu_choice, storage_choice],
            {
                'nl1/3': 'You must select exactly one {P1}, one {P3}, and one {P5} device for your {verb}.'.format(**theme),
                'nl2/3': 'Choose a single {P1}, {P3}, and {P5} from the available options to complete your {verb}.'.format(**theme),
                'nl3/3': 'For this {verb}, you are required to pick one {P1}, one {P3}, and one {P5} device.'.format(**theme),
                'nl4/3': 'To proceed, select one {P1}, one {P3}, and one {P5} device for your {verb}.'.format(**theme),
                'nl5/3': 'Your {verb} must include exactly one {P1}, one {P3}, and one {P5} device, no more and no less.'.format(**theme),
                'nl6/3': 'Among all available options, you are allowed to select just one {P1}, one {P3}, and one {P5} device for your {verb}.'.format(**theme),
                'nl7/3': 'A valid {verb} requires you to pick one {P1}, one {P3}, and one {P5} device from the available choices.'.format(**theme),
                'nl8/3': 'To ensure your {verb} is valid, select exactly one {P1}, one {P3}, and one {P5} device from all possible options.'.format(**theme),
                'nl9/3': 'For this {theme}, you must select one and only one {P1}, {P3}, and {P5} device for your {verb}.'.format(**theme),
                'nl10/3': 'In this {theme} {verb}, you are required to include exactly one {P1}, one {P3}, and one {P5} device, each selected from all available options.'.format(**theme)
            }
        ) 

        # Cost 
        cpu_cost = p.add_line(
            '{P7}("^V1^", ^C1^; "^V1b^", ^C1b^; "^V1c^", ^C1c^).'.format(**theme),
            {
                'cnl1': '{P1} costs are ^V1^=^C1^, ^V1b^=^C1b^, ^V1c^=^C1c^.'.format(**theme),
                'cnl2': 'Each {P1} has a cost: ^V1^ costs ^C1^, ^V1b^ costs ^C1b^, ^V1c^ costs ^C1c^.'.format(**theme),
                'cnl3': 'Assign the following costs to {P1}s: ^V1^=^C1^, ^V1b^=^C1b^, ^V1c^=^C1c^.'.format(**theme)
            },
            {
                'nl1': 'The cost of {P1} ^V1^ is ^C1^, ^V1b^ is ^C1b^, and ^V1c^ is ^C1c^.'.format(**theme),
                'nl2': 'Each {P1} has a specific cost: ^V1^ costs ^C1^, ^V1b^ costs ^C1b^, and ^V1c^ costs ^C1c^.'.format(**theme),
                'nl3': 'For your {verb}, the {P1} options have the following costs: ^V1^ is ^C1^, ^V1b^ is ^C1b^, ^V1c^ is ^C1c^.'.format(**theme),
                'nl4': 'When selecting a {P1}, note that ^V1^ costs ^C1^, ^V1b^ costs ^C1b^, and ^V1c^ costs ^C1c^.'.format(**theme),
                'nl5': 'The available {P1}s are priced as follows: ^V1^ at ^C1^, ^V1b^ at ^C1b^, ^V1c^ at ^C1c^.'.format(**theme),
                'nl6': 'For this {verb}, you can choose a {P1} with these costs: ^V1^ (^C1^), ^V1b^ (^C1b^), ^V1c^ (^C1c^).'.format(**theme),
                'nl7': 'Each {P1} option comes with a cost: ^V1^ is ^C1^, ^V1b^ is ^C1b^, ^V1c^ is ^C1c^.'.format(**theme),
                'nl8': 'Consider the costs of the {P1}s: ^V1^ costs ^C1^, ^V1b^ costs ^C1b^, ^V1c^ costs ^C1c^.'.format(**theme),
                'nl9': 'For the {theme}, the {P1} choices have these costs: ^V1^ (^C1^), ^V1b^ (^C1b^), ^V1c^ (^C1c^).'.format(**theme),
                'nl10': 'In this {theme} {verb}, you must be aware that the {P1}s cost ^C1^ for ^V1^, ^C1b^ for ^V1b^, and ^C1c^ for ^V1c^.'.format(**theme)
            }
        )
        gpu_cost = p.add_line(
            '{P7}("^V2^", ^C2^; "^V2b^", ^C2b^; "^V2c^", ^C2c^).'.format(**theme),
            {
                'cnl1': '{P3} costs are ^V2^=^C2^, ^V2b^=^C2b^, ^V2c^=^C2c^.'.format(**theme),
                'cnl2': 'Each {P3} has a cost: ^V2^ costs ^C2^, ^V2b^ costs ^C2b^, ^V2c^ costs ^C2c^.'.format(**theme),
                'cnl3': 'Assign the following costs to {P3}s: ^V2^=^C2^, ^V2b^=^C2b^, ^V2c^=^C2c^.'.format(**theme)
            },
            {
                'nl1': 'The cost of {P3} ^V2^ is ^C2^, ^V2b^ is ^C2b^, and ^V2c^ is ^C2c^.'.format(**theme),
                'nl2': 'Each {P3} has a specific cost: ^V2^ costs ^C2^, ^V2b^ costs ^C2b^, and ^V2c^ costs ^C2c^.'.format(**theme),
                'nl3': 'For your {verb}, the {P3} options have the following costs: ^V2^ is ^C2^, ^V2b^ is ^C2b^, ^V2c^ is ^C2c^.'.format(**theme),
                'nl4': 'When selecting a {P3}, note that ^V2^ costs ^C2^, ^V2b^ costs ^C2b^, and ^V2c^ costs ^C2c^.'.format(**theme),
                'nl5': 'The available {P3}s are priced as follows: ^V2^ at ^C2^, ^V2b^ at ^C2b^, ^V2c^ at ^C2c^.'.format(**theme),
                'nl6': 'For this {verb}, you can choose a {P3} with these costs: ^V2^ (^C2^), ^V2b^ (^C2b^), ^V2c^ (^C2c^).'.format(**theme),
                'nl7': 'Each {P3} option comes with a cost: ^V2^ is ^C2^, ^V2b^ is ^C2b^, ^V2c^ is ^C2c^.'.format(**theme),
                'nl8': 'Consider the costs of the {P3}s: ^V2^ costs ^C2^, ^V2b^ costs ^C2b^, ^V2c^ costs ^C2c^.'.format(**theme),
                'nl9': 'For the {theme}, the {P3} choices have these costs: ^V2^ (^C2^), ^V2b^ (^C2b^), ^V2c^ (^C2c^).'.format(**theme),
                'nl10': 'In this {theme} {verb}, you must be aware that the {P3}s cost ^C2^ for ^V2^, ^C2b^ for ^V2b^, and ^C2c^ for ^V2c^.'.format(**theme)
            }
        )
        storage_cost = p.add_line(
            '{P7}("^V3^", ^C3^; "^V3b^", ^C3b^; "^V3c^", ^C3c^).'.format(**theme),
            {
                'cnl1': '{P5} device costs are ^V3^=^C3^, ^V3b^=^C3b^, ^V3c^=^C3c^.'.format(**theme),
                'cnl2': 'Each {P5} device has a cost: ^V3^ costs ^C3^, ^V3b^ costs ^C3b^, ^V3c^ costs ^C3c^.'.format(**theme),
                'cnl3': 'Assign the following costs to {P5} devices: ^V3^=^C3^, ^V3b^=^C3b^, ^V3c^=^C3c^.'.format(**theme)
            },
            {
                'nl1': 'The cost of {P5} device ^V3^ is ^C3^, ^V3b^ is ^C3b^, and ^V3c^ is ^C3c^.'.format(**theme),
                'nl2': 'Each {P5} device has a specific cost: ^V3^ costs ^C3^, ^V3b^ costs ^C3b^, and ^V3c^ costs ^C3c^.'.format(**theme),
                'nl3': 'For your {verb}, the {P5} device options have the following costs: ^V3^ is ^C3^, ^V3b^ is ^C3b^, ^V3c^ is ^C3c^.'.format(**theme),
                'nl4': 'When selecting a {P5} device, note that ^V3^ costs ^C3^, ^V3b^ costs ^C3b^, and ^V3c^ costs ^C3c^.'.format(**theme),
                'nl5': 'The available {P5} devices are priced as follows: ^V3^ at ^C3^, ^V3b^ at ^C3b^, ^V3c^ at ^C3c^.'.format(**theme),
                'nl6': 'For this {verb}, you can choose a {P5} device with these costs: ^V3^ (^C3^), ^V3b^ (^C3b^), ^V3c^ (^C3c^).'.format(**theme),
                'nl7': 'Each {P5} device option comes with a cost: ^V3^ is ^C3^, ^V3b^ is ^C3b^, ^V3c^ is ^C3c^.'.format(**theme),
                'nl8': 'Consider the costs of the {P5} devices: ^V3^ costs ^C3^, ^V3b^ costs ^C3b^, ^V3c^ costs ^C3c^.'.format(**theme),
                'nl9': 'For the {theme}, the {P5} device choices have these costs: ^V3^ (^C3^), ^V3b^ (^C3b^), ^V3c^ (^C3c^).'.format(**theme),
                'nl10': 'In this {theme} {verb}, you must be aware that the {P5} devices cost ^C3^ for ^V3^, ^C3b^ for ^V3b^, and ^C3c^ for ^V3c^.'.format(**theme)
            }
        )

        p.add_group(
            [cpu_cost, gpu_cost, storage_cost],
            {
                'nl1/6': (
                    '{P1} costs: ^V1^ (^C1^), ^V1b^ (^C1b^), ^V1c^ (^C1c^); '
                    '{P3} costs: ^V2^ (^C2^), ^V2b^ (^C2b^), ^V2c^ (^C2c^); '
                    '{P5} costs: ^V3^ (^C3^), ^V3b^ (^C3b^), ^V3c^ (^C3c^).'
                ).format(**theme),
                'nl2/6': (
                    'Each {P1}, {P3}, and {P5} device has an associated cost: '
                    '{P1}s (^V1^: ^C1^, ^V1b^: ^C1b^, ^V1c^: ^C1c^), '
                    '{P3}s (^V2^: ^C2^, ^V2b^: ^C2b^, ^V2c^: ^C2c^), '
                    '{P5}s (^V3^: ^C3^, ^V3b^: ^C3b^, ^V3c^: ^C3c^).'
                ).format(**theme),
                'nl3/6': (
                    'For your {verb}, the costs are as follows: {P1}s (^V1^: ^C1^, ^V1b^: ^C1b^, ^V1c^: ^C1c^), '
                    '{P3}s (^V2^: ^C2^, ^V2b^: ^C2b^, ^V2c^: ^C2c^), {P5} devices (^V3^: ^C3^, ^V3b^: ^C3b^, ^V3c^: ^C3c^).'
                ).format(**theme),
                'nl4/6': (
                    'When making your {verb}, note the following costs: {P1}s (^V1^ at ^C1^, ^V1b^ at ^C1b^, ^V1c^ at ^C1c^), '
                    '{P3}s (^V2^ at ^C2^, ^V2b^ at ^C2b^, ^V2c^ at ^C2c^), {P5} devices (^V3^ at ^C3^, ^V3b^ at ^C3b^, ^V3c^ at ^C3c^).'
                ).format(**theme),
                'nl5/6': (
                    'The pricing for each component in your {verb} is: {P1}s (^V1^: ^C1^, ^V1b^: ^C1b^, ^V1c^: ^C1c^); '
                    '{P3}s (^V2^: ^C2^, ^V2b^: ^C2b^, ^V2c^: ^C2c^); {P5} devices (^V3^: ^C3^, ^V3b^: ^C3b^, ^V3c^: ^C3c^).'
                ).format(**theme),
                'nl6/6': (
                    'For the {theme}, each {P1}, {P3}, and {P5} device comes with a specific cost: '
                    '{P1}s (^V1^: ^C1^, ^V1b^: ^C1b^, ^V1c^: ^C1c^), {P3}s (^V2^: ^C2^, ^V2b^: ^C2b^, ^V2c^: ^C2c^), '
                    '{P5} devices (^V3^: ^C3^, ^V3b^: ^C3b^, ^V3c^: ^C3c^).'
                ).format(**theme),
                'nl7/6': (
                    'In this {theme} {verb}, the cost for each {P1}, {P3}, and {P5} device is as follows: '
                    '{P1}s (^V1^: ^C1^, ^V1b^: ^C1b^, ^V1c^: ^C1c^), {P3}s (^V2^: ^C2^, ^V2b^: ^C2b^, ^V2c^: ^C2c^), '
                    '{P5} devices (^V3^: ^C3^, ^V3b^: ^C3b^, ^V3c^: ^C3c^).'
                ).format(**theme),
                'nl8/6': (
                    'Be aware that for your {verb}, each {P1}, {P3}, and {P5} device has its own cost: '
                    '{P1}s (^V1^: ^C1^, ^V1b^: ^C1b^, ^V1c^: ^C1c^), {P3}s (^V2^: ^C2^, ^V2b^: ^C2b^, ^V2c^: ^C2c^), '
                    '{P5} devices (^V3^: ^C3^, ^V3b^: ^C3b^, ^V3c^: ^C3c^).'
                ).format(**theme),
                'nl9/6': (
                    'To make an informed {verb}, consider the following costs for each component: '
                    '{P1}s (^V1^: ^C1^, ^V1b^: ^C1b^, ^V1c^: ^C1c^), {P3}s (^V2^: ^C2^, ^V2b^: ^C2b^, ^V2c^: ^C2c^), '
                    '{P5} devices (^V3^: ^C3^, ^V3b^: ^C3b^, ^V3c^: ^C3c^).'
                ).format(**theme),
                'nl10/6': (
                    'For this {theme} {verb}, the cost structure is as follows: '
                    '{P1}s (^V1^: ^C1^, ^V1b^: ^C1b^, ^V1c^: ^C1c^), {P3}s (^V2^: ^C2^, ^V2b^: ^C2b^, ^V2c^: ^C2c^), '
                    '{P5} devices (^V3^: ^C3^, ^V3b^: ^C3b^, ^V3c^: ^C3c^). Make your selections accordingly.'
                ).format(**theme),
            }
        )

        # Performance

        cpu_perf = p.add_line(
            '{P8}("^V1^", ^P1_perf^; "^V1b^", ^P1b_perf^; "^V1c^", ^P1c_perf^).'.format(**theme),
            {
                'cnl1': '{P1} {P8} values: ^V1^=^P1_perf^, ^V1b^=^P1b_perf^, ^V1c^=^P1c_perf^.'.format(**theme),
                'cnl2': 'Each {P1} has a {P8} value: ^V1^ is ^P1_perf^, ^V1b^ is ^P1b_perf^, ^V1c^ is ^P1c_perf^.'.format(**theme),
                'cnl3': 'Assign the following {P8} values to {P1}s: ^V1^=^P1_perf^, ^V1b^=^P1b_perf^, ^V1c^=^P1c_perf^.'.format(**theme)
            },
            {
                'nl1': 'The {P8} value of {P1} ^V1^ is ^P1_perf^, ^V1b^ is ^P1b_perf^, and ^V1c^ is ^P1c_perf^.'.format(**theme),
                'nl2': 'Each {P1} has a specific {P8} value: ^V1^ is ^P1_perf^, ^V1b^ is ^P1b_perf^, and ^V1c^ is ^P1c_perf^.'.format(**theme),
                'nl3': 'For your {verb}, the {P1} options have the following {P8} values: ^V1^ is ^P1_perf^, ^V1b^ is ^P1b_perf^, ^V1c^ is ^P1c_perf^.'.format(**theme),
                'nl4': 'When selecting a {P1}, note that ^V1^ has a {P8} of ^P1_perf^, ^V1b^ has ^P1b_perf^, and ^V1c^ has ^P1c_perf^.'.format(**theme),
                'nl5': 'The available {P1}s are rated as follows: ^V1^ at ^P1_perf^, ^V1b^ at ^P1b_perf^, ^V1c^ at ^P1c_perf^.'.format(**theme),
                'nl6': 'For this {verb}, you can choose a {P1} with these {P8} values: ^V1^ (^P1_perf^), ^V1b^ (^P1b_perf^), ^V1c^ (^P1c_perf^).'.format(**theme),
                'nl7': 'Each {P1} option comes with a {P8} value: ^V1^ is ^P1_perf^, ^V1b^ is ^P1b_perf^, ^V1c^ is ^P1c_perf^.'.format(**theme),
                'nl8': 'Consider the {P8} values of the {P1}s: ^V1^ is ^P1_perf^, ^V1b^ is ^P1b_perf^, ^V1c^ is ^P1c_perf^.'.format(**theme),
                'nl9': 'For the {theme}, the {P1} choices have these {P8} values: ^V1^ (^P1_perf^), ^V1b^ (^P1b_perf^), ^V1c^ (^P1c_perf^).'.format(**theme),
                'nl10': 'In this {theme} {verb}, you must be aware that the {P1}s have {P8} values of ^P1_perf^ for ^V1^, ^P1b_perf^ for ^V1b^, and ^P1c_perf^ for ^V1c^.'.format(**theme)
            }
        )

        gpu_perf = p.add_line(
            '{P8}("^V2^", ^P2_perf^; "^V2b^", ^P2b_perf^; "^V2c^", ^P2c_perf^).'.format(**theme),
            {
                'cnl1': '{P3} {P8} values: ^V2^=^P2_perf^, ^V2b^=^P2b_perf^, ^V2c^=^P2c_perf^.'.format(**theme),
                'cnl2': 'Each {P3} has a {P8} value: ^V2^ is ^P2_perf^, ^V2b^ is ^P2b_perf^, ^V2c^ is ^P2c_perf^.'.format(**theme),
                'cnl3': 'Assign the following {P8} values to {P3}s: ^V2^=^P2_perf^, ^V2b^=^P2b_perf^, ^V2c^=^P2c_perf^.'.format(**theme)
            },
            {
                'nl1': 'The {P8} value of {P3} ^V2^ is ^P2_perf^, ^V2b^ is ^P2b_perf^, and ^V2c^ is ^P2c_perf^.'.format(**theme),
                'nl2': 'Each {P3} has a specific {P8} value: ^V2^ is ^P2_perf^, ^V2b^ is ^P2b_perf^, and ^V2c^ is ^P2c_perf^.'.format(**theme),
                'nl3': 'For your {verb}, the {P3} options have the following {P8} values: ^V2^ is ^P2_perf^, ^V2b^ is ^P2b_perf^, ^V2c^ is ^P2c_perf^.'.format(**theme),
                'nl4': 'When selecting a {P3}, note that ^V2^ has a {P8} of ^P2_perf^, ^V2b^ has ^P2b_perf^, and ^V2c^ has ^P2c_perf^.'.format(**theme),
                'nl5': 'The available {P3}s are rated as follows: ^V2^ at ^P2_perf^, ^V2b^ at ^P2b_perf^, ^V2c^ at ^P2c_perf^.'.format(**theme),
                'nl6': 'For this {verb}, you can choose a {P3} with these {P8} values: ^V2^ (^P2_perf^), ^V2b^ (^P2b_perf^), ^V2c^ (^P2c_perf^).'.format(**theme),
                'nl7': 'Each {P3} option comes with a {P8} value: ^V2^ is ^P2_perf^, ^V2b^ is ^P2b_perf^, ^V2c^ is ^P2c_perf^.'.format(**theme),
                'nl8': 'Consider the {P8} values of the {P3}s: ^V2^ is ^P2_perf^, ^V2b^ is ^P2b_perf^, ^V2c^ is ^P2c_perf^.'.format(**theme),
                'nl9': 'For the {theme}, the {P3} choices have these {P8} values: ^V2^ (^P2_perf^), ^V2b^ (^P2b_perf^), ^V2c^ (^P2c_perf^).'.format(**theme),
                'nl10': 'In this {theme} {verb}, you must be aware that the {P3}s have {P8} values of ^P2_perf^ for ^V2^, ^P2b_perf^ for ^V2b^, and ^P2c_perf^ for ^V2c^.'.format(**theme)
            }
        )

        storage_perf = p.add_line(
            '{P8}("^V3^", ^P3_perf^; "^V3b^", ^P3b_perf^; "^V3c^", ^P3c_perf^).'.format(**theme),
            {
                'cnl1': '{P5} {P8} values: ^V3^=^P3_perf^, ^V3b^=^P3b_perf^, ^V3c^=^P3c_perf^.'.format(**theme),
                'cnl2': 'Each {P5} has a {P8} value: ^V3^ is ^P3_perf^, ^V3b^ is ^P3b_perf^, ^V3c^ is ^P3c_perf^.'.format(**theme),
                'cnl3': 'Assign the following {P8} values to {P5}s: ^V3^=^P3_perf^, ^V3b^=^P3b_perf^, ^V3c^=^P3c_perf^.'.format(**theme)
            },
            {
                'nl1': 'The {P8} value of {P5} ^V3^ is ^P3_perf^, ^V3b^ is ^P3b_perf^, and ^V3c^ is ^P3c_perf^.'.format(**theme),
                'nl2': 'Each {P5} has a specific {P8} value: ^V3^ is ^P3_perf^, ^V3b^ is ^P3b_perf^, and ^V3c^ is ^P3c_perf^.'.format(**theme),
                'nl3': 'For your {verb}, the {P5} options have the following {P8} values: ^V3^ is ^P3_perf^, ^V3b^ is ^P3b_perf^, ^V3c^ is ^P3c_perf^.'.format(**theme),
                'nl4': 'When selecting a {P5}, note that ^V3^ has a {P8} of ^P3_perf^, ^V3b^ has ^P3b_perf^, and ^V3c^ has ^P3c_perf^.'.format(**theme),
                'nl5': 'The available {P5} devices are rated as follows: ^V3^ at ^P3_perf^, ^V3b^ at ^P3b_perf^, ^V3c^ at ^P3c_perf^.'.format(**theme),
                'nl6': 'For this {verb}, you can choose a {P5} device with these {P8} values: ^V3^ (^P3_perf^), ^V3b^ (^P3b_perf^), ^V3c^ (^P3c_perf^).'.format(**theme),
                'nl7': 'Each {P5} device option comes with a {P8} value: ^V3^ is ^P3_perf^, ^V3b^ is ^P3b_perf^, ^V3c^ is ^P3c_perf^.'.format(**theme),
                'nl8': 'Consider the {P8} values of the {P5} devices: ^V3^ is ^P3_perf^, ^V3b^ is ^P3b_perf^, ^V3c^ is ^P3c_perf^.'.format(**theme),
                'nl9': 'For the {theme}, the {P5} device choices have these {P8} values: ^V3^ (^P3_perf^), ^V3b^ (^P3b_perf^), ^V3c^ (^P3c_perf^).'.format(**theme),
                'nl10': 'In this {theme} {verb}, you must be aware that the {P5} devices have {P8} values of ^P3_perf^ for ^V3^, ^P3b_perf^ for ^V3b^, and ^P3c_perf^ for ^V3c^.'.format(**theme)
            }
        )

        p.add_group(
            [cpu_perf, gpu_perf, storage_perf],
            {
                'nl1/6': (
                    '{P1} {P8}: ^V1^ (^P1_perf^), ^V1b^ (^P1b_perf^), ^V1c^ (^P1c_perf^); '
                    '{P3} {P8}: ^V2^ (^P2_perf^), ^V2b^ (^P2b_perf^), ^V2c^ (^P2c_perf^); '
                    '{P5} {P8}: ^V3^ (^P3_perf^), ^V3b^ (^P3b_perf^), ^V3c^ (^P3c_perf^).'
                ).format(**theme),
                'nl2/6': (
                    'Each {P1}, {P3}, and {P5} device has a {P8} value: '
                    '{P1}s (^V1^: ^P1_perf^, ^V1b^: ^P1b_perf^, ^V1c^: ^P1c_perf^), '
                    '{P3}s (^V2^: ^P2_perf^, ^V2b^: ^P2b_perf^, ^V2c^: ^P2c_perf^), '
                    '{P5}s (^V3^: ^P3_perf^, ^V3b^: ^P3b_perf^, ^V3c^: ^P3c_perf^).'
                ).format(**theme),
                'nl3/6': (
                    'For your {verb}, the {P8} values are as follows: {P1}s (^V1^: ^P1_perf^, ^V1b^: ^P1b_perf^, ^V1c^: ^P1c_perf^), '
                    '{P3}s (^V2^: ^P2_perf^, ^V2b^: ^P2b_perf^, ^V2c^: ^P2c_perf^), {P5} devices (^V3^: ^P3_perf^, ^V3b^: ^P3b_perf^, ^V3c^: ^C3c_perf^).'
                ).format(**theme),
                'nl4/6': (
                    'When making your {verb}, note the following {P8} values: {P1}s (^V1^ at ^P1_perf^, ^V1b^ at ^P1b_perf^, ^V1c^ at ^P1c_perf^), '
                    '{P3}s (^V2^ at ^P2_perf^, ^V2b^ at ^P2b_perf^, ^V2c^ at ^P2c_perf^), {P5} devices (^V3^ at ^P3_perf^, ^V3b^ at ^P3b_perf^, ^V3c^ at ^C3c^).'
                ).format(**theme),
                'nl5/6': (
                    'The {P8} for each component in your {verb} is: {P1}s (^V1^: ^P1_perf^, ^V1b^: ^P1b_perf^, ^V1c^: ^P1c_perf^); '
                    '{P3}s (^V2^: ^P2_perf^, ^V2b^: ^P2b_perf^, ^V2c^: ^P2c_perf^); {P5} devices (^V3^: ^P3_perf^, ^V3b^: ^P3b_perf^, ^V3c^: ^C3c_perf^).'
                ).format(**theme),
                'nl6/6': (
                    'For the {theme}, each {P1}, {P3}, and {P5} device comes with a {P8} value: '
                    '{P1}s (^V1^: ^P1_perf^, ^V1b^: ^P1b_perf^, ^V1c^: ^P1c_perf^), {P3}s (^V2^: ^P2_perf^, ^V2b^: ^P2b_perf^, ^V2c^: ^C2c_perf^), '
                    '{P5} devices (^V3^: ^P3_perf^, ^V3b^: ^P3b_perf^, ^V3c^: ^C3c_perf^).'
                ).format(**theme),
                'nl7/6': (
                    'In this {theme} {verb}, the {P8} for each {P1}, {P3}, and {P5} device is as follows: '
                    '{P1}s (^V1^: ^P1_perf^, ^V1b^: ^P1b_perf^, ^V1c^: ^P1c_perf^), {P3}s (^V2^: ^P2_perf^, ^V2b^: ^P2b_perf^, ^V2c^: ^C2c_perf^), '
                    '{P5} devices (^V3^: ^P3_perf^, ^V3b^: ^P3b_perf^, ^V3c^: ^C3c_perf^).'
                ).format(**theme),
                'nl8/6': (
                    'Be aware that for your {verb}, each {P1}, {P3}, and {P5} device has its own {P8} value: '
                    '{P1}s (^V1^: ^P1_perf^, ^V1b^: ^P1b_perf^, ^V1c^: ^P1c_perf^), {P3}s (^V2^: ^P2_perf^, ^V2b^: ^P2b_perf^, ^V2c^: ^C2c_perf^), '
                    '{P5} devices (^V3^: ^P3_perf^, ^V3b^: ^P3b_perf^, ^V3c^: ^C3c_perf^).'
                ).format(**theme),
                'nl9/6': (
                    'To make an informed {verb}, consider the following {P8} values for each component: '
                    '{P1}s (^V1^: ^P1_perf^, ^V1b^: ^P1b_perf^, ^V1c^: ^P1c_perf^), {P3}s (^V2^: ^P2_perf^, ^V2b^: ^P2b_perf^, ^V2c^: ^C2c_perf^), '
                    '{P5} devices (^V3^: ^P3_perf^, ^V3b^: ^P3b_perf^, ^V3c^: ^C3c_perf^).'
                ).format(**theme),
                'nl10/6': (
                    'For this {theme} {verb}, the {P8} structure is as follows: '
                    '{P1}s (^V1^: ^P1_perf^, ^V1b^: ^P1b_perf^, ^V1c^: ^P1c_perf^), {P3}s (^V2^: ^P2_perf^, ^V2b^: ^P2b_perf^, ^V2c^: ^C2c_perf^), '
                    '{P5} devices (^V3^: ^P3_perf^, ^V3b^: ^P3b_perf^, ^V3c^: ^C3c_perf^). Make your selections accordingly.'
                ).format(**theme),
            }
        )

        # Constraints - The most expensive selected component must also be the one with the highest performance among selected parts.
        selected_cpu_union = p.add_line(
            '{P9}(X) :- {P2}(X).'.format(**theme),
            {
                'cnl1': '{P9} includes all selected {P1}.'.format(**theme),
                'cnl2': 'For every selected {P1}, add it to {P9}.'.format(**theme),
                'cnl3': '{P9} is the set of all selected {P1}.'.format(**theme)
            },
            {
                'nl1': '{P9} includes any {P1} that is selected.'.format(**theme),
                'nl2': 'Any selected {P1} is included in {P9}.'.format(**theme),
                'nl3': '{P9} will contain every {P1} that has been selected.'.format(**theme),
                'nl4': 'If a {P1} is selected, it is part of {P9}.'.format(**theme),
                'nl5': 'All chosen {P1}s are included in {P9}.'.format(**theme),
                'nl6': '{P9} represents the set of selected {P1}s.'.format(**theme),
                'nl7': 'Whenever a {P1} is selected, it is added to {P9}.'.format(**theme),
                'nl8': 'The set {P9} consists of all selected {P1}s.'.format(**theme),
                'nl9': 'Each selected {P1} will be present in {P9}.'.format(**theme),
                'nl10': '{P9} is the collection of all {P1}s that have been selected.'.format(**theme)
            }
        )
        selected_gpu_union = p.add_line(
            '{P9}(X) :- {P4}(X).'.format(**theme),
            {
                'cnl1': '{P9} includes all selected {P3}.'.format(**theme),
                'cnl2': 'For every selected {P3}, add it to {P9}.'.format(**theme),
                'cnl3': '{P9} is the set of all selected {P3}.'.format(**theme)
            },
            {
                'nl1': '{P9} includes any {P3} that is selected.'.format(**theme),
                'nl2': 'Any selected {P3} is included in {P9}.'.format(**theme),
                'nl3': '{P9} will contain every {P3} that has been selected.'.format(**theme),
                'nl4': 'If a {P3} is selected, it is part of {P9}.'.format(**theme),
                'nl5': 'All chosen {P3}s are included in {P9}.'.format(**theme),
                'nl6': '{P9} represents the set of selected {P3}s.'.format(**theme),
                'nl7': 'Whenever a {P3} is selected, it is added to {P9}.'.format(**theme),
                'nl8': 'The set {P9} consists of all selected {P3}s.'.format(**theme),
                'nl9': 'Each selected {P3} will be present in {P9}.'.format(**theme),
                'nl10': '{P9} is the collection of all {P3}s that have been selected.'.format(**theme)
            }
        )
        selected_storage_union = p.add_line(
            '{P9}(X) :- {P6}(X).'.format(**theme),
            {
                'cnl1': '{P9} includes all selected {P5}.'.format(**theme),
                'cnl2': 'For every selected {P5}, add it to {P9}.'.format(**theme),
                'cnl3': '{P9} is the set of all selected {P5}.'.format(**theme)
            },
            {
                'nl1': '{P9} includes any {P5} that is selected.'.format(**theme),
                'nl2': 'Any selected {P5} is included in {P9}.'.format(**theme),
                'nl3': '{P9} will contain every {P5} that has been selected.'.format(**theme),
                'nl4': 'If a {P5} is selected, it is part of {P9}.'.format(**theme),
                'nl5': 'All chosen {P5}s are included in {P9}.'.format(**theme),
                'nl6': '{P9} represents the set of selected {P5}s.'.format(**theme),
                'nl7': 'Whenever a {P5} is selected, it is added to {P9}.'.format(**theme),
                'nl8': 'The set {P9} consists of all selected {P5}s.'.format(**theme),
                'nl9': 'Each selected {P5} will be present in {P9}.'.format(**theme),
                'nl10': '{P9} is the collection of all {P5}s that have been selected.'.format(**theme)
            }
        )

        max_cost = p.add_line(
            '{P10}(C) :- {P7}(C, V), V = #max {{V1 : {P7}(C1, V1), {P9}(C1)}}.'.format(**theme),
            {
                'cnl1': '{P10} is true for the selected component with the highest cost.'.format(**theme),
                'cnl2': '{P10} holds for the selected part that has the maximum cost.'.format(**theme),
                'cnl3': '{P10} marks the selected item with the greatest cost.'.format(**theme)
            },
            {
                'nl1': '{P10} marks the selected part with the highest cost among your choices.'.format(**theme),
                'nl2': 'The selected component with the highest cost is identified by {P10}.'.format(**theme),
                'nl3': '{P10} is used to indicate which selected part is the most expensive.'.format(**theme),
                'nl4': 'Among all selected parts, {P10} highlights the one with the greatest cost.'.format(**theme),
                'nl5': '{P10} is true for the most expensive selected component.'.format(**theme),
                'nl6': '{P10} identifies the selected part that costs the most.'.format(**theme),
                'nl7': 'If a selected part has the highest cost, it is marked by {P10}.'.format(**theme),
                'nl8': 'The part with the maximum cost among those selected is indicated by {P10}.'.format(**theme),
                'nl9': '{P10} applies to the selected component with the largest cost value.'.format(**theme),
                'nl10': 'Use {P10} to find which selected part is the most expensive.'.format(**theme)
            }
        )
        max_perf = p.add_line(
            '{P11}(C) :- {P8}(C, V), V = #max {{V1 : {P8}(C1, V1), {P9}(C1)}}.'.format(**theme),
            {
                'cnl1': '{P11} is true for the selected component with the highest {P8}.'.format(**theme),
                'cnl2': '{P11} holds for the selected part that has the maximum {P8} value.'.format(**theme),
                'cnl3': '{P11} marks the selected item with the greatest {P8} value.'.format(**theme)
            },
            {
                'nl1': '{P11} marks the selected part with the highest {P8} among your choices.'.format(**theme),
                'nl2': 'The selected component with the highest {P8} is identified by {P11}.'.format(**theme),
                'nl3': '{P11} is used to indicate which selected part has the highest {P8}.'.format(**theme),
                'nl4': 'Among all selected parts, {P11} highlights the one with the greatest {P8}.'.format(**theme),
                'nl5': '{P11} is true for the selected component with the highest {P8}.'.format(**theme),
                'nl6': '{P11} identifies the selected part with the largest {P8} value.'.format(**theme),
                'nl7': 'If a selected part has the highest {P8}, it is marked by {P11}.'.format(**theme),
                'nl8': 'The part with the maximum {P8} among those selected is indicated by {P11}.'.format(**theme),
                'nl9': '{P11} applies to the selected component with the greatest {P8}.'.format(**theme),
                'nl10': 'Use {P11} to find which selected part has the highest {P8}.'.format(**theme)
            }
        )
        expensive_perf_constraint = p.add_line(
            ':- {P9}(C), {P10}(C), not {P11}(C).'.format(**theme),
            {
                'cnl1': 'The most expensive selected component must also be the one with the highest {P8}.'.format(**theme),
                'cnl2': 'It is required that the most expensive selected part is also the highest in {P8}.'.format(**theme),
                'cnl3': 'No selected component can be the most expensive without also having the highest {P8}.'.format(**theme)
            },
            {
                'nl1': 'The most expensive selected part must also be the highest in {P8} among your choices.'.format(**theme),
                'nl2': 'You cannot select a component that is the most expensive unless it also has the highest {P8}.'.format(**theme),
                'nl3': 'Among your selected parts, the one with the highest cost must also have the highest {P8}.'.format(**theme),
                'nl4': 'It is not allowed for the most expensive selected component to have less than the highest {P8}.'.format(**theme),
                'nl5': 'Only the most expensive selected part can also be the highest in {P8}.'.format(**theme),
                'nl6': 'If a selected part is the most expensive, it must also have the highest {P8}.'.format(**theme),
                'nl7': 'The part with the greatest cost must also be the one with the greatest {P8}.'.format(**theme),
                'nl8': 'You must not select a part that is most expensive but not highest in {P8}.'.format(**theme),
                'nl9': 'The rule enforces that the most expensive selected part is also the top in {P8}.'.format(**theme),
                'nl10': 'A valid selection requires the most expensive part to also have the highest {P8}.'.format(**theme)
            }
        )

        p.add_group(
            [
                selected_cpu_union,
                selected_gpu_union,
                selected_storage_union,
                max_cost,
                max_perf,
                expensive_perf_constraint
            ],
            {
                'nl1/10': (
                    'All selected {P1}, {P3}, and {P5} devices are grouped as {P9}. '
                    '{P10} is true for the selected component with the highest cost, and {P11} is true for the one with the highest {P8}. '
                    'The most expensive selected component must also be the one with the highest {P8}.'
                ).format(**theme),
                'nl2/10': (
                    'After selecting your {P1}, {P3}, and {P5}, they are all included in {P9}. '
                    '{P10} marks the most expensive selected part, and {P11} marks the one with the highest {P8}. '
                    'It is required that the most expensive selected part is also the highest in {P8}.'
                ).format(**theme),
                'nl3/10': (
                    '{P9} contains all selected {P1}, {P3}, and {P5} devices. '
                    '{P10} identifies the selected component with the greatest cost, and {P11} identifies the one with the greatest {P8}. '
                    'No selected component can be the most expensive without also having the highest {P8}.'
                ).format(**theme),
                'nl4/10': (
                    'All chosen {P1}, {P3}, and {P5} devices are included in {P9}. '
                    '{P10} is used for the most expensive, and {P11} for the highest {P8}. '
                    'The most expensive selected device must also have the highest {P8}.'
                ).format(**theme),
                'nl5/10': (
                    'Selected {P1}, {P3}, and {P5} devices are grouped as {P9}. '
                    '{P10} applies to the most expensive, and {P11} to the highest {P8}. '
                    'It is not allowed for the most expensive device to have less than the highest {P8}.'
                ).format(**theme),
                'nl6/10': (
                    'Once selected, all {P1}, {P3}, and {P5} devices are part of {P9}. '
                    '{P10} marks the highest cost, {P11} marks the highest {P8}. '
                    'Only the most expensive selected device can also be the highest in {P8}.'
                ).format(**theme),
                'nl7/10': (
                    'The set {P9} includes every selected {P1}, {P3}, and {P5}. '
                    '{P10} is for the most expensive, {P11} for the highest {P8}. '
                    'A valid selection requires the most expensive device to also be the highest in {P8}.'
                ).format(**theme),
                'nl8/10': (
                    'After selection, all {P1}, {P3}, and {P5} devices are grouped as {P9}. '
                    '{P10} and {P11} identify the most expensive and highest {P8} devices, respectively. '
                    'The most expensive selected device must also be the highest in {P8}.'
                ).format(**theme),
                'nl9/10': (
                    'All selected devices ({P1}, {P3}, {P5}) are included in {P9}. '
                    '{P10} highlights the most expensive, {P11} the highest {P8}. '
                    'It is required that the most expensive device is also the highest in {P8}.'
                ).format(**theme),
                'nl10/10': (
                    'Selected {P1}, {P3}, and {P5} devices are grouped as {P9}. '
                    '{P10} and {P11} indicate the most expensive and highest {P8} devices. '
                    'A valid selection means the most expensive device is also the highest in {P8}.'
                ).format(**theme),
            }
        )

        # You may not select all three top-performing components.
        top_cpu = p.add_line(
            '{P12}(C) :- {P1}(C), {P8}(C, V), V = #max {{V1 : {P8}(C1, V1), {P1}(C1)}}.'.format(**theme),
            {
                'cnl1': '{P12} is true for the {P1} with the highest {P8}.'.format(**theme),
                'cnl2': '{P12} holds for the {P1} that has the maximum {P8} value.'.format(**theme),
                'cnl3': '{P12} marks the {P1} with the greatest {P8} value.'.format(**theme)
            },
            {
                'nl1': '{P12} marks the {P1} with the highest {P8}.'.format(**theme),
                'nl2': 'The {P1} with the highest {P8} is identified by {P12}.'.format(**theme),
                'nl3': '{P12} is used to indicate which {P1} has the highest {P8}.'.format(**theme),
                'nl4': 'Among all {P1}s, {P12} highlights the one with the greatest {P8}.'.format(**theme),
                'nl5': '{P12} is true for the {P1} with the highest {P8}.'.format(**theme),
                'nl6': '{P12} identifies the {P1} with the largest {P8} value.'.format(**theme),
                'nl7': 'If a {P1} has the highest {P8}, it is marked by {P12}.'.format(**theme),
                'nl8': 'The {P1} with the maximum {P8} is indicated by {P12}.'.format(**theme),
                'nl9': '{P12} applies to the {P1} with the greatest {P8}.'.format(**theme),
                'nl10': 'Use {P12} to find which {P1} has the highest {P8}.'.format(**theme)
            }
        )
        top_gpu = p.add_line(
            '{P13}(C) :- {P3}(C), {P8}(C, V), V = #max {{V1 : {P8}(C1, V1), {P3}(C1)}}.'.format(**theme),
            {
                'cnl1': '{P13} is true for the {P3} with the highest {P8}.'.format(**theme),
                'cnl2': '{P13} holds for the {P3} that has the maximum {P8} value.'.format(**theme),
                'cnl3': '{P13} marks the {P3} with the greatest {P8} value.'.format(**theme)
            },
            {
                'nl1': '{P13} marks the {P3} with the highest {P8}.'.format(**theme),
                'nl2': 'The {P3} with the highest {P8} is identified by {P13}.'.format(**theme),
                'nl3': '{P13} is used to indicate which {P3} has the highest {P8}.'.format(**theme),
                'nl4': 'Among all {P3}s, {P13} highlights the one with the greatest {P8}.'.format(**theme),
                'nl5': '{P13} is true for the {P3} with the highest {P8}.'.format(**theme),
                'nl6': '{P13} identifies the {P3} with the largest {P8} value.'.format(**theme),
                'nl7': 'If a {P3} has the highest {P8}, it is marked by {P13}.'.format(**theme),
                'nl8': 'The {P3} with the maximum {P8} is indicated by {P13}.'.format(**theme),
                'nl9': '{P13} applies to the {P3} with the greatest {P8}.'.format(**theme),
                'nl10': 'Use {P13} to find which {P3} has the highest {P8}.'.format(**theme)
            }
        )
        top_storage = p.add_line(
            '{P14}(C) :- {P5}(C), {P8}(C, V), V = #max {{V1 : {P8}(C1, V1), {P5}(C1)}}.'.format(**theme),
            {
                'cnl1': '{P14} is true for the {P5} with the highest {P8}.'.format(**theme),
                'cnl2': '{P14} holds for the {P5} that has the maximum {P8} value.'.format(**theme),
                'cnl3': '{P14} marks the {P5} with the greatest {P8} value.'.format(**theme)
            },
            {
                'nl1': '{P14} marks the {P5} with the highest {P8}.'.format(**theme),
                'nl2': 'The {P5} with the highest {P8} is identified by {P14}.'.format(**theme),
                'nl3': '{P14} is used to indicate which {P5} has the highest {P8}.'.format(**theme),
                'nl4': 'Among all {P5} devices, {P14} highlights the one with the greatest {P8}.'.format(**theme),
                'nl5': '{P14} is true for the {P5} with the highest {P8}.'.format(**theme),
                'nl6': '{P14} identifies the {P5} with the largest {P8} value.'.format(**theme),
                'nl7': 'If a {P5} has the highest {P8}, it is marked by {P14}.'.format(**theme),
                'nl8': 'The {P5} with the maximum {P8} is indicated by {P14}.'.format(**theme),
                'nl9': '{P14} applies to the {P5} with the greatest {P8}.'.format(**theme),
                'nl10': 'Use {P14} to find which {P5} has the highest {P8}.'.format(**theme)
            }
        )
        
        # 1. You may not select all three top-performing components.
        all_top_selected = p.add_line(
            ':- {P2}(C), {P12}(C), {P4}(G), {P13}(G), {P6}(S), {P14}(S).'.format(**theme),
            {
                'cnl1': 'You may not select all three top-performing components.',
                'cnl2': 'It is not allowed to select the top {P1}, {P3}, and {P5} at the same time.'.format(**theme),
                'cnl3': 'Selecting the highest {P1}, {P3}, and {P5} together is forbidden.'.format(**theme)
            },
            {
                'nl1': 'You cannot select the top-performing {P1}, {P3}, and {P5} all at once.'.format(**theme),
                'nl2': 'It is not permitted to choose the best {P1}, {P3}, and {P5} in a single configuration.'.format(**theme),
                'nl3': 'Selecting all three highest-performing components is not allowed.',
                'nl4': 'You must not pick the top {P1}, {P3}, and {P5} together.'.format(**theme),
                'nl5': 'A configuration with all three top-performing parts is invalid.',
                'nl6': 'You are not allowed to select the best {P1}, {P3}, and {P5} at the same time.'.format(**theme),
                'nl7': 'Choosing the highest {P1}, {P3}, and {P5} in one build is forbidden.'.format(**theme),
                'nl8': 'Do not select all three top-performing components in your configuration.',
                'nl9': 'A valid configuration cannot include the best {P1}, {P3}, and {P5} simultaneously.'.format(**theme),
                'nl10': 'You are prohibited from selecting all three top-performing components together.'
            }
        )

        # 2. No selected component can be more than 250 more expensive than another selected component.
        cost_diff_constraint = p.add_line(
            ':- {P9}(C1), {P9}(C2), {P7}(C1, V1), {P7}(C2, V2), V1 - 250 >= V2.'.format(**theme),
            {
                'cnl1': 'No selected component can be more than 250 more expensive than another selected component.',
                'cnl2': 'The cost difference between any two selected components must be less than 250.',
                'cnl3': 'Selected components cannot differ in cost by 250 or more.'
            },
            {
                'nl1': 'No selected part can be more than 250 more expensive than another selected part.',
                'nl2': 'The cost difference between any two selected components must be less than 250.',
                'nl3': 'You cannot select components where one costs 250 or more above another.',
                'nl4': 'Among your selected parts, none can exceed another by 250 in cost.',
                'nl5': 'A valid configuration requires all selected components to be within 250 of each other in cost.',
                'nl6': 'Do not select a component that is 250 or more expensive than another selected one.',
                'nl7': 'The price gap between any two selected parts must be under 250.',
                'nl8': 'You must ensure that no selected component is more than 250 cost units above another.',
                'nl9': 'Configurations with a cost difference of 250 or more between selected parts are invalid.',
                'nl10': 'All selected components must be within 250 cost units of each other.'
            }
        )

        # 3. The GPU must not outperform the CPU.
        gpu_not_better_cpu = p.add_line(
            ':- {P2}(C), {P4}(G), {P8}(C, PC), {P8}(G, PG), PG > PC.'.format(**theme),
            {
                'cnl1': 'The GPU must not outperform the CPU.',
                'cnl2': 'Selected GPU performance cannot exceed selected CPU performance.',
                'cnl3': 'It is not allowed for the GPU to have higher performance than the CPU.'
            },
            {
                'nl1': 'The selected GPU cannot have higher performance than the selected CPU.',
                'nl2': 'Your configuration must not include a GPU that outperforms the CPU.',
                'nl3': 'It is invalid to select a GPU with greater performance than the CPU.',
                'nl4': 'The GPU’s performance must not exceed that of the CPU.',
                'nl5': 'You cannot choose a GPU that is better than the CPU in performance.',
                'nl6': 'A valid configuration requires the CPU to be at least as performant as the GPU.',
                'nl7': 'Do not select a GPU with higher performance than the CPU.',
                'nl8': 'The GPU must not be superior to the CPU in performance.',
                'nl9': 'Configurations where the GPU outperforms the CPU are not allowed.',
                'nl10': 'Ensure the selected GPU does not exceed the CPU in performance.'
            }
        )

        # 4. You cannot select Alpha8 CPU with NovaX GPU.
        alpha8_novax_constraint = p.add_line(
            ':- {P2}("Alpha8"), {P4}("NovaX").'.format(**theme),
            {
                'cnl1': 'You cannot select Alpha8 CPU with NovaX GPU.',
                'cnl2': 'Alpha8 and NovaX cannot be selected together.',
                'cnl3': 'Selecting Alpha8 as CPU and NovaX as GPU is forbidden.'
            },
            {
                'nl1': 'Do not select Alpha8 CPU together with NovaX GPU.',
                'nl2': 'A configuration with Alpha8 and NovaX is not allowed.',
                'nl3': 'You cannot choose Alpha8 as CPU if NovaX is selected as GPU.',
                'nl4': 'Alpha8 and NovaX cannot be part of the same configuration.',
                'nl5': 'Selecting both Alpha8 and NovaX is invalid.',
                'nl6': 'You must not pair Alpha8 CPU with NovaX GPU.',
                'nl7': 'Alpha8 and NovaX are mutually exclusive in your selection.',
                'nl8': 'A valid configuration cannot include both Alpha8 and NovaX.',
                'nl9': 'Do not combine Alpha8 CPU and NovaX GPU in your build.',
                'nl10': 'Alpha8 and NovaX cannot be selected at the same time.'
            }
        )

        # 5. You cannot select FusionDrive storage unless ZetaCore CPU is also selected.
        fusiondrive_requires_zetacore = p.add_line(
            ':- {P6}("FusionDrive"), not {P2}("ZetaCore").'.format(**theme),
            {
                'cnl1': 'FusionDrive storage cannot be selected unless ZetaCore CPU is also selected.',
                'cnl2': 'Selecting FusionDrive requires ZetaCore CPU to be selected.',
                'cnl3': 'You may not select FusionDrive unless ZetaCore is also chosen as CPU.'
            },
            {
                'nl1': 'Do not select FusionDrive storage unless ZetaCore CPU is also selected.',
                'nl2': 'FusionDrive can only be chosen if ZetaCore is also selected as CPU.',
                'nl3': 'You cannot select FusionDrive storage without also selecting ZetaCore CPU.',
                'nl4': 'A valid configuration with FusionDrive must include ZetaCore as CPU.',
                'nl5': 'FusionDrive requires ZetaCore CPU to be part of the configuration.',
                'nl6': 'You must select ZetaCore CPU if you want FusionDrive storage.',
                'nl7': 'FusionDrive is only allowed when ZetaCore is also selected.',
                'nl8': 'Selecting FusionDrive without ZetaCore CPU is not permitted.',
                'nl9': 'You cannot have FusionDrive storage unless ZetaCore is your CPU.',
                'nl10': 'FusionDrive and ZetaCore must be selected together for a valid configuration.'
            }
        )


        p.add_variations(theme['variations'])
        programs.append(p)
    return programs

# CNL/NL levels
cnl_levels = {
    'cnl1': ['cnl1'],
    'cnl2': ['cnl2'],
    'cnl3': ['cnl3'],
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
    'nl1/3': ['nl1/3'],
    'nl2/3': ['nl2/3'],
    'nl3/3': ['nl3/3'],
    'nl4/3': ['nl4/3'],
    'nl5/3': ['nl5/3'],
    'nl6/3': ['nl6/3'],
    'nl7/3': ['nl7/3'],
    'nl8/3': ['nl8/3'],
    'nl9/3': ['nl9/3'],
    'nl10/3': ['nl10/3'],
    'nl1/6': ['nl1/6'],
    'nl2/6': ['nl2/6'],
    'nl3/6': ['nl3/6'],
    'nl4/6': ['nl4/6'],
    'nl5/6': ['nl5/6'],
    'nl6/6': ['nl6/6'],
    'nl7/6': ['nl7/6'],
    'nl8/6': ['nl8/6'],
    'nl9/6': ['nl9/6'],
    'nl10/6': ['nl10/6'],
    'nl1/10': ['nl1/10'],
    'nl2/10': ['nl2/10'],
    'nl3/10': ['nl3/10'],
    'nl4/10': ['nl4/10'],
    'nl5/10': ['nl5/10'],
    'nl6/10': ['nl6/10'],
    'nl7/10': ['nl7/10'],
    'nl8/10': ['nl8/10'],
    'nl9/10': ['nl9/10'],
    'nl10/10': ['nl10/10']
}

programs = generate_programs(theme_sets)

splice_params = {
    'strategy': 'multi_granularity',
    'min_size': 1,
    'max_size': 9,
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

    dg = DataGenerator(p, 'whole')
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
output_cnl_asp = "hard_config_cnl_to_asp_20k.jsonl"
output_nl_cnl = "hard_config_nl_to_cnl_20k.jsonl"

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

print("Hard config modelling complete!")