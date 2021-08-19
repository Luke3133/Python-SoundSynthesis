"""
This is a Python project which outputs an infinitely long sine wave, programmed by Emily Glover.
It works by using callbacks from pyaudio to request the next set of data for the buffer.
The SineOscillator class could be instantiated many times with different frequencies. To output the sum of waves,
an oscillator controller class should be produced which can get the frame across all active oscillators.
"""
import numpy as np
import pyaudio

BUFFER_SIZE = 1024  # How many samples to send to the audio processor buffer
SAMPLE_RATE = 44100  # How many samples per second to generate
NOTE_AMP = 0.5  # Master volume
freq = 200  # The frequency of the note we wish to produce


class SineOscillator:
    # This produces a single instance of a sine oscillator. To use multiple oscillators per voice or multiple voices
    # with sine waves, we must create instances for each oscillator.
    def __init__(self, Frequency, Samplerate=SAMPLE_RATE, Position=0):
        self.Frequency = Frequency  # Frequency of the oscillator
        self.SampleRate = Samplerate  # Sample rate of project
        # Keep track of how much of the wave has been sent to the buffer already
        # i.e. upon sending the first lot of data, we have sent BUFFER_SIZE samples. Therefore,
        # Position will equal BUFFER_SIZE so that next time we can send BUFFER_SIZE+1 to 2*BUFFER_SIZE.
        self.Position = Position


    def getframe(self):
        # This function returns the next set of samples to the callback
        increment = (2 * np.pi * self.Frequency) / self.SampleRate  # Calculate a single sample
        # The output returns a list which contains the samples in the range(position, position+buffer)
        output = [count * increment for count in range(self.Position, self.Position + BUFFER_SIZE)]
        self.Position += BUFFER_SIZE  # Increase the position ready for the next callback
        return np.sin(output)  # Return the sin of the output


Osc1 = SineOscillator(freq)  # Instantiate the class SineOscillator with frequency freq


# The function callback is called when the audio buffer is ready to be filled with more data.
def callback(in_data, frame_count, time_info, status):
    # Osc1.getframe will return an array of numbers with length BUFFER_SIZE
    # The data is then converted to float16 which is required by pyaudio
    data = np.array(Osc1.getframe()).astype(np.float16)
    # Return the data and also tell pyaudio to fill the buffer and continue playing
    return data, pyaudio.paContinue


# The following lines open the audio stream and use stream_callback to call the above function when the buffer is ready
# to receive more audio.
p = pyaudio.PyAudio()
stream = p.open(
    rate=SAMPLE_RATE,
    channels=1,
    format=pyaudio.paInt16,
    output=True,
    frames_per_buffer=BUFFER_SIZE,
    stream_callback=callback
)
stream.start_stream()

# The following code is used to keep the program looping forever. To end the project early, add an event listener and
# update x to be greater than y.
x, y = 1, 2
try:
    while True:
        if x > y:
            print("true")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
