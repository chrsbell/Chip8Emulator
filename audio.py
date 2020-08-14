import pyaudio
import numpy as np


class AudioSynthesizer:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.volume = 0.5
        self.rate = 44100
        self.frequency = 440.0

    def play_square_wave(self, duration):
        samples = (np.sin(2 * np.pi * np.arange(self.frequency * duration) * self.frequency / self.rate)).astype(
            np.float32)
        stream = self.audio.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=self.rate,
                        output=True)
        stream.write(self.volume * samples)
        stream.stop_stream()
        stream.close()

    def close(self):
        self.audio.terminate()
