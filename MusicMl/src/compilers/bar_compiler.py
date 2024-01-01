from musical_event_compiler import *


def compile_bar(music_ml_model, music_ml_meta, bar, i, midi_file, track, track_number, channel, velocity):
    if textx_isinstance(bar, music_ml_meta['Bar']):
        music_events = bar.musicalEvents
        ticks_in_bar = bar_position_in_ticks(music_ml_model, midi_file, i + 1) - bar_position_in_ticks(music_ml_model,
                                                                                                       midi_file, i)
        music_events_length = calculate_music_events_length(midi_file, music_ml_meta, music_events)
        if music_events_length > ticks_in_bar:
            raise TextXSemanticError('Bar is overflown, split into multiple bars', **get_location(bar))
        if bar.velocity != 0:
            velocity = bar.velocity
        for music_event in music_events:
            compile_music_event(music_ml_model, music_ml_meta, music_event, i, midi_file, track_number, channel,
                                velocity)
        overlapping_events = bar.overlappingEvents
        for overlapping_event in overlapping_events:
            event_start_position = calculate_event_start_time(midi_file, music_ml_meta, overlapping_event)
            if event_start_position > ticks_in_bar:
                raise TextXSemanticError('Overlapping event is out of bar bound,'
                                         ' change the start of the event or move it to the correct bar',
                                         **get_location(bar))
            compile_music_event(music_ml_model, music_ml_meta, overlapping_event, i, midi_file, track_number, channel,
                                velocity)
    position = i
    if textx_isinstance(bar, music_ml_meta['ReusedBar']):
        original_bar = get_original_bar(music_ml_meta, track, bar)
        music_events = original_bar.musicalEvents + bar.musicalEvents
        ticks_in_bar = bar_position_in_ticks(music_ml_model, midi_file, i + 1) - bar_position_in_ticks(music_ml_model,
                                                                                                       midi_file, i)
        music_events_length = calculate_music_events_length(midi_file, music_ml_meta, music_events)
        if music_events_length > ticks_in_bar:
            raise TextXSemanticError('Bar is overflown, split into multiple bars', **get_location(bar))
        overlapping_events = original_bar.overlappingEvents + bar.overlappingEvents
        repeat = bar.times
        if repeat == 0:
            repeat = 1
        for i in range(repeat):
            for music_event in music_events:
                compile_music_event(music_ml_model, music_ml_meta, music_event, position, midi_file, track_number,
                                    channel, velocity)
            for overlapping_event in overlapping_events:
                event_start_position = calculate_event_start_time(midi_file, music_ml_meta, overlapping_event)
                if event_start_position > ticks_in_bar:
                    raise TextXSemanticError('Overlapping event is out of bar range,'
                                             ' change the start of the event or move it to the correct bar',
                                             **get_location(bar))
                compile_music_event(music_ml_model, music_ml_meta, overlapping_event, position, midi_file,
                                    track_number, channel, velocity)
            position += 1
