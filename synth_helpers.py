import numpy as np
from scipy.io.wavfile import read, write
from scipy import signal


# TODO: Replace the code below with your implementation of the waveforms.
# Hint: You may want to write more helper functions to create the waveforms
# Note: How will you handle aliasing?
def gen_wave(type, freq, dur, fs=44100, amp=1, phi=0):
    """
    Args:
    type (str) = waveform type: 'sine', 'square', 'saw', or 'triangle'
    freq (float) = fundamental frequency in Hz
    dur (float) = duration of the sinusoid (in seconds)
    fs (float) = sampling frequency of the sinusoid in Hz
    amp (float) = amplitude of the fundamental
    phi (float) = initial phase of the wave in radians
    Returns:
    The function should return a numpy array
    wave (numpy array) = The generated waveform
    """
  
    wave = np.array([])

    if type == 'sine':
        # create sinusoid
        wave = amp * np.sin(2*np.pi*freq*np.arange(0,dur,1/fs) + phi)
    elif type == 'saw':
        # create saw
        wave = np.array([])
    elif type == 'square':
        # create square
        wave = np.array([])
    elif type == 'triangle':
        # create triangle
        wave = np.array([])
    return wave
    

# TODO: Replace the code below with your implementation of an ADSR
# Hint: If you use %'s for your ADSR lengths, what length should the sustain value be
# Note: How will you handle percentages that are too long? For example, attack is 50, decay is 50, release is 50?
def adsr(data, attack, decay, sustain, release, fs=44100):
    """
    Args:
    data (np.array) = signal to be modified
    attack (float) = value between 0-100 representing what percentage of the note duration the attack should be
    decay (float) = value between 0-100 representing what percentage of the note duration the attack should be
    sustain (float) = value between 0-1 representing the amplitude of the sustain
    release (float) = value between 0-100 representing what percentage of the note duration the attack should be
    fs (float) = sampling frequency of the sinusoid in Hz
    Returns:
    The function should return a numpy array
    sig (numpy array) = the modified, enveloped signal
    """
    sig = data
    return sig


# TODO: Replace the code below with your implementation of a FM synthesis
# Hint: You should really be doing PM.
def fm_synth(carrier_type, carrier_freq, mod_index, mod_ratio, dur, fs=44100, amp=1, modulator_type='sine'):
    """
    Args:
    carrier_type (str) = carrier waveform type: 'sine', 'square', 'saw', or 'triangle'
    carrier_freq (float) = frequency of carrier in Hz
    mod_index (float) = index of modulation
    mod_ratio (float) = modulation ratio, where modulator frequency = carrier_freq * mod_ratio
    dur (float) = duration of the sinusoid (in seconds)
    fs (float) = sampling frequency of the sinusoid in Hz
    amp (float) = amplitude of the carrier
    modulator_type (str) = modulator waveform type: 'sine', 'square', 'saw', or 'triangle'

    Returns:
    The function should return a numpy array
    sig (numpy array) = frequency modulated signal
    """
    sig = gen_wave(carrier_type, carrier_freq, dur, fs=fs)
    return sig

# TODO: Replace the code below with your implementation of a AM synthesis
def am_synth(carrier_type, carrier_freq, mod_depth, mod_ratio, dur, fs=44100, amp=1, modulator_type='sine'):
    """
    Args:
    carrier_type (str) = carrier waveform type: 'sine', 'square', 'saw', or 'triangle'
    carrier_freq (float) = frequency of carrier in Hz
    mod_depth (float) = depth of the modulator
    mod_ratio (float) = modulation ratio, where 1:mod_ratio is C:M
    dur (float) = duration of the sinusoid (in seconds)
    fs (float) = sampling frequency of the sinusoid in Hz
    amp (float) = amplitude of the carrier
    modulator_type (str) = modulator waveform type: 'sine', 'square', 'saw', or 'triangle'

    Returns:
    The function should return a numpy array
    sig (numpy array) = amplitude modulated signal
    """
    sig = gen_wave(carrier_type, carrier_freq, dur, fs=fs)
    return sig


# TODO: Complete at least one of the functions below: filter, reverb, delay.

# Note: I wrote this to only create low or highpass filters. You can alter to create bandpass/bandstop, but do not change the function definition.
def filter(data, type, cutoff_freq, fs=44100, order=5):
    """
    Args:
    data (np.array) = signal to be modified
    type (str) = filter type 'lowpass' or 'highpass'
    cutoff_freq (float) = cutoff frequency in Hz
    fs (float) = sampling frequency of the sinusoid in Hz
    order (int) = filter order

    Returns:
    The function should return a numpy array
    sig (numpy array) = filtered signal
    """
    sig = data
    return sig

def reverb(data, ir, dry_wet=0.5):
    """
    Args:
    data (np.array) = signal to be modified
    ir (str) = file path to impulse response
    dry_wet (float) = value between 0-1 dry/wet balance

    Returns:
    The function should return a numpy array
    sig (numpy array) = signal with reverb
    """
    sig = data
    return sig

def delay(data, delay_time, dry_wet=0.5, fs=44100):
    """
    Args:
    data (np.array) = signal to be modified
    delay_time (float) = delay time in seconds
    dry_wet (float) = value between 0-1 dry/wet balance
    fs (float) = sampling frequency of the sinusoid in Hz

    Returns:
    The function should return a numpy array
    sig (numpy array) = signal with a delay
    """
    sig = data
    return sig
