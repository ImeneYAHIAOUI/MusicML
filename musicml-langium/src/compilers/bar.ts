import { Bar } from "../language-server/generated/ast";
import { compileNote } from "./note";

import { Track  as MIDITrack } from "midi-writer-js/build/types/chunks/track";

export function compileBar(bar: Bar, midiTrack: MIDITrack) {
    const repeat = bar.repeat ? bar.repeat : 1;
    for (let i = 0; i < repeat; i++) {
        for (const note of bar.notes) {
            compileNote(note, midiTrack);
        }
    }
}