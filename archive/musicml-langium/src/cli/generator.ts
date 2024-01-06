import fs from "fs";
import path from "path";
import {
  MusicPiece,
} from "../language-server/generated/ast";
import MidiWriter from "midi-writer-js";

import { extractDestinationAndName } from "./cli-util";
import { compile } from "../compilers/music-piece";

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




