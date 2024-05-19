from sensors.abe.ABE_ADCPi import ADCPi
from sensors.abe.ABE_helpers import ABEHelpers
from sensors.sensor_head import SensorHead


class AmperageSensor(SensorHead):

    def __init__(self):
        super().__init__()
        self.system_name = 'amperage'
        self.i2c_helper = ABEHelpers()
        self.bus = self.i2c_helper.get_smbus()
        self.adc = ADCPi(self.bus, 0x68, 0x69, 12)

    @staticmethod
    def calc_current(value):
        return (value - 2.5) / 0.066

    def get_data(self, channel: int = 1) -> float:
        return self.calc_current(self.adc.read_voltage(channel))
