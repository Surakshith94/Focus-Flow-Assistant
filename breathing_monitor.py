import pyaudio
import numpy as np
import time
""" 
Sound is a wave. "Loudness" is the height (amplitude) of the wave.

When you breathe into a mic, it creates a loud "wind" noise.

We need to calculate the RMS (Root Mean Square) of the audio chunk. This effectively gives you the "average volume."
"""

def measure_noise_level(stream, seconds=2, chunk=1024):
    values = []
    start = time.time()
    print("Stay quiet, calibrating noise level...")
    while time.time() - start < seconds:
        data = stream.read(chunk, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        rms = np.sqrt(np.mean(audio_data ** 2))
        values.append(rms)
    noise_mean = np.mean(values)
    print("Noise RMS ≈", noise_mean)
    return noise_mean

def detect_exhale(duration=5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    # 1) measure background
    noise_level = measure_noise_level(stream, seconds=2, chunk=CHUNK)

    # 2) set threshold as some multiple of noise
    THRESHOLD = noise_level * 3  # tune multiplier if needed
    print("Using threshold:", THRESHOLD)

    print("Now exhale towards the mic...")
    start_time = time.time()
    while time.time() - start_time < duration:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        rms = np.sqrt(np.mean(audio_data ** 2))

        if rms > THRESHOLD:
            print("Exhale detected! RMS:", rms)

    stream.stop_stream()
    stream.close()
    p.terminate()

    
if __name__ == "__main__":
    detect_exhale(duration=10)  # detect exhales for 10 seconds