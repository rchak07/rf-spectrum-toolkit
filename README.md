SDR Signal Analyser

A Python-based RF spectrum analyser built on an RTL-SDR dongle. Captures live IQ samples from the radio spectrum, processes them with FFTs, and visualises the result — with signal detection and ADS-B aircraft decoding planned as next steps.

Show Image Example capture: Capital FM (95.8 MHz) showing a clear station peak against the noise floor.

Overview

This project uses a NooElec NESDR SMArt v5 (RTL2832U-based SDR dongle) to receive and analyse RF signals directly through Python, without relying on GUI tools like SDR# or GQRX. It's built as a hands-on exploration of software-defined radio, digital signal processing, and embedded/RF engineering concepts.

Features
Live capture of IQ samples from an RTL-SDR device via pyrtlsdr
FFT-based spectrum analysis and visualisation with NumPy and Matplotlib
Configurable centre frequency and sample rate
Planned
Continuous/live spectrum display (waterfall)
Peak and signal detection above the noise floor
FM broadcast demodulation
ADS-B aircraft transponder decoding for real-time aircraft detection/tracking
Hardware
NooElec NESDR SMArt v5 (RTL2832U + R820T tuner)
Whip/telescoping antenna
Requirements
Python 3.x
pyrtlsdr
NumPy
Matplotlib
rtlsdr.dll / libusb-1.0.dll (Windows) or librtlsdr installed via package manager (Linux/Mac)

Install Python dependencies:

bash
pip install pyrtlsdr numpy matplotlib
Setup
Install the RTL-SDR drivers for your OS (on Windows, via Zadig — install the WinUSB driver for the device).
Verify the dongle works using SDR# or GQRX before running any Python code.
Clone this repo and install the Python dependencies above.
Run a capture:
bash
python capture.py
Project Structure
sdr-signal-analyser/
├── README.md
├── requirements.txt
├── capture.py       # SDR interface: open device, configure, read samples
├── dsp.py           # FFT, windowing, peak detection, filters
├── display.py       # plotting / waterfall / GUI or web front end
└── main.py          # ties it together, run loop
Status

Early stage. Core capture-to-spectrum pipeline is working and confirmed against a known FM broadcast signal. Next phase is moving from single-shot captures to a live display, followed by signal detection and ADS-B decoding.
