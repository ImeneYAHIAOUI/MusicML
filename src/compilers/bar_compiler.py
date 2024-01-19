from musical_event_compiler import *


def compile_bar(music_ml_model, music_ml_meta, bar, bar_number, midi_file, track, track_number, channel, velocity):
    if textx_isinstance(bar, music_ml_meta['Bar']):
        music_events = bar.musicalEvents
        if bar.velocity != 0:
            velocity = bar.velocity
        for music_event in music_events:
            compile_music_event(music_ml_model, music_ml_meta, music_event, bar_number, midi_file, track_number,
                                channel,
                                velocity)
    position = bar_number
    if textx_isinstance(bar, music_ml_meta['ReusedBar']):
        original_bar = get_original_bar(music_ml_meta, track, bar)
        original_bar_events = original_bar.musicalEvents
        music_events = reused_bar_events(music_ml_meta, music_ml_model, midi_file, original_bar_events, bar, bar_number)

        repeat = bar.times
        if repeat == 0:
            repeat = 1
        for i in range(repeat):
            for music_event in music_events:
                compile_music_event(music_ml_model, music_ml_meta, music_event, position, midi_file, track_number,
                                    channel, velocity)
            position += 1


def reused_bar_events(music_ml_meta, music_ml_model, midi_file, music_events, reused_bar, bar_number):
    return music_events
