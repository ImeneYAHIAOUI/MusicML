#!/usr/bin/env python3

from midiutil import MIDIFile
from textx import *


def note_to_midi(note_string):
    note = ''.join(char for char in note_string if char.isalpha() or char in ('#', 'b'))
    octave = int(''.join(char for char in note_string if char.isdigit()))
    note_to_midi_number1 = {'DO': 0, 'DO#': 1, 'REb': 1, 'RE': 2, 'RE#': 3, 'MIb': 3, 'MI': 4, 'FA': 5, 'FA#': 6,
                            'SOLb': 6, 'SOL': 7,
                            'SOL#': 8, 'LAb': 8, 'LA': 9,
                            'LA#': 10, 'SIb': 10, 'SI': 11}
    note_to_midi_number2 = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6,
                            'G': 7,
                            'G#': 8, 'Ab': 8, 'A': 9,
                            'A#': 10, 'Bb': 10, 'B': 11}
    if note not in note_to_midi_number1 and note not in note_to_midi_number2:
        return None
    if note in note_to_midi_number1:
        return 12 * (octave + 1) + note_to_midi_number1[note]
    else:
        return 12 * (octave + 1) + note_to_midi_number2[note]


instrument_to_program_number = {
    'Acoustic Grand Piano': 1,
    'Piano': 1,
    'Bright Acoustic Piano': 2,
    'Piano 2': 2,
    'Electric Grand Piano': 3,
    'Piano 3': 3,
    'Honky-tonk Piano': 4,
    'Electric Piano 1': 5,
    'Electric Piano 2': 6,
    'Harpsichord': 7,
    'Clavinet': 8,
    'Celesta': 9,
    'Glockenspiel': 10,
    'Music Box': 11,
    'Vibraphone': 12,
    'Marimba': 13,
    'Xylophone': 14,
    'Tubular Bells': 15,
    'Dulcimer': 16,
    'Drawbar Organ': 17,
    'Percussive Organ': 18,
    'Rock Organ': 19,
    'Church Organ': 20,
    'Reed Organ': 21,
    'Accordion': 22,
    'Harmonica': 23,
    'Tango Accordion': 24,
    'Acoustic Guitar (nylon)': 25,
    'Guitar': 25,
    'Acoustic Guitar (steel)': 26,
    'Electric Guitar (jazz)': 27,
    'Electric Guitar (clean)': 28,
    'Electric Guitar (muted)': 29,
    'Overdriven Guitar': 30,
    'Distortion Guitar': 31,
    'Guitar Harmonics': 32,
    'Acoustic Bass': 33,
    'Bass': 33,
    'Electric Bass (finger)': 34,
    'Electric Bass (pick)': 35,
    'Fretless Bass': 36,
    'Slap Bass 1': 37,
    'Slap Bass 2': 38,
    'Synth Bass 1': 39,
    'Synth Bass 2': 40,
    'Violin': 41,
    'Viola': 42,
    'Cello': 43,
    'Contrabass': 44,
    'Tremolo Strings': 45,
    'Pizzicato Strings': 46,
    'Orchestral Harp': 47,
    'Timpani': 48,
    'String Ensemble 1': 49,
    'String Ensemble 2': 50,
    'SynthStrings 1': 51,
    'SynthStrings 2': 52,
    'Choir Aahs': 53,
    'Voice': 53,
    'Synth Voice': 54,
    'Orchestra Hit': 55,
    'Trumpet': 56,
    'Trombone': 57,
    'Tuba': 58,
    'Muted Trumpet': 59,
    'French Horn': 60,
    'Brass Section': 61,
    'SynthBrass 1': 62,
    'SynthBrass 2': 63,
    'Soprano Sax': 64,
    'Alto Sax': 65,
    'Tenor Sax': 66,
    'Baritone Sax': 67,
    'Oboe': 68,
    'English Horn': 69,
    'Bassoon': 70,
    'Clarinet': 71,
    'Piccolo': 72,
    'Flute': 73,
    'Recorder': 74,
    'Pan Flute': 75,
    'Blown Bottle': 76,
    'Shakuhachi': 77,
    'Whistle': 78,
    'Ocarina': 79,
    'Lead 1 (square)': 80,
    'Lead 2 (sawtooth)': 81,
    'Lead 3 (calliope)': 82,
    'Lead 4 (chiff)': 83,
    'Lead 5 (charang)': 84,
    'Lead 6 (voice)': 85,
    'Lead 7 (fifths)': 86,
    'Lead 8 (bass + lead)': 87,
    'Pad 1 (new age)': 88,
    'Pad 2 (warm)': 89,
    'Pad 3 (polysynth)': 90,
    'Pad 4 (choir)': 91,
    'Pad 5 (bowed)': 92,
    'Pad 6 (metallic)': 93,
    'Pad 7 (halo)': 94,
    'Pad 8 (sweep)': 95,
    'FX 1 (rain)': 96,
    'FX 2 (soundtrack)': 97,
    'FX 3 (crystal)': 98,
    'FX 4 (atmosphere)': 99,
    'FX 5 (brightness)': 100,
    'FX 6 (goblins)': 101,
    'FX 7 (echoes)': 102,
    'FX 8 (sci-fi)': 103,
    'Sitar': 104,
    'Banjo': 105,
    'Shamisen': 106,
    'Koto': 107,
    'Kalimba': 108,
    'Bagpipe': 109,
    'Fiddle': 110,
    'Shanai': 111,
    'Tinkle Bell': 112,
    'Agogo': 113,
    'Steel Drums': 114,
    'Woodblock': 115,
    'Taiko Drum': 116,
    'Melodic Tom': 117,
    'Synth Drum': 118,
    'Reverse Cymbal': 119,
    'Guitar Fret Noise': 120,
    'Breath Noise': 121,
    'Seashore': 122,
    'Bird Tweet': 123,
    'Telephone Ring': 124,
    'Helicopter': 125,
    'Applause': 126,
    'Gunshot': 127,
}

