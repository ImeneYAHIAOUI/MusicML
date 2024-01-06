import { MusicPiece } from './../language-server/generated/ast';
import { Track as MIDITrack } from "midi-writer-js/build/types/chunks/track";

import MidiWriter from "midi-writer-js";
import { compileTrack } from './track';

export function compile(musicPiece: MusicPiece): MIDITrack[] {
    const midiTrack = new MidiWriter.Track();
    const midiClocksPerTick = musicPiece.globalDirectives.midiClocksPerTick
      ? musicPiece.globalDirectives.midiClocksPerTick
      : 24;
    const notesPerMidiClock = musicPiece.globalDirectives.notesPerMidiClock
      ? musicPiece.globalDirectives.notesPerMidiClock
      : 8;
    midiTrack.setTimeSignature(
      musicPiece.globalDirectives.timeSignature.beatsPerBar,
      musicPiece.globalDirectives.timeSignature.noteValue,
      midiClocksPerTick,
      notesPerMidiClock
    );
    midiTrack.setTempo(musicPiece.globalDirectives.tempo);
    let tracks: MIDITrack[] = [];
    for (const track of musicPiece.tracks) {
      if (track.startTick) {
        midiTrack.setTempo(musicPiece.globalDirectives.tempo, track.startTick);
      }
      compileTrack(track, midiTrack);
      tracks.push(midiTrack);
    }
    return tracks;
}