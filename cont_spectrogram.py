import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
DEVICE = 5  # Set to None to use the default input device
FS = 44100  # Sample rate
NFFT = 1024  # Number of points in FFT
OVERLAP = 512  # Overlap between frames
DURATION = 5  # Duration of the rolling spectrogram (seconds)
BUFFER_SIZE = int(DURATION * FS)  # Buffer size


print(sd.query_devices())

# Create buffer for rolling spectrogram
audio_buffer = np.zeros(BUFFER_SIZE)

# Set up Matplotlib figure
fig, ax = plt.subplots()
cax = ax.imshow(
    np.random.rand(NFFT // 2, BUFFER_SIZE // NFFT), 
    aspect='auto', origin='lower', cmap='inferno', 
    extent=[0, DURATION, 0, FS / 2]
)
fig.colorbar(cax, ax=ax, label="Amplitude (dB)")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Frequency (Hz)")

def audio_callback(indata, frames, time, status):
    """Callback function to receive audio input."""
    global audio_buffer
    if status:
        print(status)
    audio_buffer = np.roll(audio_buffer, -frames)
    audio_buffer[-frames:] = indata[:, 0]  # Store mono audio

def update_plot(frame):
    """Update spectrogram plot in real-time."""
    ax.clear()
    _, _, Sxx, _ = ax.specgram(audio_buffer, NFFT=NFFT, Fs=FS, noverlap=OVERLAP, cmap="inferno")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_ylim(0, FS / 2)
    return ax,

# Start audio stream
stream = sd.InputStream(device=DEVICE, channels=1, samplerate=FS, callback=audio_callback)

with stream:
    ani = animation.FuncAnimation(fig, update_plot, interval=50, blit=False)
    plt.show()
