from signalparameters import SignalParameters
from artiq.experiment import *

class SignalManager:
    def __init__(self):
        self.signals = []

    # Creates a signal parameters object and populates its fields 
    def add_signal(self, frequency, amplitude, attenuation, duration):
        new_signal = SignalParameters(frequency, amplitude, attenuation, duration)
        self.signals.append(new_signal)

    # Retrieves list of signal param objects
    def get_signals(self):
        return self.signals

    # displays signal param objects and their fields 
    def display_signals(self):
        for i, signal in enumerate(self.signals):
            print(f"Signal {i+1}: Frequency {signal.frequency/MHz} MHz, "
                  f"Amplitude {signal.amplitude}, Attenuation {signal.attenuation} dB, "
                  f"Duration {signal.duration/s} seconds")
