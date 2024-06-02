from abc import ABC, abstractmethod


class SensorHead(ABC):
    def __init__(self, *args, **kwargs):
        self.system_name = 'SystemName'

    @abstractmethod
    async def get_data(self, *args, **kwargs) -> dict[str: str]:
        """
        method to get data from sensors

        :param args: arguments for getting information from sensors (like ports, baudrate, etc.)
        :param kwargs: arguments for getting information from sensors (like ports, baudrate, etc.)
        :return: information from sensors (format {"parameter": "value with unit"})
        """
        pass
