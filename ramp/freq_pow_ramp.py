from artiq.experiment import *

class RampControl:
    def __init__(self):
        # freq ramp parameters
        self.start_freq = 1 * MHz
        self.end_freq = 50 * MHz
        self.ramp_duration = 10000 * ms
        self.num_steps = 1000
        self.step_duration = self.ramp_duration / self.num_steps
        self.freq_step = (self.end_freq - self.start_freq) / self.num_steps

        # amplitude parameters
        self.start_amplitude = 0.1           
        self.end_amplitude = 0.8             
        self.amp_step = (self.end_amplitude - self.start_amplitude) / self.num_steps


    @kernel
    def run_frequency_ramp(self, channel):
        current_freq = self.start_freq

        for step in range(self.num_steps):
            channel.set(current_freq)
            channel.cpld.io_update.pulse_mu(8)
            delay(self.step_duration)
            current_freq += self.freq_step

    @kernel
    def run_amplitude_ramp(self, channel):
        current_amplitude = self.start_amplitude
        
        for step in range(self.num_steps):
            channel.set(amplitude =current_amplitude)
            channel.cpld.io_update.pulse_mu(8)
            delay(self.step_duration)
            current_amplitude += self.amp_step