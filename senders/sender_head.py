from abc import abstractmethod, ABC

from pydantic import BaseModel

from models import SenderData


class SenderHead(ABC):
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def send_data(self, data: BaseModel) -> SenderData:
        """
        send data to device

        :param data: data to send which form on server-side (like port, baudrate, etc. )
        :return: results from current sender
        """
        return SenderData()
