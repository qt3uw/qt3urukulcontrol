from artiq.experiment import *

class DDSBasicTest(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("urukul0_cpld")
        self.dds = self.get_device("urukul0_ch1")

    @kernel
    def run(self):
        self.core.reset()
        self.dds.cpld.init()
        self.dds.init()
        self.dds.cpld.io_update.pulse_mu(8)

        self.dds.set_frequency(40 * MHz)
        self.dds.set_amplitude(0.5)
        self.dds.set_att(10 * dB)
        self.dds.cpld.io_update.pulse_mu(8)
        self.dds.sw.on()
        delay(5 * s)
        self.dds.sw.off()
