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
        play_obj = simpleaudio.play_buffer(audio_array, 1, 2, self.rate)
        play_obj.wait_done()