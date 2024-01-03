#!/usr/bin/env python3

import os
from argparse import ArgumentParser
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from generator import generate_midi_file


def main(debug=False):
    this_folder = os.getcwd()
    this_folder = this_folder.replace('\\', '/')
    parent_folder = os.path.abspath(os.path.join(this_folder, os.pardir))
    parent_folder = parent_folder.replace('\\', '/')
    argparse = ArgumentParser()
    argparse.add_argument('--generate', type=str, help='Generate Midi file from this musicML file')
    argparse.add_argument('-d', '--debug', action='store_true', help='debug mode')
    if argparse.parse_args().debug:
        debug = True
    ml_file = argparse.parse_args().generate

    # Get metamodel from language description
    music_ml_meta = metamodel_from_file( this_folder + '/musicML.tx', debug=debug)
    # Optionally export meta-model to dot
    metamodel_export(music_ml_meta, parent_folder + '/diagram/musicML.dot')

    # Instantiate model
    music_ml_model = music_ml_meta.model_from_file(parent_folder + '/' + ml_file)

    ml_file_name = ml_file.split('.')[0]
    try:
        ml_file_name = ml_file_name.split('/')[1]
    except:
        ml_file_name = ml_file_name.split('\\')[1]

    # Generate Midi file
    generate_midi_file(music_ml_meta, music_ml_model, '../generated/' + ml_file_name)

    # Optionally export model to dot
    model_export(music_ml_model, parent_folder + '/diagram/' + ml_file_name + '.dot')


if __name__ == '__main__':
    main()
