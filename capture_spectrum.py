"""
capture_spectrum.py

Captures IQ samples from an RTL-SDR and plots an averaged, windowed
power spectrum using Welch's method (instead of a single raw FFT).

This fixes two things vs. a naive single-FFT plot:
  1. Averaging multiple FFT frames -> much smoother noise floor,
     easier to spot weak signals.
  2. A proper window function (Hann by default) -> less spectral
     leakage, cleaner peaks.

Usage:
    python capture_spectrum.py
Adjust CENTER_FREQ / SAMPLE_RATE / N_SAMPLES / N_AVERAGES below as needed.
"""

from rtlsdr import RtlSdr
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# ---- Capture parameters ----
CENTER_FREQ = 95.8e6      # Hz, tune to your target (e.g. Capital FM)
SAMPLE_RATE = 2.4e6       # Hz, RTL-SDR v5 typical stable rate
GAIN = 'auto'             # or a specific dB value, e.g. 40.0

N_FFT = 4096               # FFT size per segment (frequency resolution)
N_SAMPLES = 2**20          # total IQ samples to capture per sweep
N_AVERAGES_TARGET = 50     # roughly how many FFT segments we want Welch to average

TITLE = "Capital FM capture (averaged)"


def capture_iq(center_freq, sample_rate, n_samples, gain='auto'):
    sdr = RtlSdr()
    try:
        sdr.sample_rate = sample_rate
        sdr.center_freq = center_freq
        sdr.gain = gain
        samples = sdr.read_samples(n_samples)
    finally:
        sdr.close()
    return samples


def compute_averaged_spectrum(samples, sample_rate, n_fft):
    """
    Welch's method: splits the signal into overlapping segments,
    windows each one (Hann), FFTs them, and averages the power
    spectra together. This is the standard way to get a smooth,
    low-variance spectrum estimate from a finite-length capture.
    """
    freqs, psd = signal.welch(
        samples,
        fs=sample_rate,
        window='hann',
        nperseg=n_fft,
        noverlap=n_fft // 2,   # 50% overlap -> more averages, less variance
        return_onesided=False,  # IQ data is complex -> need both halves of spectrum
        scaling='density',
    )
    # fftshift so frequencies run low->high instead of 0..fs/2, -fs/2..0
    freqs = np.fft.fftshift(freqs)
    psd = np.fft.fftshift(psd)

    # Convert to dB
    psd_db = 10 * np.log10(psd + 1e-20)  # epsilon avoids log(0)
    return freqs, psd_db


def plot_spectrum(freqs, psd_db, center_freq, title):
    freq_mhz = (freqs + center_freq) / 1e6

    plt.figure(figsize=(10, 6))
    plt.plot(freq_mhz, psd_db, linewidth=0.8)
    plt.title(title)
    plt.xlabel("Frequency (MHz)")
    plt.ylabel("Power Spectral Density (dB)")
    plt.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.savefig("spectrum_averaged.png", dpi=150)
    plt.show()


def main():
    n_segments = N_SAMPLES // (N_FFT // 2)  # rough estimate given 50% overlap
    print(f"Capturing {N_SAMPLES} samples at {SAMPLE_RATE/1e6:.2f} Msps "
          f"centered on {CENTER_FREQ/1e6:.3f} MHz...")
    print(f"(~{n_segments} overlapping segments will be averaged)")

    samples = capture_iq(CENTER_FREQ, SAMPLE_RATE, N_SAMPLES, GAIN)
    freqs, psd_db = compute_averaged_spectrum(samples, SAMPLE_RATE, N_FFT)
    plot_spectrum(freqs, psd_db, CENTER_FREQ, TITLE)

    print("Saved plot to spectrum_averaged.png")


if __name__ == "__main__":
    main()