import simpleaudio
import numpy as np


class AudioSynthesizer:
    def __init__(self):
        # Frequency in Hz
        self.frequency = 440
        self.rate = 44100

    def play_square_wave(self, duration):
        samples = np.linspace(0, duration, duration * self.rate, False)
        audio_array = np.sin(self.frequency * samples * 2 * np.pi)
        # Constrain audio data to size of data type
        audio_array *= int(0xFFFF / 2) / np.max(np.abs(audio_array))
        audio_array = audio_array.astype(np.int16)
        play_obj = simpleaudio.play_buffer(audio_array, 1, 2, self.rate)
        play_obj.wait_done()