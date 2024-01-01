
from utils import *

from textx import *


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
    position_in_ticks = bar_position_in_ticks(music_ml_model, midi_file, position) + ticks_to_add
    if note.start is not None:
        position_in_ticks += duration_to_ticks(note.start, midi_file.ticks_per_quarternote)
    repeat = 1 if note.repeat == 0 else note.repeat
    for i in range(repeat):
        for note_value in note.values:
            value = note_to_midi(note_value)
            if value is None:
                raise TextXSemanticError('Note not supported: ' + note.values, **get_location(note.values))
            midi_file.addNote(track_number, channel, value, position_in_ticks, duration, velocity)
        position_in_ticks += duration


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
