import numpy as np
from IPython.display import Audio
from scipy.signal import butter, filtfilt
from scipy.io.wavfile import read, write
from scipy import signal

class InvalidInputError(Exception):
    pass

def genSine(freq, dur, fs=44100, amp=1, phi=0):
    t = np.arange(0, dur, 1/fs)
    return amp * np.sin(2*np.pi * freq * t + phi)

# push check

def genSaw(freq, dur, fs=44100, amp=1, phi=0):
    saw = genSine(freq, dur, fs, amp, phi)
    nyquist = fs / 2
    harms = int(nyquist / freq)
    for i in range (2, harms+1):
        saw += genSine(f=freq*i, amp=(amp*(1/i)), fs=fs, dur=dur, phi=phi)
    return saw

def genSquare(freq, dur, fs=44100, amp=1, phi=0):
    square = genSine(freq, dur, fs, amp, phi)
    nyquist = fs / 2
    harms = int(nyquist / freq)
    for i in range (3, harms+1, 2):
        square += genSine(f=freq*i, amp=(amp*(1/i)), fs=fs, dur=dur, phi=phi)
    return square

def genTriangle(freq, dur, fs=44100, amp=1, phi=0):
    triangle = genSine(freq, dur, fs, amp, phi)
    nyquist = fs / 2
    harms = int(nyquist / freq)
    for i in range (3, harms+1, 2):
        triangle += genSine(f=freq*i, amp=(amp*(1/i**2)), fs=fs, dur=dur, phi=phi)
    return triangle

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
    type = str(type)
    freq = float(freq)
    dur = float(dur)
    fs = float(fs)
    amp = float(amp)
    phi = float(phi)
    type_option = np.array(['sine', 'square', 'saw', 'triangle'])
    wave = np.array([])

    try:
        if (type in type_option) & (type(type) == str) & (freq < fs/2) & (freq > 0) & (amp >= 0) & (dur > 0) & (fs > 0):
            if type == 'sine':
                # create sinusoid
                wave = genSine(freq, dur, fs, amp, phi)
            elif type == 'saw':
                # create saw
                wave = genSaw(freq, dur, fs, amp, phi)
            elif type == 'square':
                # create square
                wave = genSquare(freq, dur, fs, amp, phi)
            elif type == 'triangle':
                # create triangle
                wave = genTriangle(freq, dur, fs, amp, phi)
            return Audio(wave, rate=fs)
        elif (type not in type_option):
            raise InvalidInputError('Type must be sine, square, saw, or triangle')
        elif(type(type) != str):
            raise InvalidInputError('Type must be a string')
        elif(freq >= fs/2):
            raise InvalidInputError('Frequency will cause aliasing')
        elif(freq <= 0):
            raise InvalidInputError('Frequency must be greater than 0')
        elif(amp < 0):
            raise InvalidInputError('Amplitude must be greater than or equal to 0')
        elif(dur <= 0):
            raise InvalidInputError('Duration must be greater than 0')
        elif(fs <= 0):
            raise InvalidInputError('Sampling frequency must be greater than 0')
    except InvalidInputError as e:
        return e        
    

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
    t = len(data)/fs

    a_time = ((attack/100) * t) * 1000
    d_time = ((decay/100) * t) * 1000
    r_time = ((release/100) * t) * 1000

    if a_time is None:
        a_time = (1/5 * t)
        print("Attack time not specified. a_time set to default of 1/5 of audio length.")

    if d_time is None:
        d_time = (1/5 * t)
        if sustain != None:
            print("Decay time not specified. d_time set to default of 1/5 of audio length.")

    if r_time is None:
        r_time = (1/5 * t)
        print("Release time not specified. r_time set to default of 1/5 of audio length.")
    elif r_time < 20 and not (t-0.02 <= a_time <= t):
        r_time = 20
        print("Release time must be at least 20ms. r_time set to 20ms.")
    elif (t-0.02 <= a_time <= t):
        r_time = t - a_time
        print("Attack time goes to within 20ms of end of audio signal. Release time set to amount of remaining ms, or: ", r_time)

    if a_time + d_time + r_time > t * 1000:
        a_time = (1/5 * t * 1000)
        d_time = (1/5 * t * 1000)
        r_time = (1/5 * t * 1000)
        print("Attack, decay and release time combine to a duration longer than input audio. Please input smaller values. Values set to defaults (each 1/5 of audio length).")

    if sustain is None: 
        a_samp = int(a_time * fs / 1000)
        d_samp = 0
        r_samp = int(r_time * fs / 1000)
        s_samp = 0
        zero_arr = np.zeros((len(data) - a_samp - d_samp - r_samp))
        zero_samp =len(zero_arr)
        env_samp = a_samp + d_samp + r_samp + s_samp + zero_samp #for error handling only
        print("No sustain input. Sustain and decay parameters nullified, only attack and release applied. Amplitude of 0 applied to remainder of audio.")
    else: 
        a_samp = int(a_time * fs / 1000)
        d_samp = int(d_time * fs / 1000)
        r_samp = int(r_time * fs / 1000)
        s_samp = int(len(data) - a_samp - d_samp - r_samp)
        zero_arr = []
        zero_samp = len(zero_arr)
        env_samp = a_samp + d_samp + r_samp + s_samp + zero_samp #for error handling only

    if env_samp != len(data) and s_lvl is None:
       zero_arr = np.zeros(len(data) - a_samp - d_samp - r_samp + (len(data) - env_samp))
       zero_samp = len(zero_arr)
       env_samp = a_samp + d_samp + r_samp + s_samp + zero_samp
    else: 
       s_samp = s_samp + (len(data) - env_samp)
       env_samp = a_samp + d_samp + r_samp + s_samp + zero_samp
    #Compensates envelope length in case of length inconsistency in envelope array and original audio array caused by truncation by the int function.

    if sustain is None:
        a = np.linspace(0, 1, a_samp)
        r = np.linspace(1, 0, r_samp)
        z = np.full(len(zero_arr), 0)
        env = np.concatenate([a,r,z])
    else: 
        a = np.linspace(0, 1, a_samp)
        d = np.linspace(1, sustain, d_samp)
        s = np.full(s_samp, sustain)
        r = np.linspace(sustain, 0, r_samp)
        env = np.concatenate([a,d,s,r])

    sig = env * data
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
    carrier_type = str(carrier_type)
    carrier_freq = float(carrier_freq)
    mod_depth = float(mod_depth)
    mod_ratio = float(mod_ratio)
    dur = float(dur)
    fs = float(fs)
    amp = float(amp)
    modulator_type = str(modulator_type)
    try:
        if (mod_depth >= 0) & (mod_ratio > 0):
            carrier = gen_wave(carrier_type, carrier_freq, dur, fs=fs)
            modulator = 1 + gen_wave(modulator_type, carrier_freq*mod_ratio, dur, fs=fs)
            sig = carrier * (mod_depth * modulator)
            return sig
        elif (mod_depth < 0):
            raise InvalidInputError('Modulation depth must be greater than or equal to 0.')
        elif (mod_ratio <= 0):
            raise InvalidInputError('MOdulation ratio must be greater than 0.')
    except InvalidInputError as e:
        print(e)


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
    type = str(type)
    cutoff_freq = float(cutoff_freq)
    fs = float(fs)
    order = int(order)
    type_option = np.array(['lowpass', 'highpass'])
    nyq = 0.5 * fs
    normal_cuttoff = cutoff_freq / nyq

    #AI SHIT: if band pass/band stop, cutoff_freq should be a list of two frequencies, and normal_cutoff should be a list of two values. Also, type_option should include bandpass and bandstop. Then, in the if statement, you would need to check if type is in the new type_option, and if type is bandpass or bandstop, then use the new normal_cutoff and btype in the butter function.
    #should be an array rather than a float (cutoff for bandpass/bandstop 
    try:
        if (type in type_option) & (type(type) == str) & (cutoff_freq > 0) & (fs > 0) & (order > 0 and order <= 6):
           nyq = 0.5 * fs
           normal_cuttoff = cutoff_freq / nyq 
           (b, a) = butter(order, normal_cuttoff, btype=type, fs=fs)
           sig = filtfilt(b, a, data)
           return sig
        elif (type not in type_option):
            raise InvalidInputError('Type must be lowpass or highpass')
        elif (type(type) != str):
            raise InvalidInputError('Type must be a string')
        elif (cutoff_freq <= 0):
            raise InvalidInputError('Cutoff frequency must be greater than 0')
        elif (fs <= 0):
            raise InvalidInputError('Sampling frequency must be greater than 0')
        elif (order <= 0 or order > 6):
            raise InvalidInputError('Order must be between 1 and 6')
    except InvalidInputError as e:
        return e

def convert_to_float(file):
    file_c = file.astype(np.float32, order='C')/32768.0 #divide by max int
    return(file_c)

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
    convert_to_float(data)
    convert_to_float(ir)
    sig = np.convolve(data, dry_wet * ir)
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
    data = data / abs(data).max()
    copy = data.copy()
    pad = np.zeros(int(fs/1000*delay_time))
    orig = np.concatenate((data, pad))
    delay = np.concatenate((pad, copy))
    sig = orig + (dry_wet * delay)
    return sig