percussion_instrument_to_program_number = {
    'Acoustic Bass Drum': 35,
    'Bass Drum 1': 36,
    'Side Stick': 37,
    'Acoustic Snare': 38,
    'Hand Clap': 39,
    'Electric Snare': 40,
    'Low Floor Tom': 41,
    'Closed Hi-Hat': 42,
    'High Floor Tom': 43,
    'Pedal Hi-Hat': 44,
    'Low Tom': 45,
    'Open Hi-Hat': 46,
    'Low-Mid Tom': 47,
    'Hi-Mid Tom': 48,
    'Crash Cymbal 1': 49,
    'High Tom': 50,
    'Ride Cymbal 1': 51,
    'Chinese Cymbal': 52,
    'Ride Bell': 53,
    'Tambourine': 54,
    'Splash Cymbal': 55,
    'Cowbell': 56,
    'Crash Cymbal 2': 57,
    'Vibraslap': 58,
    'Ride Cymbal 2': 59,
    'Hi Bongo': 60,
    'Low Bongo': 61,
    'Mute Hi Conga': 62,
    'Open Hi Conga': 63,
    'Low Conga': 64,
    'High Timbale': 65,
    'Low Timbale': 66,
    'High Agogo': 67,
    'Low Agogo': 68,
    'Cabasa': 69,
    'Maracas': 70,
    'Short Whistle': 71,
    'Long Whistle': 72,
    'Short Guiro': 73,
    'Long Guiro': 74,
    'Claves': 75,
    'Hi Wood Block': 76,
    'Low Wood Block': 77,
    'Mute Cuica': 78,
    'Open Cuica': 79,
    'Mute Triangle': 80,
    'Open Triangle': 81,
}

