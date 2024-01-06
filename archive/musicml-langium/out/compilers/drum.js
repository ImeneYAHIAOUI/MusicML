"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.compileDrum = void 0;
function compileDrum(drumNote) {
    const note = drumNote === "bd"
        ? "C2"
        : drumNote === "sd"
            ? "E2"
            : drumNote === "ch"
                ? "F#2"
                : drumNote === "oh"
                    ? "A#2"
                    : drumNote === "rc"
                        ? "F2"
                        : "D#2";
    return note;
}
exports.compileDrum = compileDrum;
//# sourceMappingURL=drum.js.map