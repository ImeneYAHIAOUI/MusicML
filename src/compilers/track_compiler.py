from bar_compiler import *
from region_compiler import *
from control_message_compiler import *


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
        if textx_isinstance(bar, music_ml_meta['EmptyBar']) or textx_isinstance(bar, music_ml_meta['ReusedBar']):
            repeat = bar.times
            if repeat == 0:
                repeat = 1
            i += repeat
    for region in track.midiRegions:
        compile_region(music_ml_model, music_ml_meta, region, midi_file, track, track_number, channel, velocity)
    for control_message in track.controlMessages:
        compile_control_message(music_ml_model, control_message, track_number, channel, midi_file)