midi_durations = {
    'whole': 4,
    '1/2 dotted': 3,
    'triplet': 2 / 3,
    '1/2': 2,
    '1/4 dotted': 1.5,
    '1/2 triplet': 4 / 3,
    '1/4': 1,
    '1/8 dotted': 0.75,
    '1/4 triplet': 2 / 3,
    '1/8': 0.5,
    '1/16 dotted': 0.375,
    '1/8 triplet': 1 / 3,
    '1/16': 0.25,
    '1/32 dotted': 0.1875,
    '1/16 triplet': 1 / 6,
    '1/32': 0.125,
    '1/64 dotted': 0.09375,
    '1/32 triplet': 1 / 12,
    '1/64': 0.0625,
    '1/128 dotted': 0.046875,
    '1/64 triplet': 1 / 24,
    '1/128': 0.03125,
}


def duration_to_ticks(duration, ticks_per_quarternote):
    if duration.value != 0:
        return duration.value
    else:
        return int(midi_durations[duration.durationValue] * ticks_per_quarternote)


def instrument_program_number(instrument):
    if instrument in instrument_to_program_number:
        return instrument_to_program_number[instrument]
    elif instrument in percussion_instrument_to_program_number:
        return percussion_instrument_to_program_number[instrument]
    else:
        return None


def default_channel(instrument):
    if instrument in percussion_instrument_to_program_number:
        return 9
    else:
        return 1


def bar_position_in_ticks(music_ml_model, midi_file, bar_number):
    ticks_per_quarternote = midi_file.ticks_per_quarternote
    time_signature = music_ml_model.defaultTimeSignature
    numerator = time_signature.numerator
    beats_per_bar = numerator
    ticks_per_bar = (ticks_per_quarternote * beats_per_bar)
    default_position_in_ticks = ticks_per_bar * bar_number
    if len(music_ml_model.timeSignatures) == 0:
        return int(default_position_in_ticks)
    position_in_ticks = 0
    for ts in music_ml_model.timeSignatures:
        if position_in_ticks + ticks_per_bar >= bar_number * ticks_per_bar:
            position_in_ticks += bar_number * ticks_per_bar
            break
        else:
            # Bar is beyond this time signature, move to the next
            position_in_ticks += ts.position
            numerator = ts.numerator
            denominator = ts.denominator
            beats_per_bar = numerator
            ticks_per_bar = ticks_per_quarternote * (4 / denominator) * beats_per_bar

    return int(position_in_ticks)


def generate_midi_file(music_ml_meta, music_ml_model, ml_file_name):
    # Create the MIDIFile Object
    track_number = len(music_ml_model.tracks)
    if music_ml_model.ticksPerQuarterNote != 0:
        midi_file = MIDIFile(track_number, eventtime_is_ticks=True,
                             ticks_per_quarternote=music_ml_model.ticksPerQuarterNote)
    else:
        midi_file = MIDIFile(track_number, eventtime_is_ticks=True)
    for i, track in enumerate(music_ml_model.tracks):
        midi_file.addTempo(i, 0, music_ml_model.defaultTempo)
        for tempo in music_ml_model.tempos:
            midi_file.addTempo(i, tempo.position, tempo.tempo)
        midi_file.addTimeSignature(i, 0, music_ml_model.defaultTimeSignature.numerator,
                                   music_ml_model.defaultTimeSignature.denominator, 24, 8)
        for time_signature in music_ml_model.timeSignatures:
            midi_file.addTimeSignature(i, time_signature.position, time_signature.numerator,
                                       time_signature.denominator, 24, 8)
        compile_track(music_ml_model, music_ml_meta, track, midi_file, i)
    bin_file = open(ml_file_name + '.mid', 'wb')
    midi_file.writeFile(bin_file)
    bin_file.close()


