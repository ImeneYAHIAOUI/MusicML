from utils import *


def compile_control_message(music_ml_model, music_ml_meta, control_message, track_number, channel, midi_file, ticks_to_add=0):
    position = position_in_ticks(music_ml_model, music_ml_meta, midi_file, control_message.position) + ticks_to_add
    cc = control_message.CC
    if control_message.message != '':
        cc = get_control_message_number(control_message.message)
        if cc is None:
            raise TextXSemanticError('Control message not supported: ' + control_message.message, **get_location(
                control_message))
    else:
        if cc == 3 or cc == 9 or cc == 14 or cc == 15 or 20 <= cc <= 31 or 85 <= cc <= 87 or 89 <= cc <= 90 or 102 <= cc <= 119 or cc < 0 or cc > 127:
            raise TextXSemanticError('cc value not supported: ' + control_message.CC, **get_location(
                control_message))

    midi_file.addControllerEvent(track_number, channel, position, cc, control_message.value)
