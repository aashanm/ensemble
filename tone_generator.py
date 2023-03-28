# https://stackoverflow.com/questions/43904019/how-can-i-make-sound-with-frequency-in-python3

import os
import osascript
import time
import sounddevice as sd

print(sd.query_devices())

duration_sec = 0.8
frequencies = [240, 
               280, 
               330, 
               540, 
               600,
               620,
               #720 (not on list)
               910,
               1210,
               1360,
               1460,
               1760, 
               2150,
               2430, 
               2560,
               2710, 
               3000,
               3190,
               # 3430 (not on list)
               3710,
               3830,
               3920
               ]

volumes = [35, 35, 30, 35, 45, 45, 45, 45, 45, 40, 45, 45, 45, 45, 55, 45, 50, 45, 50, 55]

osascript.osascript("set volume output volume 35")

'''
for i, n in enumerate(frequencies):
    osascript.osascript("set volume output volume " + str(volumes[i]))
    print(os.system('play -n synth %s sin %s' % (duration_sec, n)))
'''

