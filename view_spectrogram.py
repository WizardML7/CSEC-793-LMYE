import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import sys
from scipy.signal import spectrogram


def generate_spectrogram(filename="cpu_leakage.wav"):
    """Loads a WAV file and displays an enhanced spectrogram with log scaling and time in milliseconds."""
    try:
        samplerate, data = wav.read(filename)

        # Convert stereo to mono if needed
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)

        # Compute the spectrogram with high resolution
        plt.figure(figsize=(10, 6))
        Pxx, freqs, bins, im = plt.specgram(data, Fs=samplerate, cmap='Greens', NFFT=2048, noverlap=1024)

        # Convert to dB scale for better visibility of variations
        Pxx = 10 * np.log10(Pxx + 1e-10)  # Avoid log(0) issues

        # Convert time bins from seconds to milliseconds
        bins *= 1000  

        # Set dynamic range to enhance contrast (adjust vmin/vmax as needed)
        plt.imshow(Pxx, aspect='auto', origin='lower', cmap='Greens',
           extent=[bins.min(), bins.max(), freqs.min(), freqs.max()],
           vmin=Pxx.max() - 60, vmax=Pxx.max())  # Expanding range to show more details


        plt.xlabel('Time [ms]')
        plt.ylabel('Frequency [Hz]')
        plt.title(f'Enhanced Spectrogram of {filename}')
        plt.colorbar(label='Power (dB)')
        plt.show()
    except Exception as e:
        print(f"Error loading {filename}: {e}")

def plot_audio_spectrum(wav_file_path):
    sample_rate, samples = wav.read(wav_file_path)
    
    if samples.ndim == 2:
        samples = samples[:, 0]

    f, t, Sxx = spectrogram(samples, fs=sample_rate, nperseg=512)
    plt.figure(figsize=(15, 4))
    plt.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='viridis')  
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.title('Spectrogram of Recorded Audio')
    plt.colorbar(label='Intensity [dB]')
    plt.show()

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "cpu_leakage.wav"
    generate_spectrogram(filename)

    plot_audio_spectrum(filename)
