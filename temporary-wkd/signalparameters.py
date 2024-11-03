from dataclasses import dataclass

@dataclass
class SignalParameters:
    frequency: float #frequency in Hz
    amplitude: float #Amplitude scale factor 0-1
    attenuation: float #Attenuation variable
    duration: int #Duration of signal 