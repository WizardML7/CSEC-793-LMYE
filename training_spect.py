import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from scipy.signal import spectrogram, butter, filtfilt

# Define paths
WAV_DIR = r"C:\Users\loiac\Desktop\recordings\voip_web"
OUTPUT_DIR = r"C:\Users\loiac\Desktop\recordings\spectrograms"

def highpass_filter(data, cutoff=1000, fs=44100, order=5):
    """Applies a high-pass Butterworth filter to remove low-frequency noise."""
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return filtfilt(b, a, data)

def generate_spectrogram(filename, output_path):
    """Generates a spectrogram and saves it as an image."""
    samplerate, data = wav.read(filename)

    # Convert stereo to mono if needed
    if data.ndim > 1:
        data = np.mean(data, axis=1)

    # Apply high-pass filtering
    #filtered_data = highpass_filter(data, cutoff=1000, fs=samplerate)

    # Compute spectrogram
    f, t, Sxx = spectrogram(data, fs=samplerate, nperseg=2048, noverlap=1024)
    Sxx = 10 * np.log10(Sxx + 1e-10)  # Convert power to dB scale

    # Plot and save spectrogram
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(t * 1000, f, Sxx, shading='gouraud', cmap='magma')  # Convert time to ms
    plt.xlabel('Time [ms]')
    plt.ylabel('Frequency [Hz]')
    plt.title('Spectrogram')
    plt.colorbar(label='Power (dB)')
    plt.savefig(output_path)
    plt.close()

def process_wav_files():
    """Processes all WAV files and generates spectrograms in a single directory."""
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for file in os.listdir(WAV_DIR):
        if file.endswith(".wav"):
            input_path = os.path.join(WAV_DIR, file)
            output_path = os.path.join(OUTPUT_DIR, file.replace(".wav", ".png"))
            generate_spectrogram(input_path, output_path)

if __name__ == "__main__":
    process_wav_files()
