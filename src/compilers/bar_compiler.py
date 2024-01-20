from musical_event_compiler import *

def ms_to_ticks(milliseconds, ticks_per_quarternote):
    return int((milliseconds * ticks_per_quarternote) / 1000)


def is_first_interval(number, notes):
    interval = number //notes
    return interval % 2 == 0

def have_human_error(music_ml_model) :
    return music_ml_model.notes >0 and music_ml_model.margin > 0

def add_human_error(i, ticks_to_add, midi_file, music_ml_model) :
    ticks_error = ms_to_ticks(music_ml_model.margin, midi_file.ticks_per_quarternote)
    if(is_first_interval(i, music_ml_model.notes)) :
        return ticks_to_add + ticks_error
    return ticks_to_add - ticks_error

def compile_bar(music_ml_model, music_ml_meta, bar, bar_number, midi_file, track, track_number, channel, velocity,iterator, 
                ticks_to_add=0):
    if textx_isinstance(bar, music_ml_meta['Bar']):
        music_events = bar.musicalEvents
        if bar.velocity != 0:
            velocity = bar.velocity

        for music_event in music_events:
            if(have_human_error(music_ml_model)) : 
                iterator+=1
                compile_music_event(music_ml_model, music_ml_meta, music_event, bar_number, midi_file, track_number,
                                    channel,
                                    velocity, add_human_error(iterator, ticks_to_add,midi_file, music_ml_model))
            else : 
                compile_music_event(music_ml_model, music_ml_meta, music_event, bar_number, midi_file, track_number,
                        channel, velocity, ticks_to_add)

    position = bar_number
    if textx_isinstance(bar, music_ml_meta['ReusedBar']):
        original_bar = get_original_bar(music_ml_meta, track, bar)
        bar_events = original_bar.musicalEvents + bar.musicalEvents
        repeat = bar.times
        if repeat == 0:
            repeat = 1
        for i in range(repeat):
            for music_event in bar_events:
                if(have_human_error(music_ml_model)) : 
                    iterator+=1
                    compile_music_event(music_ml_model, music_ml_meta, music_event, position, midi_file, track_number,
                                        channel, velocity, add_human_error(iterator, ticks_to_add,midi_file, music_ml_model), )
                else :
                    compile_music_event(music_ml_model, music_ml_meta, music_event, position, midi_file, track_number,
                                        channel, velocity, ticks_to_add, )

            position += 1
        removed_bar_events(music_ml_meta, music_ml_model, midi_file, bar.removedNotes, bar_number, track_number, ticks_to_add)
        changed_bar_events(music_ml_meta, music_ml_model, midi_file, bar.changedEvents, bar_number, track_number, ticks_to_add)


def removed_bar_events(music_ml_meta, music_ml_model, midi_file, removed_notes, bar_number, track_number, ticks_to_add=0):
    for removed_note in removed_notes:
        position = bar_position_in_ticks(music_ml_model, midi_file, bar_number) + ticks_in_beat(music_ml_model,
                                                                                                midi_file.ticks_per_quarternote,
                                                                                                bar_number) * (
                               removed_note.position.beat - 1) + ticks_to_add
        if removed_note.position.offset is not None:
            position += midi_time_to_ticks(music_ml_meta, music_ml_model, removed_note.position.offset,
                                           midi_file.ticks_per_quarternote, bar_number)
        notes = [note_to_midi(note) for note in removed_note.values]
        i = 0
        for msg in midi_file.tracks[track_number + 1].eventList:
            if msg.evtname == 'NoteOn' and msg.tick == int(position) and msg.pitch in notes:
                msg.volume = 0


def changed_bar_events(music_ml_meta, music_ml_model, midi_file, changed_events, bar_number, track_number, ticks_to_add=0):
    for changed_event in changed_events:
        position = bar_position_in_ticks(music_ml_model, midi_file, bar_number) + ticks_in_beat(music_ml_model,
                                                                                                midi_file.ticks_per_quarternote,
                                                                                                bar_number) * (
                               changed_event.position.beat - 1) + ticks_to_add
        if changed_event.position.offset is not None:
            position += midi_time_to_ticks(music_ml_meta, music_ml_model, changed_event.position.offset,
                                           midi_file.ticks_per_quarternote, bar_number)
        note = note_to_midi(changed_event.value)
        i = 0
        for msg in midi_file.tracks[track_number + 1].eventList:
            if msg.evtname == 'NoteOn' and msg.pitch == note and msg.tick == int(position):
                msg.pitch = note_to_midi(changed_event.newValue)
                note_off = midi_file.tracks[track_number + 1].eventList[i + 1]
                note_off.pitch = note_to_midi(changed_event.newValue)
            i += 1
