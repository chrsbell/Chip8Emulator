import simpleaudio
import numpy as np
from math import ceil
from scipy import signal

class AudioSynthesizer:
    def __init__(self):
        # Frequency in Hz
        self.frequency = 100
        self.rate = 44100

    def play_square_wave(self, duration):
        # Make sure number of samples for linspace is at least 1
        if duration <= 0:
            return
        samples = np.linspace(0, ceil(duration), ceil(duration) * self.rate, False)
        audio_array = signal.square(2 * np.pi * self.frequency * samples)
        # Use a fractional duration
        if duration < 1:
            max_index = int(len(audio_array) * duration)
            audio_array = audio_array[:max_index]
        # Constrain audio data to size of data type
        audio_array *= int(0xFFFF / 2) / np.max(np.abs(audio_array))
        audio_array = audio_array.astype(np.int16)
        simpleaudio.play_buffer(audio_array, 1, 2, self.rate)
