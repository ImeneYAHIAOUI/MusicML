from textx import *
from constants import *


def calculate_chord_length(music_ml_model, chord, midi_file, music_ml_meta, bar_number):
    ticks_per_quarternote = midi_file.ticks_per_quarternote
    total_duration = 0
    smallest_start_time = float('inf')

    for note in chord.notes:
        duration, start_time = get_not_position_and_duration(music_ml_meta, bar_number, note, music_ml_model,
                                                             ticks_per_quarternote)
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


def midi_time_to_ticks(music_ml_model, music_ml_meta, midi_time, ticks_per_quarternote, bar_number):
    if textx_isinstance(midi_time, music_ml_meta['Tick']):
        return int(midi_time.value)
    elif textx_isinstance(midi_time, music_ml_meta['BeatFraction']):
        denominator = midi_time.denominator
        numerator = midi_time.numerator
        if denominator == 0:
            raise TextXSemanticError('Invalid beat fraction, denominator cannot be 0', **get_location(midi_time))
        ticks_per_beat = ticks_in_beat(music_ml_model, ticks_per_quarternote, bar_number)
        return int((numerator / denominator) * ticks_per_beat)


def midi_duration_to_ticks(music_ml_meta, music_ml_model, duration, ticks_per_quarternote, bar_number):
    if textx_isinstance(duration, music_ml_meta['Tick']):
        return duration.value
    elif textx_isinstance(duration, music_ml_meta['BeatFraction']):
        num = duration.fraction.numerator
        den = duration.fraction.denominator
        return int((num / den) * 4 * ticks_per_quarternote)
    try:
        if duration.predefined is not None:
            return int(midi_durations[duration.predefined] * ticks_per_quarternote)
        if duration.userDefined is not None:
            return midi_time_to_ticks(music_ml_model, music_ml_meta, duration.userDefined, ticks_per_quarternote,
                                      bar_number)
    except KeyError:
        raise TextXSemanticError(
            'Invalid duration value, it must respect one of the following patterns : T(INT), F(INT/INT) or (MidiDuration)',
            **get_location(duration))


def instrument_program_number(instrument):
    if instrument in instrument_to_program_number:
        return instrument_to_program_number[instrument]
    elif instrument in percussion_instrument_to_program_number:
        return percussion_instrument_to_program_number[instrument]
    else:
        return None


def default_channel(instrument):
    if instrument in percussion_instrument_to_program_number:
        return 10
    else:
        return 1


def bar_position_in_ticks(music_ml_model, midi_file, bar_number):
    ticks_per_quarternote = midi_file.ticks_per_quarternote
    time_signature = music_ml_model.defaultTimeSignature
    beats_per_bar = time_signature.numerator
    beat_value = time_signature.denominator
    ticks_per_bar = ticks_per_quarternote * (4 / beat_value) * beats_per_bar
    default_position_in_ticks = ticks_per_bar * bar_number
    if len(music_ml_model.timeSignatures) == 0:
        return int(default_position_in_ticks)
    ticks = default_position_in_ticks
    for ts in music_ml_model.timeSignatures:
        if bar_number < ts.bar:
            break
        else:
            ticks = ticks_per_bar * ts.bar
            beats_per_bar = ts.numerator
            beat_value = ts.denominator
            ticks_per_bar = ticks_per_quarternote * (4 / beat_value) * beats_per_bar
            ticks += ticks_per_bar * (bar_number - ts.bar)

    return int(ticks)


def position_in_ticks(music_ml_model, music_ml_meta, midi_file, position):
    tick_position = bar_position_in_ticks(music_ml_model, midi_file, position.bar)
    ticks_per_quarternote = midi_file.ticks_per_quarternote
    ticks_per_beat = ticks_in_beat(music_ml_model, ticks_per_quarternote, position.bar)
    tick_position += ticks_per_beat * (position.beat - 1)
    tick_position += midi_time_to_ticks(music_ml_model, music_ml_meta, position.offset, ticks_per_quarternote,
                                        position.bar)
    return tick_position


