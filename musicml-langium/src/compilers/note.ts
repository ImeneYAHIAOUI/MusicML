import MidiWriter from 'midi-writer-js';
import { Note, DrumNote, NormalNote } from "../language-server/generated/ast";
import { compilePitch } from "./pitch";
import { compileDrum } from "./drum";

import { Track  as MIDITrack } from "midi-writer-js/build/types/chunks/track";


export function compileNote(note: Note, midiTrack: MIDITrack) {
    let midiPitches: string[] = [];
    if (note.noteValue.$type === "NormalNote") {
        midiPitches = compileNormalNote(note.noteValue as NormalNote);
    } else if (note.noteValue.$type === "DrumNote") {
        midiPitches = compileDrumNote(note.noteValue as DrumNote);
    }
    let sequence = false;
    if (note.sequence) {
        sequence = note.sequence === "true" ? true : false;
    }
    let repeat = 1;
    if (note.repeat) {
        repeat = note.repeat;
    }

    let velocity = 50;
    if (note.velocity) {
        velocity = note.velocity;
    }

    let channel = note.noteValue.$type === "DrumNote" ? 10 : 0;
    if (note.channel) {
        channel = note.channel;
    }

    const duration = "T" + note.duration;

    let wait = "0";
    if (note.wait) {
        wait = "T" + note.wait;
    }

    if (note.startTick) {
        midiTrack.addEvent(
            new MidiWriter.NoteEvent({
                pitch: midiPitches,
                tick: note.startTick,
                wait: wait,
                duration: duration,
                sequential: sequence,
                repeat: repeat,
                velocity: velocity,
                channel: channel,
            })
        );
    } else {
        midiTrack.addEvent(
            new MidiWriter.NoteEvent({
                pitch: midiPitches,
                wait: wait,
                duration: duration,
                sequential: sequence,
                repeat: repeat,
                velocity: velocity,
                channel: channel,
            })
        );
    }
}

function compileNormalNote(note: NormalNote) {
    const pitches = note.pitches;
    const midiPitches = [];
    for (const pitch of pitches) {
        midiPitches.push(compilePitch(pitch));
    }
    return midiPitches;
}

function compileDrumNote(note: DrumNote) {
    const drumNotes = note.notes;
    const midiDrumNotes = [];
    for (const drumNote of drumNotes) {
        midiDrumNotes.push(compileDrum(drumNote));
    }
    return midiDrumNotes;
}