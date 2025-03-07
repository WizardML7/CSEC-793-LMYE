import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import os
from scipy.signal import spectrogram

T1_FOLDER = "recordings/without_cpu"
T2_FOLDER = "recordings/with_cpu"
NFFT = 2048
NOVERLAP = 1024

def load_wav_files(folder):
    """Loads all WAV files from a folder and returns a list of file paths."""
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".wav")]

def compute_spectrogram(filename):
    """Computes the spectrogram of a given WAV file and returns its power matrix."""
    samplerate, data = wav.read(filename)
    
    # Convert stereo to mono if needed
    if data.ndim > 1:
        data = np.mean(data, axis=1)

    # Compute spectrogram
    f, t, Sxx = spectrogram(data, fs=samplerate, nperseg=NFFT, noverlap=NOVERLAP)

    # Convert to dB scale
    Sxx_dB = 10 * np.log10(Sxx + 1e-10)  # Avoid log(0) issues
    return Sxx_dB, f, t  # Return spectrogram and its frequency/time axes

def average_spectrograms(spectrograms):
    """Computes the element-wise average of a list of spectrograms."""
    return np.mean(spectrograms, axis=0)

def plot_spectrogram(Sxx, f, t, title, cmap="viridis"):
    """Plots a spectrogram with proper labeling."""
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(t, f, Sxx, shading='gouraud', cmap=cmap)
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    plt.title(title)
    plt.colorbar(label="Power (dB)")
    plt.show()

def plot_differential_spectrogram(diffT, time_bins, freqs):
    """Plots the differential spectrogram with white at 0 dB."""
    
    # Normalize around zero (find symmetric range)
    max_abs_val = np.max(np.abs(diffT))
    
    plt.figure(figsize=(12, 6))
    plt.imshow(diffT, aspect='auto', origin='lower', cmap='RdBu_r', 
               extent=[time_bins.min(), time_bins.max(), freqs.min(), freqs.max()],
               vmin=-max_abs_val, vmax=max_abs_val)

    plt.xlabel("Time [ms]")
    plt.ylabel("Frequency [Hz]")
    plt.title("Differential Spectrogram (avgT2 - avgT1)")
    plt.colorbar(label="Power Difference (dB)")
    plt.show()

# Load WAV files
T1_files = load_wav_files(T1_FOLDER)
T2_files = load_wav_files(T2_FOLDER)

# Compute spectrograms
T1_spectrograms = [compute_spectrogram(file)[0] for file in T1_files]
T2_spectrograms = [compute_spectrogram(file)[0] for file in T2_files]

# Use the frequency and time values from the first computation (assuming consistent parameters)
_, freqs, times = compute_spectrogram(T1_files[0])

# Compute average spectrograms
avgT1 = average_spectrograms(T1_spectrograms)
avgT2 = average_spectrograms(T2_spectrograms)

# Compute differential spectrogram
diffT = avgT2 - avgT1


# Plot results
plot_spectrogram(avgT1, freqs, times, "Average Spectrogram T1 (No CPU Load)")
plot_spectrogram(avgT2, freqs, times, "Average Spectrogram T2 (With CPU Load)")
plot_spectrogram(diffT, freqs, times, "Differential Spectrogram (T2 - T1)", cmap="RdBu")
