"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.compile = void 0;
const midi_writer_js_1 = __importDefault(require("midi-writer-js"));
const track_1 = require("./track");
function compile(musicPiece) {
    const midiTrack = new midi_writer_js_1.default.Track();
    const midiClocksPerTick = musicPiece.globalDirectives.midiClocksPerTick
        ? musicPiece.globalDirectives.midiClocksPerTick
        : 24;
    const notesPerMidiClock = musicPiece.globalDirectives.notesPerMidiClock
        ? musicPiece.globalDirectives.notesPerMidiClock
        : 8;
    midiTrack.setTimeSignature(musicPiece.globalDirectives.timeSignature.beatsPerBar, musicPiece.globalDirectives.timeSignature.noteValue, midiClocksPerTick, notesPerMidiClock);
    midiTrack.setTempo(musicPiece.globalDirectives.tempo);
    let tracks = [];
    for (const track of musicPiece.tracks) {
        if (track.startTick) {
            midiTrack.setTempo(musicPiece.globalDirectives.tempo, track.startTick);
        }
        (0, track_1.compileTrack)(track, midiTrack);
        tracks.push(midiTrack);
    }
    return tracks;
}
exports.compile = compile;
//# sourceMappingURL=music-piece.js.map