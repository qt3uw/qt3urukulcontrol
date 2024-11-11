from artiq.experiment import *
from freq_pow_ramp import RampControl

class SampleExperiment(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("urukul0_ch1")
        self.ramp = RampControl()

    @kernel
    def run(self):
        # Reset core device and initialize CPLD and DDS on channel 1
        self.core.reset()
        self.urukul0_ch1.cpld.init()        
        self.urukul0_ch1.init()             
        delay(10 * ms)                      

        # Set initial attenuation and turn on the switch
        attenuation = 6.0 * dB
        self.urukul0_ch1.set_att(attenuation)
        self.urukul0_ch1.sw.on()

        # Run frequency and amplitude ramping
        self.ramp.run_frequency_ramp(self.urukul0_ch1)
        # self.ramp.run_amplitude_ramp(self.urukul0_ch1)

        # Turn off the DDS channel after completing the ramp
        self.urukul0_ch1.sw.off()
