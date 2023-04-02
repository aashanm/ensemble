'''
Steps to run:

1. open Terminal through top bar menu (Terminal -> New Terminal)
2. type command in Terminal: python3 tone_generator.py (or press the up arrow)
3. press enter to run

Steps to edit:

1. Make edit
2. Ctrl + S to save changes

Steps to stop run:

1. Delete icon in Terminal
or Ctrl + Z
'''

import osascript
import time
import sounddevice as sd
import sounddevice as sd
import numpy as np

freq_duration_sec = 1
sampling_freq = 44100

frequency_speaker_id = 0

frequencies = [60, 106, 126, 130, 145, 150, 160, 220, 225, 255, 320, 450, 535, 625, 735, 825, 1100, 1350, 1380, 1440, 1600, 1750,
               2200, 2230, 2310, 2530, 2830, 3090, 3110, 3200, 3320, 3620, 3630, 3790, 4130, 4450, 4540, 4640, 4820, 4860, 5040]

# edit variable (i.e. 60) below with frequency of choice for +/-5 frequencies (i.e. 55-65)
frequencies = list(range(60-5, 60+6))
volumes = [5] * len(frequencies)
freq_vol_pairs = dict(zip(frequencies, volumes))

# correspond to frequencies above
#            1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28
# volumes = [55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 65, 63, 53, 55, 65, 50, 55, 45, 45, 45, 55, 45, 50, 45, 50, 55]

# play series of tones for (duration_sec, at n frequency in list)
for i, frequency in enumerate(frequencies):
   osascript.osascript("set volume output volume " + str(15))
   t = np.linspace(0.0, freq_duration_sec, int(freq_duration_sec * sampling_freq), endpoint=False)
   waveform = (freq_vol_pairs[frequency]) * np.sin(2.0 * np.pi * frequency * t)
   sd.play(waveform, sampling_freq, device=frequency_speaker_id)
   sd.wait()

# play single tone for duration_sec at specified frequency and volume
'''
frequency = 60
volume = 5

osascript.osascript("set volume output volume " + str(15))
t = np.linspace(0.0, freq_duration_sec, int(freq_duration_sec * sampling_freq), endpoint=False)
waveform = (volume) * np.sin(2.0 * np.pi * frequency * t)
sd.play(waveform, sampling_freq, device=frequency_speaker_id)
'''
