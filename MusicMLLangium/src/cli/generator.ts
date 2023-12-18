import fs from "fs";
import path from "path";
import {
  Bar,
  DrumNote,
  MusicPiece,
  NormalNote,
  Note,
  Pitch,
  Track,
} from "../language-server/generated/ast";
import MidiWriter from "midi-writer-js";
import { Track as MIDITrack } from "midi-writer-js/build/types/chunks/track";

import { extractDestinationAndName } from "./cli-util";

export function generateMIDIFile(
  musicPiece: MusicPiece,
  filePath: string,
  destination: string | undefined
): string {
  const data = extractDestinationAndName(filePath, destination);
  const generatedFilePath = `${path.join(data.destination, data.name)}.mid`;

  const tracks = compile(musicPiece);
  const writer = new MidiWriter.Writer(tracks);
  const file = writer.buildFile();

  if (!fs.existsSync(data.destination)) {
    fs.mkdirSync(data.destination, { recursive: true });
  }

  fs.writeFileSync(generatedFilePath, Buffer.from(file));

  return generatedFilePath;
}

function compile(musicPiece: MusicPiece): MIDITrack[] {
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

function compileTrack(track: Track, midiTrack: MIDITrack) {
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

function compileBar(bar: Bar, midiTrack: MIDITrack) {
  const repeat = bar.repeat ? bar.repeat : 1;
  for (let i = 0; i < repeat; i++) {
    for (const note of bar.notes) {
      compileNote(note, midiTrack);
    }
  }
}

function compileNote(note: Note, midiTrack: MIDITrack) {
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
function compilePitch(pitch: Pitch): string {
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

function compileDrum(drumNote: string): string {
  const note =
    drumNote === "bd"
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

type InstrumentMapping = Record<string, number>;

const instrumentMapping: InstrumentMapping = {
  "Acoustic Grand Piano": 0,
  "Bright Acoustic Piano": 1,
  "Electric Grand Piano": 2,
  "Honky-tonk Piano": 3,
  "Rhodes Piano": 4,
  "Chorused Piano": 5,
  Harpsichord: 6,
  Clavinet: 7,
  Celesta: 8,
  Glockenspiel: 9,
  "Music Box": 10,
  Vibraphone: 11,
  Marimba: 12,
  Xylophone: 13,
  "Tubular Bells": 14,
  Dulcimer: 15,
  "Drawbar Organ": 16,
  "Percussive Organ": 17,
  "Rock Organ": 18,
  "Church Organ": 19,
  "Reed Organ": 20,
  Accordion: 21,
  Harmonica: 22,
  "Tango Accordion": 23,
  "Acoustic Guitar (nylon)": 24,
  "Acoustic Guitar (steel)": 25,
  "Electric Guitar (jazz)": 26,
  "Electric Guitar (clean)": 27,
  "Electric Guitar (muted)": 28,
  "Overdriven Guitar": 29,
  "Distortion Guitar": 30,
  "Guitar Harmonics": 31,
  "Acoustic Bass": 32,
  "Electric Bass (finger)": 33,
  "Electric Bass (pick)": 34,
  "Fretless Bass": 35,
  Drums: 35,
  "Slap Bass 1": 36,
  "Slap Bass 2": 37,
  "Synth Bass 1": 38,
  "Synth Bass 2": 39,
  Violin: 40,
  Viola: 41,
  Cello: 42,
  Contrabass: 43,
  "Tremolo Strings": 44,
  "Pizzicato Strings": 45,
  "Orchestral Harp": 46,
  Timpani: 47,
  "String Ensemble 1": 48,
  "String Ensemble 2": 49,
};

function getInstrumentNumber(instrumentName: string): number | undefined {
  return instrumentMapping[instrumentName];
}
