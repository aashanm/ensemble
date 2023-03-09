from serial import Serial
import time
import os
from pydub import AudioSegment
from pydub.playback import play

# ser = Serial('COM4', 9600)
# time.sleep(2)

# read and record the data from the Arduino Serial Monitor
'''
https://pythonforundergradengineers.com/python-arduino-potentiometer.html#use-the-python-repl-to-read-the-potentiometer

data = []                      # empty list to store the data
for i in range(50):
    b = ser.readline()         # read a byte string
        string_n = b.decode()  # decode byte string into Unicode  
    string = string_n.rstrip() # remove \n and \r
    flt = float(string)        # convert string to float
    data.append(flt)           # add to the end of data list
    time.sleep(0.1)            # wait (sleep) 0.1 seconds

ser.close()
'''

# hard coded test values
bpm = [60, 75, 90, 115, 47]
delays = [60/x for x in bpm]
duration = 3000 # in milliseconds
suggested_frequencies = [334, 689, 839, 892, 1452, 1560, 1823, 3154, 3208, 3406, 3595, 3607, 4005, 4176, 4338, 4754, 5408, 5782, \
                         6500, 6697, 7009] # in Hertz

heartbeat_sounds = []
heartbeat_sounds.append(AudioSegment.from_file("Downloads/single-heartbeat-sound-effect_qiBGgufL.mp3"))

user_heartbeats = []
user_heartbeats.append((heartbeat_sounds[0] + AudioSegment.silent(duration=delays[0]*1000)) * 3)
for i in range(1, 5):
    user_heartbeats.append(user_heartbeats[i-1].overlay((heartbeat_sounds[0] + AudioSegment.silent(duration=delays[i]*1000)) * 3, position=delays[i]*1000))

track = AudioSegment.empty() # for exporting
for i in range(5):
    play(user_heartbeats[i])
    track += user_heartbeats[i]

track.export("Downloads/multiple_heartbeats_output.mp3", format="mp3")

# play frequency noises (Chladni plate)
'''
for i in range(len(bpm)):
  print(os.system('play -n synth %s sin %s' % (duration/1000, suggested_frequencies[i])))
'''
