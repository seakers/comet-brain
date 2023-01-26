




default_problem = {
    'name': 'EPS Design (default)',
    'dataset': {'name': 'Default'},
    'architectures': [],


    'objectives': [
        {'name': 'Lifecycle Cost', 'type': 'continuous', 'optimization': 'min', 'bounds': '[0, 10000000]'},
        {'name': 'EPS Cost', 'type': 'continuous', 'optimization': 'min', 'bounds': '[0, 10000000]'},
        {'name': 'Weighted Design Score', 'type': 'continuous', 'optimization': 'max', 'bounds': '[0, 10]'},
        {'name': 'EPS Mass', 'type': 'continuous', 'optimization': 'min', 'bounds': '[0, 100000]'},
        {'name': 'Dry Mass', 'type': 'continuous', 'optimization': 'min', 'bounds': '[0, 100000]'}
    ],

    'parameters': [
        {'name': 'Lifetime', 'units': 'Years', 'type': 'int', 'value': '5'},
        {'name': 'Delta-V', 'units': 'm/s', 'type': 'int', 'value': '70'},
        {'name': 'Payload Power', 'units': 'Watts', 'type': 'int', 'value': '814'},
        {'name': 'Payload Peak Power', 'units': 'Watts', 'type': 'int', 'value': '864'},
        {'name': 'Bus Power', 'units': 'Watts', 'type': 'int', 'value': '1085'},
        {'name': 'Payload Mass', 'units': 'Kg', 'type': 'int', 'value': '552'},
        {'name': 'Payload Dimension', 'units': 'M', 'type': 'float-list', 'value': '[.9, .9, 1]'},
        {'name': 'Inclination', 'units': 'Deg', 'type': 'int', 'value': '10'},
        {'name': 'RAAN', 'units': 'Deg', 'type': 'int', 'value': '180'},
        {'name': 'Spacecraft Dimensions', 'units': 'M', 'type': 'int-list', 'value': '[2, 2, 2]'},
        {'name': 'Link Data Volume', 'units': 'Gb/Day', 'type': 'int', 'value': '550'},
        {'name': 'Link Datarate', 'units': 'Mbps', 'type': 'int', 'value': '700'},
        {'name': 'Pointing Requirement', 'units': 'degrees', 'type': 'float', 'value': '0.004166'},
        {'name': 'Pointing Off Nadir', 'units': 'degrees', 'type': 'float-list', 'value': '[35.0, 0.0]'},
    ],

    'decisions': [
        {
            'name': 'Orbit',
            'type': 'standard-form',
            'alternatives': [
                {'value': 'LEO-400-DD', 'description': 'empty'},
                {'value': 'LEO-500-DD', 'description': 'empty'},
                {'value': 'MEO-1000-DD', 'description': 'empty'},
            ]
        },
        {
            'name': 'Solar Array',
            'type': 'standard-form',
            'alternatives': [
                {'value': 'XTE-SF', 'description': 'empty'},
                {'value': 'XTE-LILT', 'description': 'empty'},
                {'value': 'XTE-HF', 'description': 'empty'},
                {'value': 'XTJ-CIC', 'description': 'empty'},
                {'value': 'UTJ-CIC', 'description': 'empty'},
                {'value': 'XTJ-Prime', 'description': 'empty'},
                {'value': 'Azur 3G30C', 'description': 'empty'},
            ]
        },
        {
            'name': 'Battery',
            'type': 'standard-form',
            'alternatives': [
                {'value': 'Saft 8s4p', 'description': 'empty'},
                {'value': 'Saft 11s16p', 'description': 'empty'},
                {'value': 'Saft 4s1p VES16', 'description': 'empty'},
                {'value': 'EaglePicher SAR-10197', 'description': 'empty'},
                {'value': 'EaglePicher SAR-10199', 'description': 'empty'},
                {'value': 'EaglePicher SAR-10207', 'description': 'empty'},
                {'value': 'EaglePicher SAR-10215', 'description': 'empty'}
            ]
        },
        {
            'name': 'Number of Panels',
            'type': 'standard-form',
            'alternatives': [
                {'value': '1', 'description': 'empty'},
                {'value': '2', 'description': 'empty'},
                {'value': '3', 'description': 'empty'},
                {'value': '4', 'description': 'empty'},
                {'value': '5', 'description': 'empty'},
                {'value': '6', 'description': 'empty'},
            ]
        },
        {       
            'name': 'Solar Array Degrees of Freedom',
            'type': 'standard-form',
            'alternatives': [
                {'value': '1', 'description': 'empty'},
                {'value': '2', 'description': 'empty'},
                {'value': '3', 'description': 'empty'},
            ]
        },
        {
            'name': 'Solar Array Normal Direction',
            'type': 'standard-form',
            'alternatives': [
                {'value': '-3', 'description': 'empty'},
                {'value': '-2', 'description': 'empty'},
                {'value': '-1', 'description': 'empty'},
                {'value': '1', 'description': 'empty'},
                {'value': '2', 'description': 'empty'},
                {'value': '3', 'description': 'empty'}
            ]
        }
    ]
}




















