from abc import ABC, abstractmethod


class ViewFrame(ABC):

    @abstractmethod
    def set_frame(self):
        pass
