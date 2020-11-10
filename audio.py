"""
MIT License

Copyright (c) 2020 Chris Bell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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
        # play_obj = simpleaudio.play_buffer(audio_array, 1, 2, self.rate)
        # play_obj.wait_done()