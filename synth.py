import numpy as np
from scipy.io.wavfile import read, write
from scipy import signal
import pretty_midi
import synth_helpers


def parse_midi():
    """
    MIDI PARSER
    This will parse to by monophonic (even if the file is not). There are ways to make this monophonic "conversion" a lot better, 
    but right now it just lines up all the notes sequentially.

    Returns:
    A list of notes in the file. A single note is represented as a tuple (frequency, duration, amplitude)
    """

    midi_path = input("Enter MIDI file path: ")
    midi_data = pretty_midi.PrettyMIDI(midi_path)
    instrument = midi_data.instruments[0]
    midi_notes = []
    for note in instrument.notes:
        pitch = note.pitch
        freq = 440 * 2**((pitch-69)/12)
        dur = note.duration
        vel = note.velocity
        amp = vel/127
        midi_notes.append((freq, dur, amp))
    return midi_notes

# TODO: The function below controls the command line interface and collects the user's desired synth parameters. It takes in user data at the command line,
# and stores it in a Python dictionary called synth_params. You will modify synth_params if you add new parameters/controls.
# In my default, I have reverb as my effect. You can change this to be a filter or delay. You can also add more parameters rather than just on/off.
# You will also modify the preset params with your 2 presets.
def params_CLI():
    """
    Prompts the user on the command line for desired synthesis parameters.

    Returns:
    A dictionary of parameters and associated values, including sampling rate, adsr params, effect params, and sound generator params.
    """

    # DEFINE SYNTH PARAMS DICTIONARY
    synth_params = {
        'fs': 44100,
        'osc_type': 'sine',
        'modulation': 'none',
        'mod_ratio': 0,
        'mod_index': 0,
        'reverb': False,
        'adsr': (20, 20, 0.8, 30) 
    }

    # SET SYNTH PARAMS
    synth_params['fs'] = int(input("Output sample rate (max 48000): "))

    print("\nChoose a playback mode:")
    print("1 - Preset 1: MyPresetName")
    print("2 - Preset 2: MyPresetName")
    print("3 - Custom sound")
    mode = int(input("> "))

    if mode == 1:
        # TODO: UPDATE WITH YOUR PRESET PARAMS

        synth_params['osc_type'] = 'sine'
        synth_params['modulation'] = 'none'
        synth_params['mod_ratio'] = 0
        synth_params['mod_index'] = 0
        synth_params['reverb'] = False
        synth_params['adsr'] = (60, 20, 0.8, 20)
    
    elif mode == 2:
        # TODO: UPDATE WITH YOUR PRESET PARAMS

        synth_params['osc_type'] = 'sine'
        synth_params['modulation'] = 'none'
        synth_params['mod_ratio'] = 0
        synth_params['mod_index'] = 0
        synth_params['reverb'] = False
        synth_params['adsr'] = (50, 10, 0.8, 10)

    elif mode == 3:

        # SOUND GENERATOR
        print("\nChoose your oscillator:")
        print("1 - Sine")
        print("2 - Saw")
        print("3 - Square")
        print("4 - Triangle")
        osc = int(input("> "))
        if osc == 1:
            synth_params['osc_type'] = 'sine'
        elif osc == 2:
            synth_params['osc_type'] = 'saw'
        elif osc == 3:
            synth_params['osc_type'] = 'square'
        elif osc == 4:
            synth_params['osc_type'] = 'triangle'
        else:
            print("\nChoose your oscillator:")
            print("1 - Sine")
            print("2 - Saw")
            print("3 - Square")
            print("4 - Triangle")
        
        # MODULATION
        print("\nUse modulation synthesis?:")
        print("1 - FM")
        print("2 - AM")
        print("3 - None")
        mod = int(input("> "))
        if mod == 1:
            synth_params['modulation'] = 'fm'
        elif mod == 2:
            synth_params['modulation'] = 'am'
        elif mod == 3:
            synth_params['modulation'] = 'none'
        else:
            print("\nAdd modulation synthesis?:")
            print("1 - FM")
            print("2 - AM")
            print("3 - None")

        if mod == 1 or mod == 2:
            mod_index = float(input("Set modulation index: "))
            mod_ratio = float(input("Set modulator harmonicity ratio: "))
            synth_params['mod_index'] = mod_index
            synth_params['mod_ratio'] = mod_ratio
        
        # ADSR
        print("\nSet ADSR. Enter values from 0-100 as percentages for attach, decay, release. Enter a value between 0-1 for sustain amplitude.")
        attack = float(input("Attack (0-100): "))
        decay = float(input("Decay (0-100): "))
        sustain = float(input("Sustain (0-1): "))
        release = float(input("Release (0-100): "))
        synth_params['adsr'] = (attack, decay, sustain, release)
        
        # EFFECTS
        print("\nAdd reverb?:")
        print("1 - Yes")
        print("2 - No")
        reverb = int(input("> "))
        if reverb == 1:
            synth_params['reverb'] = True
        elif reverb == 2:
            synth_params['reverb'] = False

    return(synth_params)

# TODO: Complete this function. 
# You should call functions from synth_helpers to create a single note.
# Hint: You will want your sound generator/modulation synthesis here along with your ADSR at a minimum.
def gen_note(freq, dur, amp, synth_params):
    fs = synth_params['fs']
    osc_type = synth_params['osc_type']
    note = synth_helpers.gen_wave(osc_type, freq, dur, fs, amp)
    return note


# TODO: Update this function. 
# You should call functions from synth_helpers and the gen_note function above to create your audio array. 
# I've provided starter code for stepping through the note_list created by parse_midi, but you may want to modify depending on your signal flow and params.
# Think about the order you want to apply the functions. Also think about what should be applied to the note level vs the file level.
def synth(note_list, synth_params):
    song = np.array([])
    for note in note_list:
        freq = note[0]
        dur = note[1]
        amp = note[2]
        synth_note = gen_note(freq, dur, amp, synth_params)
        # Though I'm not a huge fan of appending/concatenating, it is okay for this assignment. 
        # If you choose to pre-allocate (correctly), you'll recieve extra credit.
        song = np.concatenate((song, synth_note))
   
    # TODO: Update this. This is just an example for reading into the synth_params dictionary
    if synth_params['reverb']: # remember reverb will be true/false in my example
        song = synth_helpers.reverb(song, 'file_path')

    return song



def create_file(audio_data, fs):
    # OUTPUT PATH
    print("\n Enter the desired output file name. The file will be created in this directory.")
    file_name = input("> ")
    if not file_name.endswith('.wav'):
        file_name = file_name + '.wav'
    write(file_name, fs, audio_data)
    print("\n File created!")

def main():
    # MIDI Input and parsing
    note_list = parse_midi()

    # Synth parameter setting
    synth_params = params_CLI()

    # Synthesis
    audio_data = synth(note_list, synth_params)

    # Write to file
    create_file(audio_data, synth_params['fs'])


if __name__ == "__main__":
    main()