def compile_track(music_ml_model, music_ml_meta, track, midi_file, track_number):
    midi_file.addTrackName(track_number, 0, track.name)
    program_number = instrument_program_number(track.instrument)
    if program_number is None:
        raise TextXSemanticError('Instrument not found: ' + track.instrument, **get_location(track))
    channel = default_channel(track.instrument)
    velocity = 50
    if track.channel != 0:
        channel = track.channel
    if track.velocity != 0:
        velocity = track.velocity
    midi_file.addProgramChange(track_number, channel, 0, program_number)
    i = 0
    for bar in track.bars:
        compile_bar(music_ml_model, music_ml_meta, bar, i, midi_file, track, track_number, channel, velocity)
        if textx_isinstance(bar, music_ml_meta['Bar']):
            i += 1
        if textx_isinstance(bar, music_ml_meta['EmptyBar'] or textx_isinstance(bar, music_ml_meta['ReusedBar'])):
            repeat = bar.times
            if repeat == 0:
                repeat = 1
            i += repeat


def compile_bar(music_ml_model, music_ml_meta, bar, i, midi_file, track, track_number, channel, velocity):
    if textx_isinstance(bar, music_ml_meta['Bar'] or textx_isinstance(bar, music_ml_meta['ReusedBar'])):

        if textx_isinstance(bar, music_ml_meta['ReusedBar']):
            original_bar = get_original_bar(music_ml_meta, track, bar)
            music_events = original_bar.music_events + bar.music_events
        else:
            music_events = bar.musicalEvents
        ticks_in_bar = bar_position_in_ticks(music_ml_model, midi_file, i + 1) - bar_position_in_ticks(music_ml_model, midi_file, i)
        music_events_length = calculate_music_events_length(midi_file, music_ml_meta, music_events)
        if music_events_length > ticks_in_bar:
            raise TextXSemanticError('Bar is overflown, split into multiple bars', **get_location(bar))

    if not textx_isinstance(bar, music_ml_meta['EmptyBar']):
        if bar.velocity != 0:
            velocity = bar.velocity
        for music_event in bar.musicalEvents:
            compile_music_event(music_ml_model, music_ml_meta, music_event, i, midi_file, track_number, channel,
                                velocity)
    position = i
    if textx_isinstance(bar, music_ml_meta['ReusedBar']):
        original_bar = get_original_bar(music_ml_meta, track, bar)
        repeat = bar.times
        if repeat == 0:
            repeat = 1
        for i in range(repeat):
            for music_event in original_bar.musicalEvents:
                compile_music_event(music_ml_model, music_ml_meta, music_event, position, midi_file, track_number,
                                    channel, velocity)
            position += 1


def get_original_bar(music_ml_meta, track, bar):
    original_bar = None
    for b in track.bars:
        if textx_isinstance(b, music_ml_meta['Bar']) and b.name == bar.ref:
            original_bar = b
            break
    if original_bar is None:
        raise TextXSemanticError('Reused bar not found: ' + bar.name, **get_location(bar.name))
    return original_bar


def compile_music_event(music_ml_model, music_ml_meta, music_event, position, midi_file, track_number, channel,
                        velocity):
    if textx_isinstance(music_event, music_ml_meta['Note']):
        compile_note_event(music_ml_model, music_ml_meta, music_event, position, midi_file, track_number, channel,
                           velocity)
    else:
        compile_rest_event(music_ml_model, music_event, position, midi_file, track_number, channel)


def compile_note_event(music_ml_model, music_ml_meta, note, position, midi_file, track_number, channel, velocity):
    if textx_isinstance(note, music_ml_meta['SimpleNote']):
        compile_simple_note_event(music_ml_model, note, position, midi_file, track_number, channel, velocity)
    else:
        compile_chord_event(music_ml_model, music_ml_meta, note, position, midi_file, track_number, channel, velocity)


def compile_simple_note_event(music_ml_model, note, position, midi_file, track_number, channel, velocity,
                              ticks_to_add=0):
    duration = duration_to_ticks(note.duration, midi_file.ticks_per_quarternote)
    if note.velocity != 0:
        velocity = note.velocity

    for note_value in note.values:
        position_in_ticks = bar_position_in_ticks(music_ml_model, midi_file, position) + ticks_to_add
        value = note_to_midi(note_value)
        if value is None:
            raise TextXSemanticError('Note not supported: ' + note.Value, **get_location(note.Value))
        if note.start is not None:
            position_in_ticks += duration_to_ticks(note.start, midi_file.ticks_per_quarternote)
        midi_file.addNote(track_number, channel, value, position_in_ticks, duration, velocity)


