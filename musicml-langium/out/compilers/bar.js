"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.compileBar = void 0;
const note_1 = require("./note");
function compileBar(bar, midiTrack) {
    const repeat = bar.repeat ? bar.repeat : 1;
    for (let i = 0; i < repeat; i++) {
        for (const note of bar.notes) {
            (0, note_1.compileNote)(note, midiTrack);
        }
    }
}
exports.compileBar = compileBar;
//# sourceMappingURL=bar.js.map