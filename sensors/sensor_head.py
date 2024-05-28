from pydantic import BaseModel


class SensorHead:
    def __init__(self, *args, **kwargs):
        self.system_name = 'SystemName'

    async def get_data(self, *args, **kwargs) -> dict[str: str]:
        pass
