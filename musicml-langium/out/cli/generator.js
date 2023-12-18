"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.generateMIDIFile = void 0;
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const midi_writer_js_1 = __importDefault(require("midi-writer-js"));
const cli_util_1 = require("./cli-util");
const music_piece_1 = require("../compilers/music-piece");
function generateMIDIFile(musicPiece, filePath, destination) {
    const data = (0, cli_util_1.extractDestinationAndName)(filePath, destination);
    const generatedFilePath = `${path_1.default.join(data.destination, data.name)}.mid`;
    const tracks = (0, music_piece_1.compile)(musicPiece);
    const writer = new midi_writer_js_1.default.Writer(tracks);
    const file = writer.buildFile();
    if (!fs_1.default.existsSync(data.destination)) {
        fs_1.default.mkdirSync(data.destination, { recursive: true });
    }
    fs_1.default.writeFileSync(generatedFilePath, Buffer.from(file));
    return generatedFilePath;
}
exports.generateMIDIFile = generateMIDIFile;
//# sourceMappingURL=generator.js.map