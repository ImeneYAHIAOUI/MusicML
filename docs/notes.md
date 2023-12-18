# Intro :

## What is MIDI ? 

MIDI, which stands for Musical Instrument Digital Interface, is a technical standard that describes a protocol, digital interface, and connectors. This standard allows a wide variety of electronic musical instruments, computers, and other related devices to connect and communicate with one another. MIDI conveys messages about musical notation, pitch and velocity, control signals for parameters such as volume, vibrato, audio panning, cues, and clock signals to set the tempo. As a result, musicians and producers can use MIDI to create and control music in diverse and sophisticated ways.

A key feature of MIDI is that it transmits information about the performance, rather than the actual sounds. This means MIDI data can be used to trigger different types of sound modules, synthesizers, or samples, and the same MIDI sequence can produce vastly different results depending on the instruments or sound sources being controlled.

MIDI technology was standardized in the early 1980s and has been an integral part of music production and performance ever since. It's used in a variety of applications, from simple home studios to complex live concert setups.

## What information does MIDI transmit ? 

MIDI (Musical Instrument Digital Interface) transmits a range of information that allows electronic musical instruments and devices to interact and control each other. This information is communicated through MIDI messages, which are digital instructions that tell the receiving device what to do. The key types of information transmitted by MIDI include:

    Note On/Off Messages: These indicate when a note is played (Note On) and when it is released (Note Off). Along with the note number (which corresponds to a specific pitch), these messages also include velocity information, which is a measure of how hard the note is played or released, affecting the note's dynamics.

    Control Change Messages: These messages convey changes in control settings, such as the movement of sliders, knobs, or switches on a MIDI controller. They can adjust various parameters like volume, pan, modulation, effects levels, and many others.

    Program Change Messages: These messages tell a MIDI device to change the sound or instrument being used. For example, switching from a piano sound to a violin sound on a synthesizer.

    Pitch Bend Messages: These provide information about pitch changes, simulating the bending of a string on a guitar or a shift in pitch on a wind instrument.

    Aftertouch Messages: Some MIDI keyboards and controllers can send information about the pressure applied to keys after they are initially struck. This "aftertouch" can be used to control various aspects of the sound like vibrato or volume.

    System Exclusive (SysEx) Messages: These are manufacturer-specific messages that allow detailed and device-specific control. They can be used for tasks like updating firmware, managing presets, or detailed device-specific editing.

    Clock and Synchronization Messages: These are used in MIDI setups where timing is crucial, such as in sequencers and drum machines. They ensure all devices are synchronized in terms of tempo and timing.

    Song Position Pointer and Song Select Messages: These are used to control the playback of sequenced music, telling devices where to start or stop, and selecting specific sequences or songs.

This broad range of messages allows MIDI to be incredibly versatile in music production, live performance, and other audio-related applications


### Note On/Off : How many notes does MIDI support ? 

In MIDI, the number of distinct notes that can be represented is determined by the MIDI note number system. MIDI note numbers range from 0 to 127, providing a total of 128 different possible notes. This range covers a little more than 10 octaves, but the exact range in terms of musical pitches (like C, D, E, etc.) depends on how these numbers are mapped to musical notes.

In the most common mapping, MIDI note number 60 is designated as Middle C (C4 in scientific pitch notation). From this reference point, you can determine the pitch of the other MIDI note numbers. For example, 61 would be C#4/D♭4, 62 would be D4, and so on. This mapping extends down to MIDI note number 0, which is several octaves below the lowest note on a standard piano, and up to MIDI note number 127, which is several octaves above the highest note on a standard piano.

It's important to note that while MIDI supports 128 distinct note numbers, the actual range of notes you can use effectively depends on the capabilities of the MIDI instruments (like synthesizers or software instruments) you are working with. Some instruments may not be able to produce sounds across the entire MIDI note range.


### Note Velocity 

In MIDI, velocity is a measure of how hard or softly a note is played, and it's an essential aspect of MIDI note-on messages. Velocity adds expression and dynamics to music, as it often corresponds to the volume and timbre of the note being played.

