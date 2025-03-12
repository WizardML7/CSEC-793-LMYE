import sounddevice as sd
import numpy as np
import wave

def record_audio(duration, filename, device):
    samplerate = 48000  # Common sample rate
    channels = 2  # Stereo recording

    # Enable loopback mode
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='float32', device=device, blocking=True)

    # Normalize and save as WAV
    recording = np.int16(recording * 32767)  # Convert float32 to int16 for WAV
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(samplerate)
        wf.writeframes(recording.tobytes())

record_audio(25, "voip_capture.wav", device=17)
