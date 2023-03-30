import serial
from pydub import AudioSegment
import sounddevice as sd
import soundfile as sf
import random
import numpy as np

user_heartbeats = []
single_beat_repetitions = 10
multiple_beat_repetitions = 5
bpm = [110, 75, 80, 48, 55]       
track = AudioSegment.empty()
single_heartbeat = AudioSegment.from_file("Downloads/single-heartbeat-sound-effect_qiBGgufL.mp3")

frequencies = [240, 280, 330, 540, 600, 620, 910, 1210, 1360, 1460, 1760, 2150, 2430, 2560, 2710, 3000, 3190, 3710, 3830, 3920]
volumes = [35, 35, 30, 35, 45, 45, 45, 45, 45, 40, 45, 45, 45, 45, 55, 45, 50, 45, 50, 55]
freq_vol_pairs = dict(zip(frequencies, volumes))
freq_duration_sec = 1.5
sampling_freq = 44100

frequency_speaker_id = 0
heartbeat_speaker_id = 2

def open_serial_port(port_name):
    ser = serial.Serial(port=port_name, baudrate=9600)
    return ser

'''
try:
    ser = open_serial_port('/dev/cu.usbmodem1101')
except:
    ser = open_serial_port('/dev/cu.usbmodem101')
'''

for i in range(1000):
    # line = ser.readline()      
    # if line:
        # string = line.decode()   
        # num = int(string)         
        # print(num)

        # bpm.insert(0, num)      
        # bpm.pop(5)
        print(bpm)

        delays = [60/x for x in bpm]

        user_heartbeats.append((single_heartbeat + AudioSegment.silent(duration=delays[0] * 1000)) * single_beat_repetitions)
        current_heartbeat_for_repetition = (single_heartbeat + AudioSegment.silent(duration=delays[0] * 1000)) * multiple_beat_repetitions

        for i in range(1, 5):
            if i == 1:
                user_heartbeats.append(current_heartbeat_for_repetition.overlay(((single_heartbeat) + AudioSegment.silent(duration=delays[i] * 1000)) 
                    * multiple_beat_repetitions, position=delays[i] * 1000))
            else:
                user_heartbeats.append(user_heartbeats[i-1].overlay(((single_heartbeat) + AudioSegment.silent(duration=delays[i] * 1000)) 
                    * multiple_beat_repetitions, position=delays[i] * 1000))
                
        grouped_frequencies = [frequencies[i:i+4] for i in range(0, len(frequencies), 4)]
        selected_frequencies = [random.choice(group) for group in grouped_frequencies]
                
        for i, clip in enumerate(user_heartbeats):
            clip.export("temp.wav", format="wav")
            audio_data, sample_rate = sf.read("temp.wav", dtype='float32')
            sd.play(audio_data, sample_rate, device=heartbeat_speaker_id)
            sd.wait()

            t = np.linspace(0.0, freq_duration_sec, int(freq_duration_sec * sampling_freq), endpoint=False)
            waveform = (freq_vol_pairs[selected_frequencies[i]] - 100) * np.sin(2.0 * np.pi * selected_frequencies[i] * t)
            sd.play(waveform, sampling_freq, device=frequency_speaker_id)
            sd.wait()

        '''
        for i in range(5):
            track += user_heartbeats[i]

        play(heartbeat)
        track.export("Downloads/multiple_heartbeats_output.mp3", format="mp3")
        '''

# ser.close()
