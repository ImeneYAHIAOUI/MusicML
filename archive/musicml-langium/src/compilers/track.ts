import { Track } from "../language-server/generated/ast";
import { getInstrumentNumber } from "./constants/instrument-mapping";
import { compileBar } from "./bar";


import { Track as MIDITrack } from "midi-writer-js/build/types/chunks/track";
import MidiWriter from "midi-writer-js";

export function compileTrack(track: Track, midiTrack: MIDITrack) {
    const instrument = track.instrument;
    const instrumentNumber = instrument ? getInstrumentNumber(instrument) : 0;
    if (instrumentNumber) {
      midiTrack.addEvent(
        new MidiWriter.ProgramChangeEvent({ instrument: instrumentNumber })
      );
    }
  
    for (const bar of track.bars) {
      compileBar(bar, midiTrack);
    }
  }