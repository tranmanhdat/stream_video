import pyaudio
import keyboard
import numpy as np
from scipy.io import wavfile
import sys

class Recorder:
    def __init__(self, filename):
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.sample_rate = 16000
        self.chunk = int(0.03*self.sample_rate)
        self.filename = filename
        self.START_KEY = 's'
        self.STOP_KEY = 'q'


    def record(self):
        recorded_data = []
        p = pyaudio.PyAudio()

        stream = p.open(format=self.audio_format, channels=self.channels,
                        rate=self.sample_rate, input=True,
                        frames_per_buffer=self.chunk)
        while(True):
            data = stream.read(self.chunk)
            # sys.stdout.buffer.write(data)
            recorded_data.append(data)
            if keyboard.is_pressed(self.STOP_KEY):
                print("Stop recording")
                # stop and close the stream
                stream.stop_stream()
                stream.close()
                p.terminate()
                #convert recorded data to numpy array
                recorded_data = [np.frombuffer(frame, dtype=np.int16) for frame in recorded_data]
                wav = np.concatenate(recorded_data, axis=0)
                wavfile.write(self.filename, self.sample_rate, wav)
                print("You should have a wav file in the current directory")
                break


    def listen(self):
        print("Press {} to start and {} to quit!".format(self.START_KEY,self.STOP_KEY))
        while True:
            # if keyboard.is_pressed(self.START_KEY):
            self.record()
            break
if __name__ == '__main__':
    recorder = Recorder("mic.wav") #name of output file
    recorder.listen()