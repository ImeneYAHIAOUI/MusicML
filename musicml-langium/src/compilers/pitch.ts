import { Pitch } from "../language-server/generated/ast";

export function compilePitch(pitch: Pitch): string {
    const octave = pitch.octave;
    const value = pitch.value;
    let noteValue =
        value === "do"
            ? "C"
            : value === "re"
                ? "D"
                : value === "mi"
                    ? "E"
                    : value === "fa"
                        ? "F"
                        : value === "sol"
                            ? "G"
                            : value === "la"
                                ? "A"
                                : value === "si"
                                    ? "B"
                                    : "C";
    const sharpnotes = ["C", "D", "F", "G", "A"];
    const flatNotes = ["D", "E", "G", "A", "B"];
    if (pitch.accidental) {
        noteValue +=
            pitch.accidental === "sharp" && sharpnotes.includes(noteValue)
                ? "#"
                : pitch.accidental === "flat" && flatNotes.includes(noteValue)
                    ? "b"
                    : "";
    }
    noteValue += octave;
    return noteValue;
}