from musical_event_compiler import *


def compile_region(music_ml_model, music_ml_meta, region, midi_file, track, track_number, channel, velocity, reused_start_position):
    if region.velocity != 0:
        velocity = region.velocity
    original_region = get_original_region(music_ml_meta, track, region)

    original_regions_start_position = position_in_ticks(music_ml_model,music_ml_meta, midi_file, original_region.start)

    original_regions_end_position = position_in_ticks(music_ml_model,music_ml_meta, midi_file, original_region.end)

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
        midi_file.addNote(track_number, channel-1, midi_event.pitch, reused_event_start_position, duration, velocity)


