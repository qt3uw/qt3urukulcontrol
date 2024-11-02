# from artiq.experiment import*                                   

# Class that defines parameters and settings for basic Urukul control

class UKC:
    def __init__(self):
        self.frequency = self.__get_frequency()
        self.attenuation = self.__get_attenuation()
        self.amplitude = self.__get_amplitude()
        self.channels = self.__get_RF_channels()
        self.output_duration = self.__get_output_duration()

    def __get_frequency(self):
        frequency = 10
        unit = MHz
        
        return frequency*unit
    
    def __get_attenuation(self):
        attenuation = 1 
        
        return attenuation

    def __get_amplitude(self):
        amplitude = 1
        
        return amplitude 
    
    def __get_RF_channels(self):
        use_channel_0 = False
        use_channel_1 = True 
        use_channel_2 = False
        use_channel_3 = False

        channels = [use_channel_0,use_channel_1,use_channel_2,use_channel_3]
        active_channels = []

        for index, is_active in enumerate(channels):
                if is_active:
                    active_channels.append(f"urukul0_ch{index}")
        
        return active_channels 
    
    def __get_output_duration():
        output_duration = 5
        unit = s

        return output_duration*unit

if __name__ == "__main__":
    uc = UKC()
    print(uc.channels)
    
    
    