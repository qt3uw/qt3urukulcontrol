from signalmanager import SignalManager
from artiq.experiment import *

class SignalConfigurator:
    def __init__(self):
        # Creates instance of manager 
        self.manager = SignalManager()
    
    # requests user input for frequency
    def get_frequency(self): 
        while True:
            try:
                freq_input = float(input("Enter the Frequency in MHz: "))
                if 1<= freq_input <= 500:
                    frequency = freq_input * MHz
                    return frequency
                else:
                    print("Frequency must be between 1 MHz and 500 MHz. Please try again.")
                
            except ValueError:
                print("Invalid input. Please enter valid numbers.")
   
    # requests user input for amplitude
    def get_amplitude(self):
        while True:
            try:
                amp_input = float(input("Enter the amplitude (0 - 1.0): "))
                if 0.0 <= amp_input <= 1.0:
                    return amp_input
                else:
                    print("Amplitude must be between 0.0 and 1.0. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    # requests user input for signal duration
    def get_signal_duration(self):
        while True:
            try:
                duration_input = float(input("Enter the output duration in ms: "))
                if duration_input > 0:
                    return duration_input * ms
                else:
                    print("Duration must be a positive number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def get_attenuation(self):
        while True:
            try:
                attenuation_input = float(input("Enter the attenuation value: "))
                if 0 <= attenuation_input <= 100:
                    return attenuation_input
                else: 
                    print("Attenuation must be a number from 0 to 100. Please try again")
                
            except ValueError:
                    print("Invalid input. Please enter a valid number.")
                
    # Collects user input and adds signal to manager 
    def get_user_input(self):
        while True:
            frequency = self.get_frequency()
            amplitude = self.get_amplitude()
            attenuation = self.get_attenuation()
            duration = self.get_signal_duration()
            
            # Add the validated signal to the manager
            self.manager.add_signal(frequency, amplitude, attenuation, duration)

            # Prompt to add more signals or stop
            more_signals = input("Add another signal? (yes/no): ").strip().lower()
            if more_signals != 'yes':
                break  # Exit the loop to stop adding more signals

    def get_manager(self):
        return self.manager
            
