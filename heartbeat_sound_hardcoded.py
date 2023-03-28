import serial
from pydub import AudioSegment
from pydub.playback import play


user_heartbeats = []
single_beat_repetitions = 10
multiple_beat_repetitions = 5
bpm = [110, 75, 80, 48, 55]       
track = AudioSegment.empty()
single_heartbeat = AudioSegment.from_file("Downloads/single-heartbeat-sound-effect_qiBGgufL.mp3")
violin = AudioSegment.from_file("Downloads/violin.mp3")

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
                
        play((user_heartbeats[0] + 10).overlay(violin - 8))
        play((user_heartbeats[1] + 10).overlay(violin - 8))
        play((user_heartbeats[2] + 10).overlay(violin - 8))
        play((user_heartbeats[3] + 10).overlay(violin - 8))
        play((user_heartbeats[4] + 10).overlay(violin - 8))

        '''
        for i in range(5):
            track += user_heartbeats[i]

        play(heartbeat)
        track.export("Downloads/multiple_heartbeats_output.mp3", format="mp3")
        '''

# ser.close()
