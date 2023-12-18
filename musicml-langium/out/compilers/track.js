"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.compileTrack = void 0;
const instrument_mapping_1 = require("./constants/instrument-mapping");
const bar_1 = require("./bar");
const midi_writer_js_1 = __importDefault(require("midi-writer-js"));
function compileTrack(track, midiTrack) {
    const instrument = track.instrument;
    const instrumentNumber = instrument ? (0, instrument_mapping_1.getInstrumentNumber)(instrument) : 0;
    if (instrumentNumber) {
        midiTrack.addEvent(new midi_writer_js_1.default.ProgramChangeEvent({ instrument: instrumentNumber }));
    }
    for (const bar of track.bars) {
        (0, bar_1.compileBar)(bar, midiTrack);
    }
}
exports.compileTrack = compileTrack;
//# sourceMappingURL=track.js.map