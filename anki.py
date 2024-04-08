import genanki
import pandas as pd


data = pd.read_csv("deck.csv")
df = pd.DataFrame(data)
eng = df['0'].tolist()
sw = df['1'].tolist()

#--
sound_deck= genanki.Deck(
2059400210,
'Anki sound deck')

my_package = genanki.Package(sound_deck)
my_package.media_files = ['sound.mp3', 'test.png']

my_model = genanki.Model(
  1091765104,
  'Basic and reversed ',
  fields=[
    {'name': 'English'},
    {'name': 'Swedish'}                                  # ADD THIS
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{English}}<br>',              # AND THIS
      'afmt': '{{FrontSide}}<hr id="answer">{{Swedish}}',
    },
  ])

a_note = genanki.Note(
    model = my_model,
    fields = ['I', 'Jag <img src="test.png">'] )
sound_deck.add_note(a_note)
p = genanki.Package(sound_deck).write_to_file('sound.apkg')

#--------------------------------------

my_deck = genanki.Deck(
2059400110,
'Twisted Love Chapter 1')

for e, s in zip(eng, sw):
    my_note = genanki.Note(
        model = genanki.BASIC_AND_REVERSED_CARD_MODEL,
        fields=[e, s])
    my_deck.add_note(my_note)

genanki.Package(my_deck).write_to_file('output.apkg')

