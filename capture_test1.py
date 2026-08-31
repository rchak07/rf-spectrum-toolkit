from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt

sdr = RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = 95.8e6   # Capital FM, confirmed working
sdr.gain = 'auto'

print("Reading samples...")
samples = sdr.read_samples(256*1024)
sdr.close()

spectrum = np.fft.fftshift(np.fft.fft(samples))
freqs = np.fft.fftshift(np.fft.fftfreq(len(samples), 1/sdr.sample_rate)) + sdr.center_freq

plt.figure(figsize=(10,5))
plt.plot(freqs/1e6, 20*np.log10(np.abs(spectrum)))
plt.xlabel('Frequency (MHz)')
plt.ylabel('Power (dB)')
plt.title('Capital FM capture')
plt.grid(True)
plt.show()