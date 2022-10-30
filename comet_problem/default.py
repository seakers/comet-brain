


default_problem = {
    'name': 'EPS Design (default)',

    'dataset': {'name': 'Default'},
    'architectures': [],


    'objectives': [
        ('Lifecycle Cost', 'minimize'),
        ('EPS Cost', 'minimize'),
        ('Weighted Design Score', 'maximize'),
        ('EPS Mass', 'minimize'),
        ('Dry Mass', 'minimize'),
    ],

    'parameters': [
        {'name': 'Lifetime', 'units': 'Years', 'type': 'int', 'value': '5'},
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
    ],

    'decisions': [
        {
            'name': 'Orbit',
            'type': 'standard-form',
            'alternatives': [
                {'value': 'LEO-100-DD', 'description': 'empty'},
                {'value': 'LEO-200-DD', 'description': 'empty'},
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
            ]
        },
        {
            'name': 'Battery',
            'type': 'standard-form',
            'alternatives': [
                {'value': 'Saft 8s4o', 'description': 'empty'},
                {'value': 'Saft 11s16p', 'description': 'empty'},
                {'value': 'Saft 4s1p VES16', 'description': 'empty'},
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
                {'value': '-4', 'description': 'empty'},
                {'value': '-3', 'description': 'empty'},
                {'value': '-2', 'description': 'empty'},
                {'value': '-1', 'description': 'empty'},
                {'value': '1', 'description': 'empty'},
                {'value': '2', 'description': 'empty'},
                {'value': '3', 'description': 'empty'},
                {'value': '4', 'description': 'empty'}
            ]
        }
    ]
}




















