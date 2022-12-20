from abc import ABC, abstractmethod

class DataStorage(ABC):
    """
    Abstract Class with read and write property of files
    Detailed implementation is in file_util
    """
    def __init__(self, description):
        self._description = description
        
    @property
    def description(self):
        """
        property decorator for descripiton
        """
        return self._description
    
    @description.setter
    def description(self,description):
        """
        setter decorator for description
        """
        self._description = description

    @abstractmethod
    def read(self, *args, **kwargs):
        pass

    @abstractmethod
    def write(self, *args, **kwargs):
        pass 
