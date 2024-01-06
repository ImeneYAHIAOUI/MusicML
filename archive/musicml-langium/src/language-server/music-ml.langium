grammar MusicMl

entry MusicPiece:
	'MusicPiece' name=ID '{'
        ('Author' composer=STRING)?

        globalDirectives=GlobalDirective

        'Tracks'
         tracks+=Track
        (tracks+=Track)*
        '}';

GlobalDirective:
    'GlobalDirective' '{'
    'Tempo' tempo=INT
    'TimeSignature' timeSignature=TimeSignature
    ('midiClocksPerTick' midiClocksPerTick=INT)?
    ('notesPerMidiClock' notesPerMidiClock=INT)?
    '}';

TimeSignature:
     beatsPerBar=INT '/' noteValue=INT;

Track:
    name=ID '{'
    ('startTick' startTick=INT)?
    'instrument' instrument=STRING
    bars+=Bar
    (bars+=Bar)*
    '}';

Bar:
    'Bar' '{'
        ('repeat' repeat=INT)?
        notes+=Note
        (notes+=Note)*
    '}';
Note:
    'Note' '{'
     'duration' duration=INT
     ('startTick' startTick=INT)?
     ('wait' wait=INT)?
    ('channel' channel=INT)?
    ('repeat' repeat=INT)?
    ('sequential' sequence=Boolean)?
    ('velocity' velocity=INT)?
     noteValue=( NormalNote | DrumNote )
    '}';




terminal Boolean:
    'true' | 'false';

NormalNote:
    pitches+=Pitch
    (pitches+=Pitch)*;

DrumNote:
    'DrumSounds' 
    notes+=DrumType
    (notes+=DrumType)*;

Pitch:
    'Pitch' '{'
    'octave' octave=INT
    'value' value=NoteValue (accidental=Accidental)?
    '}';

terminal Accidental:
    'sharp' | 'flat';

terminal NoteValue:
    'do'  | 'do' | 're' | 're' | 'mi' | 'fa' | 'fa' | 'sol' | 'sol' | 'la' | 'la' | 'si';
terminal DrumType:
    'bd' | 'sd' | 'ch' | 'oh' | 'cc' | 'rc';

hidden terminal WS: /\s+/;
terminal ID: /[_a-zA-Z][\w_]*/;
terminal INT returns number: /[0-9]+/;
terminal STRING: /"[^"]*"|'[^']*'/;
terminal CHAR: /'.'/;

hidden terminal ML_COMMENT: /\/\*[\s\S]*?\*\//;
hidden terminal SL_COMMENT: /\/\/[^\n\r]*/;
