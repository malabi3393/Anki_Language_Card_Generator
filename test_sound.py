import genanki

swe_list = ['jag', 'lyssna', 'test', 'example', 'a', 'list']
eng_list = ['I', 'listen']


my_model = genanki.Model(
  1380120064,
  'Example',
  fields=[
    {'name': 'English'},
    {'name': 'English'},
    {'name': 'Swedish_Audio'}
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{English}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{English}}{{Swedish_Audio}}',
    },
  ])

my_deck = genanki.Deck(
2059400191,
'Example')
for i in range(len(swe_list)):
    my_note = genanki.Note(
    model=my_model,
    fields=[swe_list[i], '[sound:sound.mp3]'])
    my_deck.add_note(my_note)

my_package = genanki.Package(my_deck)
my_package.media_files = ['sound.mp3']

my_package.write_to_file('working_sound.apkg')