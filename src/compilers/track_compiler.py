from bar_compiler import *
from region_compiler import *
from control_message_compiler import *


def compile_track(music_ml_model, music_ml_meta, track, midi_file, track_number, ticks_to_add=0):
    track_settings(midi_file, music_ml_model, music_ml_meta, track, track_number)
    program_number = instrument_program_number(track.instrument)
    if program_number is None:
        raise TextXSemanticError('Instrument not found: ' + track.instrument, **get_location(track))
    channel = default_channel(track.instrument)
    velocity = 50
    if track.channel != 0:
        channel = track.channel
    if track.velocity != 0:
        velocity = track.velocity
    midi_file.addProgramChange(track_number, channel-1, 0, program_number)
    compile_music(channel, midi_file, music_ml_meta, music_ml_model, ticks_to_add, track, track_number, velocity)


def compile_music(channel, midi_file, music_ml_meta, music_ml_model, ticks_to_add, track, track_number, velocity):
    if textx_isinstance(track.music, music_ml_meta['PlayableBars']):
        play_bars(channel, midi_file, music_ml_meta, music_ml_model, track.music, track_number, velocity, ticks_to_add)
    else:
        define_then_arrange(channel, midi_file, music_ml_meta, music_ml_model, track.music, track_number, velocity,
                            ticks_to_add)
    for control_message in track.controlMessages:
        compile_control_message(music_ml_model, music_ml_meta, control_message, track_number, channel, midi_file,
                                ticks_to_add)


def track_settings(midi_file, music_ml_model, music_ml_meta, track, track_number):
    midi_file.addTempo(track_number, 0, music_ml_model.defaultTempo)
    for tempo in music_ml_model.tempos:
        position = position_in_ticks(music_ml_model, music_ml_meta, midi_file, tempo.position)
        midi_file.addTempo(track_number, position, tempo.value)
    midi_file.addTimeSignature(track_number, 0, music_ml_model.defaultTimeSignature.numerator,
                               music_ml_model.defaultTimeSignature.denominator, 24, 8)
    for time_signature in music_ml_model.timeSignatures:
        position = bar_position_in_ticks(music_ml_model, midi_file, time_signature.bar)
        midi_file.addTimeSignature(track_number, position, time_signature.numerator,
                                   time_signature.denominator, 24, 8)
    midi_file.addTrackName(track_number, 0, track.name)


def play_bars(channel, midi_file, music_ml_meta, music_ml_model, track, track_number, velocity, ticks_to_add=0):
    i = 0
    for bar in track.bars:
        compile_bar(music_ml_model, music_ml_meta, bar, i, midi_file, track, track_number, channel, velocity,
                    ticks_to_add)
        if textx_isinstance(bar, music_ml_meta['Bar']):
            i += 1
        if textx_isinstance(bar, music_ml_meta['EmptyBar']) or textx_isinstance(bar, music_ml_meta['ReusedBar']):
            repeat = bar.times
            if repeat == 0:
                repeat = 1
            i += repeat


def define_then_arrange(channel, midi_file, music_ml_meta, music_ml_model, track, track_number, velocity,
                        ticks_to_add=0):
    i = 0
    for piece in track.arrange:
        if textx_isinstance(piece, music_ml_meta['ArrangedBar']):
            bar = get_original_bar(music_ml_meta, track, piece)
            compile_bar(music_ml_model, music_ml_meta, bar, i, midi_file, track, track_number, channel, velocity,
                        ticks_to_add)
            if textx_isinstance(bar, music_ml_meta['Bar']):
                i += 1
            if textx_isinstance(bar, music_ml_meta['EmptyBar']) or textx_isinstance(bar, music_ml_meta['ReusedBar']):
                repeat = bar.times
                if repeat == 0:
                    repeat = 1
                i += repeat
        else:
            start = bar_position_in_ticks(music_ml_model, midi_file, i)
            if piece.start is not None:
                if textx_isinstance(piece.start, music_ml_meta['NotePosition']):
                    start -= region_position_to_ticks(i, piece.start, music_ml_meta, music_ml_model,
                                                      midi_file.ticks_per_quarternote)
            region = get_original_region(music_ml_meta, track, piece)
            compile_region(music_ml_model, music_ml_meta, region, midi_file, track, track_number, channel, velocity,
                           start + ticks_to_add)
            end = position_in_ticks(music_ml_model, music_ml_meta, midi_file, region.end)
            while bar_position_in_ticks(music_ml_model, midi_file, i) < end:
                i += 1

