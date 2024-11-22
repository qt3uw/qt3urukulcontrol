from artiq.experiment import *
from artiq.coredevice import ad9910
import array

class SmoothDDSAmpSweep(EnvExperiment):
    def build(self):
        # Initialize hardware to be recognized
        self.setattr_device("core")
        self.setattr_device("urukul0_cpld")  
        self.setattr_device("urukul0_ch1")   # Using channel 1
        self.dds = self.urukul0_ch1

    def prepare(self):
        # Parameters for an amplitude sweep
        self.N = 100                        # Number of steps
        self.ampl_min = 0.1                 # Minimum amplitude (fraction of max amplitude)
        self.ampl_max = 0.5                 # Maximum amplitude (fraction of max amplitude)
        self.T = int(1e5)                   # Step duration in machine units, 10 nanoseconds per unit
        self.constant_frequency = 25 * MHz # Constant frequency for amplitude sweep

        # Generate a list of amplitudes from ampl_min to ampl_max with N steps
        ampl_span = self.ampl_max - self.ampl_min
        ampl_step = ampl_span / self.N

        # list comprehension that populates a list of N evenly spaced Amplitudes
        self.amplitudes = [self.ampl_min + i * ampl_step for i in range(self.N)]


        # Prepare an empty list for the RAM data
        self.ampl_ram = [0] * self.N

        # Use amplitude_to_ram to directly prepare the tuning words for RAM
        self.dds.amplitude_to_ram(self.amplitudes, self.ampl_ram)

    @kernel
    def run(self):
        self.core.reset()
        
        # Initialize DDS and CPLD
        self.dds.cpld.init()
        self.dds.init()
        self.dds.cpld.io_update.pulse(100 * ns)
        self.core.break_realtime()  # May be redundant

        # Set the constant frequency
        self.dds.set(self.constant_frequency)

        # Set attenuation
        self.dds.set_att(10 * dB)

        # Prepare RAM profile
        self.dds.set_cfr1()  # Disable RAM for configuration
        self.dds.cpld.io_update.pulse_mu(8)  # I/O pulse to enact RAM change

        # Configure RAM for continuous amplitude sweep
        self.dds.set_profile_ram(start=0, end=self.N - 1, step=self.T, profile=0, mode=ad9910.RAM_MODE_CONT_RAMPUP)
        self.dds.cpld.set_profile(0)
        self.dds.cpld.io_update.pulse_mu(8)

        # Write amplitude data to RAM
        delay(50 * us)
        self.dds.write_ram(self.ampl_ram)
        delay(100 * us)

        # Enable RAM mode
        self.dds.set_cfr1(internal_profile=0, ram_destination=ad9910.RAM_DEST_ASF, ram_enable=1)
        self.dds.cpld.io_update.pulse_mu(8)

        # Turn on the DDS output to start the amplitude sweep
        self.dds.sw.on()
        delay(10 * s)  # Keep the sweep running 
        self.dds.sw.off()

        # Clean up to prevent unwanted lingering configurations
        self.dds.set_cfr1(ram_enable=0, internal_profile=0)  # Disable RAM mode
        self.dds.cpld.io_update.pulse_mu(8)  # Apply changes

        # Reset CPLD profile
        self.dds.cpld.set_profile(0)
        self.dds.cpld.io_update.pulse_mu(8)

        # Turn off the DDS output
        self.dds.sw.off()

        # Reset the DDS and CPLD to defaults
        self.dds.cpld.init()
        self.dds.init()
        self.dds.cpld.io_update.pulse_mu(8)
