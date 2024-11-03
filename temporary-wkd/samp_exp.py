from signalconfig import SignalConfigurator
from artiq.experiment import* 

class sample_expirement(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("urukul0_ch1")

        configurator = SignalConfigurator()
        configurator.get_user_input()  # Collect user input for signals
        self.signal_manager = configurator.get_manager()

    @kernel
    def run(self):
        # Reset and initialize the core device and Urukul channel
        self.core.reset()
        self.urukul0_ch1.cpld.init()
        self.urukul0_ch1.init()
        delay(10 * ms)

        self.urukul0_ch1.sw.on()
        for signal in self.signal_manager.signals:
            self.urukul0_ch1.set_att(signal.attenuation)
            self.urukul0_ch1.set(signal.frequency, amplitude=signal.amplitude)
            delay(signal.duration)

        # Turn off the Urukul channel at the end
        self.urukul0_ch1.sw.off()




