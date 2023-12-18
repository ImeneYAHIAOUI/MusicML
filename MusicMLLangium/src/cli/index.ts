import chalk from 'chalk';
import { Command } from 'commander';
import { MusicPiece } from '../language-server/generated/ast';
import { MusicMlLanguageMetaData } from '../language-server/generated/module';
import { createMusicMlServices } from '../language-server/music-ml-module';
import { extractAstNode } from './cli-util';
import { generateMIDIFile } from './generator';
import { NodeFileSystem } from 'langium/node';

export const generateAction = async (fileName: string, opts: GenerateOptions): Promise<void> => {
    const services = createMusicMlServices(NodeFileSystem).MusicMl;
    const musicPiece = await extractAstNode<MusicPiece>(fileName, services);
    const generatedFilePath = generateMIDIFile(musicPiece, fileName, opts.destination);
    console.log(chalk.green(`MID file generated successfully: ${generatedFilePath}`));
};

export type GenerateOptions = {
    destination?: string;
}

export default function(): void {
    const program = new Command();

    program
        // eslint-disable-next-line @typescript-eslint/no-var-requires
        .version(require('../../package.json').version);

    const fileExtensions = MusicMlLanguageMetaData.fileExtensions.join(', ');
    program
        .command('generate')
        .argument('<file>', `source file (possible file extensions: ${fileExtensions})`)
        .option('-d, --destination <dir>', 'destination directory of generating')
        .description('generates JavaScript code that prints "Hello, {name}!" for each greeting in a source file')
        .action(generateAction);

    program.parse(process.argv);
}
