from utils import *

from textx import *


def compile_music_event(music_ml_model, music_ml_meta, music_event, position, midi_file, track_number, channel,
                        velocity):
    if textx_isinstance(music_event, music_ml_meta['Note']):
        compile_note_event(music_ml_meta, music_ml_model, music_event, position, midi_file, track_number, channel,
                           velocity)
    elif textx_isinstance(music_event, music_ml_meta['Chord']):
        compile_chord_event(music_ml_model, music_ml_meta, music_event, position, midi_file, track_number, channel,
                            velocity)
    else:
        compile_rest_event(music_ml_meta, music_ml_model, music_event, position, midi_file, track_number, channel)


def compile_note_event(music_ml_meta, music_ml_model, note, position, midi_file, track_number, channel, velocity,
                       ticks_to_add=0, chordPosition=0):
    if note.velocity != 0:
        velocity = note.velocity
    duration, start = get_not_position_and_duration(music_ml_meta, position, note, music_ml_model,
                                                    midi_file.ticks_per_quarternote)
    if start == 0 and chordPosition is not None:
        start = note_position_to_ticks(position, note, music_ml_meta, music_ml_model,  midi_file.ticks_per_quarternote)

    position_in_track = bar_position_in_ticks(music_ml_model, midi_file, position) + start + ticks_to_add
    repeat = 1 if note.repeat == 0 else note.repeat
    for i in range(repeat):
        for note_value in note.values:
            value = note_to_midi(note_value)
            if value is None:
                raise TextXSemanticError('Note not supported: ', **get_location(note.values))
            midi_file.addNote(track_number, channel, value, int(position_in_track), duration, velocity)
        position_in_track += duration


def compile_rest_event(music_ml_meta, music_ml_model, rest, position, midi_file, track_number, channel):
    duration, start = get_not_position_and_duration(music_ml_meta, position, rest, music_ml_model,
                                                    midi_file.ticks_per_quarternote)
    position_in_track = bar_position_in_ticks(music_ml_model, midi_file, position) + start

    midi_file.addNote(track_number, channel, 60, position_in_track, duration, 0)


def compile_chord_event(music_ml_model, music_ml_meta, chord, position, midi_file, track_number, channel,
                        velocity):
    ticks_to_add = 0
    if chord.velocity != 0:
        velocity = chord.velocity
    repeat = chord.repeat
    if repeat == 0:
        repeat = 1
    duration = calculate_chord_length(music_ml_model, chord, midi_file, music_ml_meta, position)
    chord_position = None
    if chord.position is not None:
        chord_position = chord.position
    for i in range(repeat):
        for note in chord.notes:
            compile_note_event(music_ml_meta, music_ml_model, note, position, midi_file, track_number, channel,
                               velocity,
                               ticks_to_add, chord_position)
        ticks_to_add += duration
