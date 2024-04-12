import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import scipy
import numpy as np

matplotlib.rcParams.update({'font.size': 12})

# load data
data = pd.read_csv("../../data/l0/l0_pressure_03-24-24_04-09-24.csv")

# subset from 3-25 to 3-29
# data = data[(data["created_at"] >= "2024-03-25 00:00:00 UTC") & (data["created_at"] <= "2024-03-29 00:00:00 UTC")]

pressure = data["value"].values

# subtract the mean. if we don't do this, the spectrum will have a dominant
# peak at 0 Hz
# pressure = pressure - np.mean(pressure)

# calculate fft and frequency array
sample_rate = 1
N = len(pressure)
pressure_fft = scipy.fft.rfft(pressure)
freq = scipy.fft.rfftfreq(N, d=1./sample_rate)

plt.plot(freq, np.abs(pressure_fft))
plt.title("Barometric Pressure Spectrum Magnitude, 3/25/24 - 3/29/24")
plt.ylabel("Magnitude")
plt.xlabel("Frequency (Hz)")
plt.show()

# repeat the previous steps, but pad the data to artificially increase the
# frequency resolution for visualization purposes
N_padded = len(pressure) * 5
pressure_padded = np.pad(pressure, (0, N_padded - N), "constant")

pressure_fft_padded = scipy.fft.rfft(pressure_padded)
freq_padded = scipy.fft.rfftfreq(len(pressure_padded), d=1./sample_rate)

plt.plot(freq_padded[:100], np.abs(pressure_fft_padded)[:100])
plt.title("Barometric Pressure Spectrum Magnitude, 3/25/24 - 3/29/24 (Padded)")
plt.ylabel("Magnitude")
plt.xlabel("Frequency (Hz)")
plt.show()

# spectrogram
f, t, Sxx = scipy.signal.spectrogram(pressure, fs=1)
plt.pcolormesh(t, f, Sxx, shading="gouraud")
plt.title("Barometric Pressure Spectrogram, 3/25/24 - 3/29/24")
plt.ylabel("Frequency (Hz)")
plt.xlabel("Time (s)")
plt.show()
