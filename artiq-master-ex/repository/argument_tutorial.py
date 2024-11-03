from artiq.experiment import *

class ArgumentTutorial (EnvExperiment):
    """Argument Tutorial"""
    def build(self):
        pass

    def run(self):
        repeat = True
        while repeat:
            print("Hello World")
            with self.interactive(title="Repeat?") as interactive:
                interactive.setattr_argument("repeat", BooleanValue(True))
            repeat = interactive.repeat