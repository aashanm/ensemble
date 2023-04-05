import serial
from pydub import AudioSegment
import sounddevice as sd
import soundfile as sf
import random
import numpy as np
import time
import threading

heartbeat_sounds = []
num_beats = 4
num_beat_repetitions = 3
bpm = [110, 75, 80, 48, 55] 
track = AudioSegment.empty()
single_heartbeat = AudioSegment.from_file("Downloads/single-heartbeat-sound-effect_qiBGgufL.mp3")

tier_2_frequencies = [145, 150, 160, 220, 225, 255, 320, 450, 535]
tier_3_frequencies = [625, 735, 825, 1100, 1350, 1380, 1440, 1600, 1750]
tier_4_frequencies = [2200, 2230, 2310, 2530, 2830, 3090, 3110, 3200, 3320]
tier_5_frequencies = [3620, 3630, 3790, 4130, 4450, 4540, 4640, 4820, 4860]
volume = 2
freq_duration_sec = 1.0
sampling_freq = 44100
frequencies_to_play = []

frequency_speaker_id = 2
heartbeat_speaker_id = 4

def open_serial_port(port_name):
    ser = serial.Serial(port=port_name, baudrate=9600)
    time.sleep(2)
    return ser

'''
try:
    ser = open_serial_port('/dev/cu.usbmodem1101')
except:
    ser = open_serial_port('/dev/cu.usbmodem101')
'''

lock = threading.Lock()

def play_audio_pairing(audio, delay, device):
    print(f"Playing audio {audio} with delay {delay} on device {device}")
    # load heartbeat sound
    audio.export("temp.wav", format="wav")
    audio_data, sample_rate = sf.read("temp.wav", dtype='float32')
    
    if delay > 0:
        padding = np.zeros((int(delay * sample_rate), audio_data.shape[1]))
        audio_data = np.concatenate((padding, audio_data), axis=0)
    
    # Play audio file on the specified sound device
    sd.play(audio_data, sample_rate, device=device)
    sd.wait()
    print(f"Finished playing audio {audio}")



while True:
    '''
    line = ser.readline()      
    if line:
        string = line.decode()   
        ser.write('\x0c'.encode())
    '''
    current_user_bpm = 69    
    print(current_user_bpm)

    # add latest user's bpm to memory and remove 5th last bpm
    bpm.insert(0, current_user_bpm)      
    bpm.pop(5)
    print(bpm)

    delays = [60/x for x in bpm]
    
    # generate user heartbeat sound
    for i in range(num_beat_repetitions):
        heartbeat_sounds.append((single_heartbeat + AudioSegment.silent(duration=delays[0] * 1000)) * num_beats)
    current_heartbeat_for_repetition = (single_heartbeat + AudioSegment.silent(duration=delays[0] * 1000)) * num_beats

    # generate combined heartbeat sounds
    for i in range(1, 5):
        if i == 1:
            for i in range(num_beat_repetitions):
                heartbeat_sounds.append(current_heartbeat_for_repetition.overlay(((single_heartbeat) + AudioSegment.silent(duration=(delays[i] * 1000))) 
                    * num_beats, position=(delays[i] * 1000)))
        else:
            for i in range(num_beat_repetitions):
                heartbeat_sounds.append(heartbeat_sounds[i-1].overlay(((single_heartbeat) + AudioSegment.silent(duration=(delays[i] * 1000))) 
                    * num_beats, position=(delays[i] * 1000)))
            
    # add frequency aligned with user heartbeat
    if current_user_bpm <= 50:
        frequencies_to_play.append([50] * num_beat_repetitions)
    elif 87 <= current_user_bpm <= 105:
        if abs(current_user_bpm - 86) < abs(current_user_bpm - 106):
            frequencies_to_play.append([86] * num_beat_repetitions)
        else: 
            frequencies_to_play.append(106)
    else:
        frequencies_to_play.append([current_user_bpm] * num_beat_repetitions)

    # add 1 random frequency from each tier
    frequencies_to_play.append([random.choice(tier_2_frequencies)] * num_beat_repetitions)
    frequencies_to_play.append([random.choice(tier_3_frequencies)] * num_beat_repetitions)
    frequencies_to_play.append([random.choice(tier_4_frequencies)] * num_beat_repetitions)
    frequencies_to_play.append([random.choice(tier_5_frequencies)] * num_beat_repetitions)

    frequencies_to_play = [freq for sublist in frequencies_to_play for freq in sublist]
    print(frequencies_to_play)

    frequency_audio = []
    for freq in frequencies_to_play:
        t = np.linspace(0.0, freq_duration_sec, int(freq_duration_sec * sampling_freq), endpoint=False)
        waveform = (volume) * np.sin(2.0 * np.pi * freq * t)
        frequency_audio.append(waveform)
            
    # play heartbeat sound and frequency noises simultaneously
    threads = []
    for i in range(len(heartbeat_sounds)):
        heartbeat_sound = heartbeat_sounds[i]
        frequency_noise = frequency_audio[i % len(frequencies_to_play)]
        delay = heartbeat_sound.duration_seconds - freq_duration_sec
        thread = threading.Thread(target=play_audio_pairing, args=(heartbeat_sound, delay, heartbeat_speaker_id))
        threads.append(thread)
        thread.start()
        thread = threading.Thread(target=play_audio_pairing, args=(frequency_noise, 0, frequency_speaker_id))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    frequencies_to_play.clear()
    frequency_audio.clear()
    heartbeat_sounds.clear()


    # ser.write('\x0c'.encode())

    '''
    for i in range(5):
        track += user_heartbeats[i]

    play(heartbeat)
    track.export("Downloads/multiple_heartbeats_output.mp3", format="mp3")
    '''

# ser.close()
