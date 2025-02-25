import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from scipy.signal import spectrogram, butter, filtfilt
import datetime

LOG_FILE = "cpu_timestamps.log"

def load_cpu_timestamps(log_file):
    """Reads the CPU start timestamps from file and converts them to relative time in milliseconds."""
    try:
        with open(log_file, "r") as f:
            timestamps = [line.strip() for line in f.readlines()]
        
        if not timestamps:
            print("No timestamps found in log file.")
            return []

        start_time = datetime.datetime.strptime(timestamps[0], "%H:%M:%S.%f")
        return [(datetime.datetime.strptime(t, "%H:%M:%S.%f") - start_time).total_seconds() * 1000 for t in timestamps]
    
    except FileNotFoundError:
        print("Log file not found.")
        return []

def highpass_filter(data, cutoff=1000, fs=44100, order=5):
    """Applies a high-pass Butterworth filter to remove low-frequency noise."""
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return filtfilt(b, a, data)

def generate_spectrogram_with_timestamps(filename="cpu_leakage.wav"):
    """Loads a WAV file, applies filtering, and overlays CPU start timestamps."""
    samplerate, data = wav.read(filename)

    # Convert stereo to mono if needed
    if data.ndim > 1:
        data = np.mean(data, axis=1)

    # Apply high-pass filtering
    filtered_data = highpass_filter(data, cutoff=1000, fs=samplerate)

    # Compute spectrogram
    f, t, Sxx = spectrogram(filtered_data, fs=samplerate, nperseg=2048, noverlap=1024)
    
    # Convert power to dB scale
    Sxx = 10 * np.log10(Sxx + 1e-10)  # Avoid log(0) issues
    
    # Convert time bins to milliseconds
    t *= 1000  

    # Plot spectrogram using pcolormesh
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(t, f, Sxx, shading='gouraud', cmap='magma')

    # Overlay CPU event timestamps
    event_times = load_cpu_timestamps(LOG_FILE)

    for event in event_times:
        plt.axvline(x=event, color='cyan', linestyle='--', linewidth=1.5, label="CPU Start" if event == event_times[0] else "")

    plt.xlabel('Time [ms]')
    plt.ylabel('Frequency [Hz]')
    plt.title('Spectrogram with CPU Load Events')
    plt.colorbar(label='Power (dB)')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    generate_spectrogram_with_timestamps("cpu_leakage.wav")
