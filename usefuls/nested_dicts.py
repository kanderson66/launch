cats = {
    'Pete': {
        'Cheddar': {
            'color': 'orange',
            'enjoys': [
                'sleeping',
                'snuggling',
                'meowing',
                'eating',
                'birdwatching',
            ],
        },
        'Cocoa': {
            'color': 'black',
            'enjoys': [
                'eating',
                'sleeping',
                'playing',
                'chewing',
            ],
        },
    },
}
print(cats['Pete']['Cocoa']['enjoys'])
# {'eating', 'chewing', 'playing', 'sleeping'}


deck = [
    { 'suit': 'Clubs', 'value': '2' },
    { 'suit': 'Clubs', 'value': '3' },
    { 'suit': 'Clubs', 'value': '4' },
    { 'suit': 'Spades', 'value': 'Queen' },
    { 'suit': 'Spades', 'value': 'King' },
    { 'suit': 'Spades', 'value': 'Ace' },
]
print(f"{deck[3]['value']} of {deck[3]['suit']}")
# Queen of Spades