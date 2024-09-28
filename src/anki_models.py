import genanki 
my_model_1 = genanki.Model(
3429,
'Example',
fields=[
    {'name': 'Native Language'},
    {'name': 'Target'},
    {'name': 'Target_Audio'}
],
templates=[
    {
    'name': 'Card 1',
    'qfmt': '<span style="font-size: 40px;">{{Native Language}}',
    'afmt': '<span style="font-size: 40px;">{{FrontSide}}<hr id="answer">{{Target}}<br>{{Target_Audio}}',
    },
])

my_model_reversed = genanki.Model(
3430,
'Reversed',
fields=[
    {'name': 'Target'},
    {'name': 'Target_Audio'},
    {'name': 'Native Language'}
],
templates=[
    {
    'name': 'Card 1',
    'qfmt': '<span style="font-size: 40px;">{{Target}} <br> {{Target_Audio}}',
    'afmt': '<span style="font-size: 40px;">{{FrontSide}}<hr id="answer">{{Native Language}}',
    },
])