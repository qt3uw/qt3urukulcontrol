from artiq.experiment import* 
import urukul_control 

class sample_expirement(EnvExperiment):
    def build(self):
        self.paramaters = urukul_control.UKC()
        self.setattr_device("core")
        
        for channel in self.paramaters.channels:
            self.setattr_device(channel)


    @kernel
    def run(self):
        self.core.reset()                                       #resets core device
        self.urukul0_ch1.cpld.init()                            #initialises CPLD on channel 1
        self.urukul0_ch1.init()                                 #initialises channel 1
        delay(10 * ms)                                          #10ms delay

        freq = self.paramaters.frequency
        amp = self.paramaters.amplitude
        attenuation = self.paramaters.attenuation

        self.urukul0_ch1.set_att(attenuation)
        for frequency in freq:
            self.urukul0_ch1.set(frequency, amplitude = amp)
            delay(0.5*s)
        
        self.urukul0_ch1.sw.off()