def compile_rest_event(music_ml_model, rest, position, midi_file, track_number, channel):
    duration = duration_to_ticks(rest.duration, midi_file.ticks_per_quarternote)

    position_in_ticks = bar_position_in_ticks(music_ml_model, midi_file, position)
    if rest.start is not None:
        position_in_ticks += duration_to_ticks(rest.start, midi_file.ticks_per_quarternote)
    midi_file.addNote(track_number, channel, 60, position_in_ticks, duration, 0)


def compile_chord_event(music_ml_model, music_ml_meta, chord, position, midi_file, track_number, channel,
                        velocity,
                        ticks_to_add=0):
    if chord.velocity != 0:
        velocity = chord.velocity
    repeat = chord.repeat
    if repeat == 0:
        repeat = 1
    duration = calculate_chord_length(chord, midi_file, music_ml_meta)
    for i in range(repeat):
        for note in chord.notes:
            if textx_isinstance(note, music_ml_meta['SimpleNote']):
                compile_simple_note_event(music_ml_model, note, position, midi_file, track_number, channel,
                                          velocity,
                                          ticks_to_add)
            else:
                compile_chord_event(music_ml_model, music_ml_meta, note, position, midi_file, track_number, channel,
                                    velocity,
                                    ticks_to_add)
        ticks_to_add += duration


def calculate_chord_length(chord, midi_file, music_ml_meta):
    ticks_per_quarternote = midi_file.ticks_per_quarternote
    total_duration = 0
    smallest_start_time = float('inf')

    for note in chord.notes:
        if textx_isinstance(note, music_ml_meta['Chord']):
            # Recursively calculate the duration for nested chords
            nested_chord_duration = calculate_chord_length(note, midi_file, music_ml_meta)
            total_duration = max(total_duration, nested_chord_duration)
        elif textx_isinstance(note, music_ml_meta['SimpleNote']):
            duration = duration_to_ticks(note.duration, ticks_per_quarternote)
            start_time = 0 if note.start is None else duration_to_ticks(note.start, ticks_per_quarternote)
            smallest_start_time = min(smallest_start_time, start_time)
            note_end_time = start_time + duration
            total_duration = max(total_duration, note_end_time)

    return total_duration - smallest_start_time


def calculate_music_events_length(midi_file, music_ml_meta, music_events):
    ticks_per_quarternote = midi_file.ticks_per_quarternote
    total_duration = 0
    smallest_start_time = float('inf')

    for music_event in music_events:
        if textx_isinstance(music_event, music_ml_meta['Note']):
            if textx_isinstance(music_event, music_ml_meta['Chord']):
                nested_chord_duration = calculate_chord_length(music_event, midi_file, music_ml_meta)
                total_duration = max(total_duration, nested_chord_duration)
            else:
                duration = duration_to_ticks(music_event.duration, ticks_per_quarternote)
                start_time = 0 if music_event.start is None else duration_to_ticks(music_event.start,
                                                                                   ticks_per_quarternote)
                smallest_start_time = min(smallest_start_time, start_time)
                note_end_time = start_time + duration
                total_duration = max(total_duration, note_end_time)
        elif textx_isinstance(music_event, music_ml_meta['Rest']):
            duration = duration_to_ticks(music_event.duration, ticks_per_quarternote)
            start_time = 0 if music_event.start is None else duration_to_ticks(music_event.start, ticks_per_quarternote)
            smallest_start_time = min(smallest_start_time, start_time)
            note_end_time = start_time + duration
            total_duration = max(total_duration, note_end_time)
    return total_duration - smallest_start_time
