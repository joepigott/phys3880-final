import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import scipy
import numpy as np

matplotlib.rcParams.update({'font.size': 12})

# load data
data = pd.read_csv("../data/l0_temperature_032424-040924.csv")

# subset from 3-25 to 3-29
data = data[(data["created_at"] >= "2024-03-25 00:00:00 UTC") & (data["created_at"] <= "2024-03-29 00:00:00 UTC")]

temperature = data["value"].values

# subtract the mean. if we don't do this, the spectrum will have a dominant
# peak at 0 Hz
temperature = temperature - np.mean(temperature)

# calculate fft and frequency array
sample_rate = 1
N = len(temperature)
temperature_fft = np.fft.fft(temperature)
freq = np.fft.fftfreq(N, d=1./sample_rate)

plt.plot(freq, np.abs(temperature_fft))
plt.title("Temperature Spectrum Magnitude, 3/25/24 - 3/29/24")
plt.ylabel("Magnitude")
plt.xlabel("Frequency (Hz)")
plt.xlim(0, 1/300)
plt.show()

# repeat the previous steps, but pad the data to artificially increase the
# frequency resolution for visualization purposes
N_padded = len(temperature) * 5
temperature_padded = np.pad(temperature, (0, N_padded - N), "constant")

temperature_fft_padded = np.fft.fft(temperature_padded)
freq_padded = np.fft.fftfreq(len(temperature_padded), d=1./sample_rate)

plt.plot(freq_padded, np.abs(temperature_fft_padded))
plt.title("Temperature Spectrum Magnitude, 3/25/24 - 3/29/24 (Padded)")
plt.ylabel("Magnitude")
plt.xlabel("Frequency (Hz)")
plt.xlim(0, 1/300)
plt.show()

# spectrogram
f, t, Sxx = scipy.signal.spectrogram(temperature, fs=1)
plt.pcolormesh(t, f, Sxx, shading="gouraud")
plt.title("Temperature Spectrogram, 3/25/24 - 3/29/24")
plt.ylabel("Frequency (Hz)")
plt.xlabel("Time (s)")
plt.ylim(0, 0.01)
plt.show()