The MIDI standard represents velocity with values ranging from 0 to 127. This provides 128 distinct levels of velocity, allowing for nuanced expression in MIDI performances. Here's how velocity typically works in MIDI:

    Value 0: Usually interpreted as a note-off command in most MIDI devices, meaning the note is not played at all.

    Values 1 to 127: These represent the actual velocity of a note. The lower end of the scale (closer to 1) corresponds to softer or quieter notes, while the higher end (closer to 127) corresponds to louder or more forceful notes.

The effect of velocity on the sound depends on how the receiving instrument or software interprets MIDI data. For example, in a piano sound, higher velocity values typically result in not only a louder note but also a change in timbre, simulating the harder strike of a piano key. In synthesizers or other electronic instruments, velocity might be mapped to various parameters, not just volume, such as filter cutoff, attack time, or modulation depth.

This wide range of velocity levels allows musicians to expressively control the dynamics of their performance when using MIDI keyboards, drum pads, and other velocity-sensitive MIDI controllers.

### And Aftertouch?

Aftertouch in MIDI is a feature that allows musicians to alter the sound of a note after it has been initially played (or struck), by applying additional pressure to the key or pad. This pressure sensitivity can be used to add expressiveness to a performance. There are two types of aftertouch in the MIDI specification:

1. **Channel Aftertouch**: This type of aftertouch sends a single message that affects all notes currently being played on that MIDI channel. When you apply pressure to any key or pad, it generates a channel aftertouch message. The value of this message, typically ranging from 0 to 127, indicates the amount of pressure applied. This is a more common type of aftertouch found on many MIDI keyboards, but its drawback is the lack of individual note control since the pressure affects all notes on the channel equally.

2. **Polyphonic Aftertouch (or Key Pressure)**: This is a more advanced type of aftertouch that allows for individual note control. With polyphonic aftertouch, you can apply different amounts of pressure to different keys or pads, and each will send its own aftertouch message with its own value. This means you can be pressing several notes at the same time and apply pressure to each one independently, controlling the aftertouch effect for each note separately. Polyphonic aftertouch offers greater expressive capabilities but is less commonly found because it requires more sophisticated and thus more expensive keyboard sensors.

In terms of its musical application, aftertouch can be used to control various aspects of the sound such as vibrato, volume, filter cut-off, modulation effects, and more, depending on how the sound module or synthesizer is programmed to respond to aftertouch messages. This provides an additional layer of expression in performance, allowing for more dynamic and emotive playing.

### Difference between Velocity and Aftertouch ?


| Aspect         | Velocity                          | Aftertouch                       |
|----------------|-----------------------------------|----------------------------------|
| **Definition** | Measures the speed at which a key is pressed when a note is initially played. | Measures the pressure applied to a key after it is already pressed and held down. |
| **Timing**     | A single value sent at the moment the key is struck. | Continuous control that can vary for the duration the key is held down after being struck. |
| **Effect**     | Primarily affects the initial volume and often the timbre of the note. Higher velocity typically means a louder, sometimes brighter sound; lower velocity results in a softer sound. | Can be mapped to various parameters like vibrato, filter cutoff, volume, or modulation. Allows real-time expressive control over these parameters while a note is sustained. |
| **Use**        | Adds dynamics to a performance, enabling notes to be played with varying intensities. | Adds expressive control to sustained notes, allowing for real-time modulation of certain aspects of the sound. |
| **Data Type**  | One-time value per note-on event. | Multiple data points can be sent as long as the key is held down and pressure is varied. |
| **Commonality**| Found on almost all MIDI keyboards and controllers. | Less common; channel aftertouch is more widespread, but polyphonic aftertouch is rarer and usually found on more advanced keyboards. |

This table outlines the fundamental differences between velocity and aftertouch, highlighting how they each contribute uniquely to the expressiveness of MIDI performances.

### Pitch bend 

**Pitch Bend** in MIDI is a feature that allows for the adjustment of the pitch of a note or notes, either up or down, after they have been played. This feature is commonly found on MIDI keyboards and synthesizers, often as a wheel or lever on the side of the keyboard. Here's a more detailed look at pitch bend:

