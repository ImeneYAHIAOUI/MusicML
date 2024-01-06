"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.compileNote = void 0;
const midi_writer_js_1 = __importDefault(require("midi-writer-js"));
const pitch_1 = require("./pitch");
const drum_1 = require("./drum");
function compileNote(note, midiTrack) {
    let midiPitches = [];
    if (note.noteValue.$type === "NormalNote") {
        midiPitches = compileNormalNote(note.noteValue);
    }
    else if (note.noteValue.$type === "DrumNote") {
        midiPitches = compileDrumNote(note.noteValue);
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
        midiTrack.addEvent(new midi_writer_js_1.default.NoteEvent({
            pitch: midiPitches,
            tick: note.startTick,
            wait: wait,
            duration: duration,
            sequential: sequence,
            repeat: repeat,
            velocity: velocity,
            channel: channel,
        }));
    }
    else {
        midiTrack.addEvent(new midi_writer_js_1.default.NoteEvent({
            pitch: midiPitches,
            wait: wait,
            duration: duration,
            sequential: sequence,
            repeat: repeat,
            velocity: velocity,
            channel: channel,
        }));
    }
}
exports.compileNote = compileNote;
function compileNormalNote(note) {
    const pitches = note.pitches;
    const midiPitches = [];
    for (const pitch of pitches) {
        midiPitches.push((0, pitch_1.compilePitch)(pitch));
    }
    return midiPitches;
}
function compileDrumNote(note) {
    const drumNotes = note.notes;
    const midiDrumNotes = [];
    for (const drumNote of drumNotes) {
        midiDrumNotes.push((0, drum_1.compileDrum)(drumNote));
    }
    return midiDrumNotes;
}
//# sourceMappingURL=note.js.map