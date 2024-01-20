from utils import *
from track_compiler import *


def compile_section(music_ml_model, music_ml_meta, section, midi_file, position):
    for track in section.tracks:
        track_number, trackDef = get_track_def(music_ml_model, track.name)
        velocity = 50
        if trackDef.velocity != 0:
            velocity = track.velocity
        channel = default_channel(trackDef.instrument)
        if trackDef.channel != 0:
            channel = trackDef.channel
        compile_music(channel, midi_file, music_ml_meta, music_ml_model, position, track, track_number, velocity)



def get_track_def(music_ml_model, name):
    track = None
    index = 0
    for i, track_def in enumerate(music_ml_model.song.trackDefs):
        if track_def.name == name:
            track = track_def
            index = i
            break
    if track is None:
        raise TextXSemanticError('Track not found: ' + name, **get_location(music_ml_model))
    return index, track