def ticks_in_beat(music_ml_model, ticks_per_quarternote, bar_number):
    time_signature = music_ml_model.defaultTimeSignature
    beat_value = time_signature.denominator
    ticks_per_beat = ticks_per_quarternote * (4 / beat_value)
    for ts in music_ml_model.timeSignatures:
        if bar_number < ts.bar:
            break
        else:
            beat_value = ts.denominator
            ticks_per_beat = ticks_per_quarternote * (4 / beat_value)
    return ticks_per_beat


def current_time_signature(music_ml_model, bar_number):
    time_signature = music_ml_model.defaultTimeSignature
    for ts in music_ml_model.timeSignatures:
        if bar_number < ts.bar:
            break
        else:
            time_signature = ts
    return time_signature


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



def get_not_position_and_duration(music_ml_meta, bar_number, music_event, music_ml_model,
                                  ticks_per_quarternote):
    duration = midi_duration_to_ticks(music_ml_meta, music_ml_model, music_event.duration, ticks_per_quarternote,
                                      bar_number)
    start_time = note_position_to_ticks(bar_number, music_event, music_ml_meta, music_ml_model,
                                        ticks_per_quarternote)
    return duration, start_time


def note_position_to_ticks(bar_number, music_event, music_ml_meta, music_ml_model, ticks_per_quarternote):
    start_time = 0
    if music_event.position is not None:
        if music_event.position.beat > current_time_signature(music_ml_model, bar_number).numerator:
            raise TextXSemanticError(
                'Beat number is greater than the number of beats in the time signature: ' + str(
                    music_event.position.beat), **get_location(music_event.position))
        start_time += ticks_in_beat(music_ml_model, ticks_per_quarternote, bar_number) * (
                music_event.position.beat - 1)
        if music_event.position.offset is not None:
            start_time += midi_time_to_ticks(music_ml_model, music_ml_meta, music_event.position.offset,
                                             ticks_per_quarternote,
                                             bar_number)
    return start_time


def region_position_to_ticks(bar_number, position, music_ml_meta, music_ml_model, ticks_per_quarternote):
    if position.beat > current_time_signature(music_ml_model, bar_number).numerator:
        raise TextXSemanticError(
            'Beat number is greater than the number of beats in the time signature: ' + str(
                position.beat), **get_location(position.beat))
    start_time = ticks_in_beat(music_ml_model, ticks_per_quarternote, bar_number) * (
            position.beat - 1)
    if position.offset is not None:
        start_time += midi_time_to_ticks(music_ml_model, music_ml_meta, position.offset,
                                         ticks_per_quarternote,
                                         bar_number)
    return start_time


def calculate_event_start_time(music_ml_model, midi_file, music_ml_meta, music_event, bar_number):
    ticks_per_quarternote = midi_file.ticks_per_quarternote

    if textx_isinstance(music_event, music_ml_meta['Note']) or textx_isinstance(music_event,
                                                                                music_ml_meta['Rest']):
        start_time = 0
        if music_event.position is not None:
            start_time += ticks_in_beat(music_ml_model, ticks_per_quarternote, bar_number) * (
                    music_event.position.beat - 1)
            if music_event.position.offset is not None:
                start_time += midi_time_to_ticks(music_ml_model, music_ml_meta, music_event.position.offset,
                                                 ticks_per_quarternote,
                                                 bar_number)
        return start_time

    elif textx_isinstance(music_event, music_ml_meta['Chord']):
        smallest_start_time = float('inf')
        for note in music_event.notes:
            start_time = 0
            if note.position is not None:
                start_time += ticks_in_beat(music_ml_model, ticks_per_quarternote, bar_number) * (
                        note.position.beat - 1)
                if note.position.offset is not None:
                    start_time += midi_time_to_ticks(music_ml_model, music_ml_meta, note.position.offset,
                                                     ticks_per_quarternote,
                                                     bar_number)
            elif music_event.position is not None:
                start_time += ticks_in_beat(music_ml_model, ticks_per_quarternote, bar_number) * (
                        music_event.position.beat - 1)
                if music_event.position.offset is not None:
                    start_time += midi_time_to_ticks(music_ml_model, music_ml_meta, music_event.position.offset,
                                                     ticks_per_quarternote,
                                                     bar_number)
            smallest_start_time = min(smallest_start_time, start_time)
        return smallest_start_time
