from artiq.experiment import *
from artiq.coredevice.ad9910 import RAM_DEST_FTW, RAM_MODE_BIDIR_RAMP

class FrequencyRamp(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.dds = self.get_device("urukul0_ch1")

    @kernel
    def run(self):
        n = 10
        data = [0] * (1 << n)
        
        for i in range(len(data) // 2):
            data[i] = int(self.dds.frequency_to_ftw(i * (50 * MHz / (len(data) // 2))))
            data[i + len(data) // 2] = self.dds.frequency_to_ftw(50 * MHz)

        self.core.reset()

        self.dds.cpld.init()
        self.dds.init()
        delay(1 * ms)

        self.dds.set_profile_ram(
            start=0, end=len(data) - 1, step=5,
            profile=0, mode=RAM_MODE_BIDIR_RAMP
        )

        self.dds.cpld.set_profile(0)
        self.dds.cpld.io_update.pulse_mu(8)
        delay(1 * ms)

        self.dds.write_ram(data)
        delay(10 * ms)

        self.dds.set_cfr1(ram_enable =1, ram_destination=RAM_DEST_FTW)

        self.dds.set_amplitude(1.0)
        self.dds.set_att(10 * dB)
        self.dds.sw.on()

        self.core.break_realtime()

        while True:
            delay(1 * ms)
            self.dds.cpld.set_profile(0)
            delay(2 * us)
            self.dds.cpld.set_profile(1)
