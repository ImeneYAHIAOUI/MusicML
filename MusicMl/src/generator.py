#!/usr/bin/env python3
import sys

sys.path.append('compilers')
from midiutil import MIDIFile
from compilers.track_compiler import *


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
            position = bar_position_in_ticks(music_ml_model, midi_file, tempo.bar)
            if tempo.start is not None:
                position += duration_to_ticks(tempo.start, midi_file.ticks_per_quarternote)
            midi_file.addTempo(i, position, tempo.tempo)
        midi_file.addTimeSignature(i, 0, music_ml_model.defaultTimeSignature.numerator,
                                   music_ml_model.defaultTimeSignature.denominator, 24, 8)
        for time_signature in music_ml_model.timeSignatures:
            position = bar_position_in_ticks(music_ml_model, midi_file, time_signature.bar)
            if time_signature.start is not None:
                position += duration_to_ticks(time_signature.start, midi_file.ticks_per_quarternote)
            midi_file.addTimeSignature(i, position, time_signature.numerator,
                                       time_signature.denominator, 24, 8)
        compile_track(music_ml_model, music_ml_meta, track, midi_file, i)
    bin_file = open(ml_file_name + '.mid', 'wb')
    midi_file.writeFile(bin_file)
    bin_file.close()
