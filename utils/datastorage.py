from abc import ABC, abstractmethod

class DataStorage(ABC):
    def __init__(self, description):
        self._description = description
        
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self,description):
        self._description = description

    @abstractmethod
    def read(self, config):
        pass

    @abstractmethod
    def write(self, config):
        pass 
