from artiq.experiment import *
from artiq.coredevice.ad9910 import (
    RAM_DEST_ASF, RAM_MODE_BIDIR_RAMP)

class ad9910RAM(EnvExperiment):
    '''Urukul Ram Amplitude Ramp'''

    def build(self):
        self.setattr_device("core")
        self.setattr_device("urukul0_cpld")  # Using cpld0

        self.dds = self.get_device("urukul0_ch1")

    
    @kernel
    def run(self):
        self.core.reset() #resets core device - may not be necessary 
        n = 10
        data = [0]*(1 << n)
        for i in range(len(data)//2):
            data[i] = i << (32 - (n - 1))  
            data[i + len(data)//2] = 0xffff << 16

        self.core.reset()

        
        self.dds.cpld.init()
        self.dds.init()
        delay(1*ms)

        self.dds.set_cfr1()
        self.dds.set_profile_ram(
            start=0, end=0+ len(data) - 1, step=5,
            profile = 0, mode = RAM_MODE_BIDIR_RAMP
        )

        self.dds.cpld.set_profile(0)
        self.dds.cpld.io_update.pulse_mu(8)
        
        delay(1*ms)
        self.dds.write_ram(data)
        delay(10*ms)

        self.dds.set_cfr1(ram_enable = 1, ram_destination=RAM_DEST_ASF)

        self.dds.set_frequency(35*MHz)
        self.dds.cpld.io_update.pulse_mu(8)
        self.dds.set_att(10*dB)
        self.dds.sw.on()

        # self.core.break_realtime()

        while True:
            delay(10*s)

            
            # self.dds.cpld.set_profile(0)

        
            delay(20*s)

            
            # self.dds.cpld.set_profile(1)

