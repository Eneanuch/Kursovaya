from pydantic import BaseModel

from web.models import SenderData


class SenderHead:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def send_data(self, data: BaseModel) -> SenderData:
        return SenderData()
