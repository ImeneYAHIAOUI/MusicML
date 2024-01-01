from musical_event_compiler import *


def compile_region(music_ml_model, music_ml_meta, region, midi_file, track, track_number, channel, velocity):
    if textx_isinstance(region, music_ml_meta['ReusedRegion']):
        if region.velocity != 0:
            velocity = region.velocity
        original_region = get_original_region(music_ml_meta, track, region)
        original_regions_start_position = bar_position_in_ticks(music_ml_model, midi_file, original_region.bar)
        if original_region.start is not None:
            original_regions_start_position += duration_to_ticks(original_region.start, midi_file.ticks_per_quarternote)

        original_regions_end_position = original_regions_start_position + duration_to_ticks(original_region.size,
                                                                                            midi_file.ticks_per_quarternote)

        reused_start_position = bar_position_in_ticks(music_ml_model, midi_file, region.bar)
        if region.start is not None:
            reused_start_position += duration_to_ticks(region.start, midi_file.ticks_per_quarternote)
        track_index = track_number
        if midi_file.header.numeric_format == 1:
            track_index += 1
        midi_events = [event for event in midi_file.tracks[track_index].eventList if event.evtname == 'NoteOn' and
                       (original_regions_start_position <= event.tick < original_regions_end_position
                        or original_regions_start_position < event.tick +
                        event.duration < original_regions_end_position
                        or (
                                event.tick <= original_regions_start_position and event.tick
                                + event.duration >= original_regions_end_position))]
        for midi_event in midi_events:
            start = midi_event.tick
            duration = midi_event.duration
            reused_event_start_position = reused_start_position
            if start < original_regions_start_position:
                duration -= original_regions_start_position - start
            if start + duration > original_regions_end_position:
                duration -= start + duration - original_regions_end_position
            if original_regions_start_position <= start < original_regions_end_position:
                reused_event_start_position = reused_start_position + start - original_regions_start_position
            midi_file.addNote(track_number, channel, midi_event.pitch, reused_event_start_position, duration, velocity)
        for event in region.musicalEvents:
            event_start_position = calculate_event_start_time(midi_file, music_ml_meta, event) + reused_start_position
            if event_start_position > reused_start_position + region.size:
                raise TextXSemanticError('Musical event is out of region range',
                                         **get_location(region))
            bar_position = 0
            while bar_position_in_ticks(music_ml_model, midi_file, bar_position) < event_start_position:
                bar_position += 1
            compile_music_event(music_ml_model, music_ml_meta, event, bar_position, midi_file, track_number, channel,
                                velocity)
