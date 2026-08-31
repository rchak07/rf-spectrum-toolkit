from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive 

def noise_filter(spectrum):

    percentile = np.percentile(spectrum, 90) # Get the 90th percentile value
    spectrum_mask = []
    for i in range(len(spectrum)):
        if spectrum[i] > percentile:
            spectrum_mask.append(1)
        else:
            spectrum_mask.append(0)

    return spectrum_mask

sdr = RtlSdr()
sdr.sample_rate = 2.4e6
sdr.center_freq = 95.8e6   # Capital FM, confirmed working
sdr.gain = 'auto'

sample_array = []
for i in range(10):
    print("Reading samples...")
    samples = sdr.read_samples(256*1024)
    sample_array.append(samples)


spectrum_array = []

for x in sample_array:
    spectrum = np.abs(np.fft.fftshift(np.fft.fft(x)))
    freqs = np.fft.fftshift(np.fft.fftfreq(len(x), 1/sdr.sample_rate)) + sdr.center_freq
    spectrum_array.append(spectrum)

final_spectrum = 20*np.log10(np.abs((np.mean(spectrum_array, axis=0))))
spectrum_mask = noise_filter(final_spectrum)
filter_spectrum = []
filter_freqs = []

for i in range(len(spectrum_mask)):
    if spectrum_mask[i] == 1:
        filter_spectrum.append(final_spectrum[i])
        filter_freqs.append(freqs[i])

plt.ion()  # Turn on interactive mode
plt.figure(figsize=(10,5))
line, = plt.plot(np.array(filter_freqs)/1e6, np.array(filter_spectrum), '.')
plt.xlabel('Frequency (MHz)')
plt.ylabel('Power (dB)')
plt.title('Capital FM capture')
plt.grid(True)
plt.show()



try:

    while(True):
        sample_array = []
        for i in range(10):
            print("Reading samples...")
            samples = sdr.read_samples(256*1024)
            sample_array.append(samples)


        spectrum_array = []

        for x in sample_array:
            spectrum = np.abs(np.fft.fftshift(np.fft.fft(x)))
            freqs = np.fft.fftshift(np.fft.fftfreq(len(x), 1/sdr.sample_rate)) + sdr.center_freq
            spectrum_array.append(spectrum)

        final_spectrum = 20*np.log10(np.abs((np.mean(spectrum_array, axis=0))))
        spectrum_mask = noise_filter(final_spectrum)
        filter_spectrum = []
        filter_freqs = []

        for i in range(len(spectrum_mask)):
            if spectrum_mask[i] == 1:
                filter_spectrum.append(final_spectrum[i])
                filter_freqs.append(freqs[i])

        line.set_ydata(np.array(filter_spectrum))
        line.set_xdata(np.array(filter_freqs)/1e6)
        plt.gca().relim()   # Recalculate limits
        plt.gca().autoscale_view()  # Autoscale
        plt.pause(0.1)  # Pause to allow the plot to update

except KeyboardInterrupt:
    print("Exiting...")
    sdr.close()
    plt.ioff()  # Turn off interactive mode



