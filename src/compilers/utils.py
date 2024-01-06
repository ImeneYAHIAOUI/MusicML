from textx import *
from constants import *


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


def note_to_midi(note_string):
    note = ''.join(char for char in note_string if char.isalpha() or char in ('#', 'b')).upper()
    octave = int(''.join(char for char in note_string if char.isdigit()))
    if note not in note_to_midi_number1 and note not in note_to_midi_number2:
        return None
    if note in note_to_midi_number1:
        return 12 * (octave + 1) + note_to_midi_number1[note]
    else:
        return 12 * (octave + 1) + note_to_midi_number2[note]


def get_control_message_number(name):
    if name.lower() in control_messages:
        return control_messages[name.lower()]
    else:
        return None


def duration_to_ticks(duration, ticks_per_quarternote):
    if duration.value != 0:
        return duration.value
    elif duration.fraction is not None:
        num = duration.fraction.numerator
        den = duration.fraction.denominator
        return int((num / den) * 4 * ticks_per_quarternote)

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
    position_in_ticks = default_position_in_ticks
    for ts in music_ml_model.timeSignatures:
        if bar_number < ts.bar:
            break
        else:
            # Bar is beyond this time signature, move to the next
            position_in_ticks = ticks_per_bar * ts.bar
            beats_per_bar = ts.numerator
            ticks_per_bar = ticks_per_quarternote * (4 / ts.denominator) * beats_per_bar
            position_in_ticks += ticks_per_bar * (bar_number - ts.bar)

    return int(position_in_ticks) 


def get_original_bar(music_ml_meta, track, bar):
    original_bar = None
    for b in track.bars:
        if textx_isinstance(b, music_ml_meta['Bar']) and b.name == bar.ref:
            original_bar = b
            break
    if original_bar is None:
        raise TextXSemanticError('Reused bar not found: ' + bar.name, **get_location(bar.name))
    return original_bar


def get_original_region(music_ml_meta, track, region):
    original_region = None
    for r in track.midiRegions:
        if textx_isinstance(r, music_ml_meta['Region']) and r.name == region.ref:
            original_region = r
            break
    if original_region is None:
        raise TextXSemanticError('Reused region not found: ' + region.name, **get_location(region.name))
    return original_region


def calculate_music_events_length(midi_file, music_ml_meta, music_events):
    ticks_per_quarternote = midi_file.ticks_per_quarternote
    total_duration = 0
    smallest_start_time = float('inf')
    for music_event in music_events:
        if textx_isinstance(music_event, music_ml_meta['Note']):
            if textx_isinstance(music_event, music_ml_meta['Chord']):
                nested_chord_duration = calculate_chord_length(music_event, midi_file, music_ml_meta)
                repeat = music_event.repeat
                if repeat == 0:
                    repeat = 1
                total_duration = max(total_duration, nested_chord_duration * (repeat - 1))
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


def calculate_event_start_time(midi_file, music_ml_meta, music_event):
    ticks_per_quarternote = midi_file.ticks_per_quarternote

    if textx_isinstance(music_event, music_ml_meta['SimpleNote']) or textx_isinstance(music_event,
                                                                                      music_ml_meta['Rest']):
        return 0 if music_event.start is None else duration_to_ticks(music_event.start, ticks_per_quarternote)

    elif textx_isinstance(music_event, music_ml_meta['Chord']):
        smallest_start_time = float('inf')
        for note in music_event.notes:
            if textx_isinstance(note, music_ml_meta['SimpleNote']):
                start_time = 0 if note.start is None else duration_to_ticks(note.start, ticks_per_quarternote)
                smallest_start_time = min(smallest_start_time, start_time)
            else:
                start_time = calculate_event_start_time(midi_file, music_ml_meta, note)
                smallest_start_time = min(smallest_start_time, start_time)
        return smallest_start_time
