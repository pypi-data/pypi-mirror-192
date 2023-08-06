from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty


class LocDataBase(ABC):

    @abstractproperty
    def data(self):
        return self.dataframe

class _LocData(LocDataBase):

    def __init__(self):
        pass

    def