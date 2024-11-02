from artiq.experiment import* 
import urukul_control 

class sample_expirement(EnvExperiment):
    
    def build(self):
        build = "build"
    
    @kernel
    def run(self):
        run = "run"



