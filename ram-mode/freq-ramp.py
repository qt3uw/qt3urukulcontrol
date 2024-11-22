from artiq.experiment import *
from artiq.coredevice import ad9910

class SmoothDDSFreqRamp(EnvExperiment):
    def build(self):
        # initializes hardware to be recognized 
        self.setattr_device("core")
        self.setattr_device("urukul0_cpld")  
        self.setattr_device("urukul0_ch1")   # Using channel 1
        self.dds = self.urukul0_ch1

    def prepare(self):
        # Parameters for a requency ramp
        self.N = 100                        # number of steps
        self.f1 = 25 * MHz                  # Start frequency
        self.f2 = 27 * MHz                  # End frequency
        self.T = int(1e7)                   # Step duration in machine units, 10 nanosecond per unit 

        # Generate a list of frequencies from f1 to f2 with N steps
        f_span = self.f2 - self.f1
        f_step = f_span / self.N
        
        # List comprehension that populates a list of N evenly spaced (f_step) frequencies
        self.frequencies = [self.f1 + i * f_step for i in range(self.N)]
        
        # Prepare an empty list for the RAM data of length N populated by zeros 
        self.f_ram = [0] * self.N
        
        # Use frequency_to_ram to directly prepare the tuning words for RAM
        self.dds.frequency_to_ram(self.frequencies, self.f_ram)

    @kernel
    def run(self):
        self.core.reset()
        
        # Initialize DDS and CPLD
        self.dds.cpld.init()
        self.dds.init()
        self.dds.cpld.io_update.pulse(100 * ns)
        self.core.break_realtime() # may be redundant
        
        # Set amplitude and attenuation
        self.dds.set_amplitude(1.0)
        self.dds.set_att(10 * dB)

        # Prepare RAM profile
        self.dds.set_cfr1()  # Disable RAM for configuration
        self.dds.cpld.io_update.pulse_mu(8)  # I/O pulse to enact RAM change

        # Configure RAM for a continuous ramp up
        self.dds.set_profile_ram(start=0, end=self.N - 1, step=self.T, profile=0, mode=ad9910.RAM_MODE_CONT_RAMPUP)

        
        # self.dds.set_profile_ram(start=0, end=self.N - 1, step=self.T, profile=0, mode=ad9910.RAM_MODE_RAMPUP) #single ramp up 
        
        self.dds.cpld.set_profile(0)
        self.dds.cpld.io_update.pulse_mu(8)

        # Write data to RAM
        delay(50 * us)
        self.dds.write_ram(self.f_ram)
        delay(100 * us)

        # Enable RAM mode
        self.dds.set_cfr1(internal_profile=0, ram_destination=ad9910.RAM_DEST_FTW, ram_enable=1)
        self.dds.cpld.io_update.pulse_mu(8)

        
        # Turn on the DDS output to start the frequency ramp
        self.dds.sw.on()
        delay(10 * s)  # Keep the ramp running 
        self.dds.sw.off()
        

        # Clean up that may help prevent unwanted configurations lingering
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