1. **Function**: The pitch bend wheel or lever lets the performer slightly alter the pitch of a note in a continuous manner, similar to bending a string on a guitar or using a whammy bar. This can be used for expressive effects like vibrato, portamento (gliding from one pitch to another), or more dramatic pitch changes.

2. **Range**: The range of pitch bend, meaning how far up or down the pitch can be altered, is configurable. It's typically measured in semitones (half steps). For instance, a pitch bend range might be set to ±2 semitones, allowing the pitch to be bent up or down by a maximum of two half steps.

3. **MIDI Representation**: In MIDI messages, pitch bend is represented by a 14-bit value, combining two 7-bit values (ranging from 0-127 each). This allows for 16,384 possible positions between the minimum and maximum bend values. The center position (8192) represents no pitch bend.

4. **Usage**: Musicians use the pitch bend feature to add expressiveness to their performance, imitating techniques found in non-keyboard instruments (like the guitar's string bend) or creating unique effects that are characteristic of electronic music.

5. **Instrument Response**: How a sound responds to pitch bend messages depends on the programming of the MIDI instrument or synthesizer. Some instruments might have very smooth and natural-sounding pitch transitions, while others might respond in a more stepped or quantized manner.

Pitch bend adds a dynamic and expressive element to MIDI performances, allowing for more nuanced and human-like phrasing, particularly in genres where subtle pitch variations are essential, like blues, jazz, or electronic music.

### Modulation 

**Modulation** typically refers to altering or shaping some aspect of the sound using various controls or signals. There are several ways in which modulation is used:

1. **MIDI Modulation Wheel (Mod Wheel)**: On MIDI keyboards, the modulation wheel is a common feature used to dynamically add expression to a performance. It's often assigned to control modulation depth of a particular parameter, like vibrato intensity or the depth of a filter sweep. The position of the wheel sends corresponding MIDI control change messages to modulate these parameters in real-time.

2. **Synthesizer Modulation**: In synthesizers, modulation involves using one signal (like an LFO - Low Frequency Oscillator) to alter another aspect of the sound (like pitch, filter frequency, or amplitude). For example, applying an LFO to a filter cutoff can create a sweeping effect, or modulating pitch can create vibrato.

3. **DAW Software Modulation**: In Digital Audio Workstations (DAWs), modulation can be applied through software tools to control various parameters of virtual instruments or effects over time. This could involve automation lanes, modulation matrices, or other modulation sources like envelopes or LFOs within software synths.

Modulation is a key tool in shaping and adding interest and variation to sounds in electronic music and sound design.

### MIDI Clock and synchronization 

A MIDI Clock is a form of MIDI signal used to synchronize tempo and timing between different MIDI devices. It's particularly important in setups involving multiple devices that need to operate in rhythmic sync, like sequencers, drum machines, arpeggiators, and software applications. Here are the key aspects of MIDI Clock:

1. **Timing Pulses**: The MIDI Clock sends out a continuous stream of timing pulses, which represent the tempo. These pulses are sent at a rate of 24 per quarter note (PPQN). Devices receiving the MIDI Clock use these pulses to align their tempo and timing.

2. **Start, Stop, and Continue Messages**: In addition to timing pulses, MIDI Clock includes start, stop, and continue messages. These signals control when the sequenced playback should begin, end, or resume, ensuring all connected devices follow the same sequence.

3. **Tempo Control**: The MIDI Clock itself doesn't specify the tempo in beats per minute (BPM); it just synchronizes devices to the same tempo. The actual BPM is usually set on the master device sending the MIDI Clock signal.

4. **Synchronization**: MIDI Clock is crucial for maintaining tight rhythmic synchronization, especially in live performance environments or when recording multiple devices into a DAW (Digital Audio Workstation).

5. **Limitations**: The MIDI Clock only carries tempo information. It does not transmit any start position data (which bar or beat to start on), so it's less suitable for syncing complex arrangements across devices. For more advanced synchronization, MIDI Time Code (MTC) is used, which includes song position information.

The MIDI Clock is an essential tool in electronic music production and live performance setups, enabling multiple devices and software applications to work together in time, creating a cohesive and synchronized sound.


