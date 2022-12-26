from abc import ABC, abstractmethod


class DataStorage(ABC):
    """
    Abstract Class with read and write property of files
    More implementation will be in child class like file_util
    DataStorage can be used to read and write any files
    DataStorage has attribute description describing any inherited class
    """
    def __init__(self, description):
        self._description = description
        
    @property
    def description(self):
        """
        Property decorator for descripiton
        Property decorator makes it easier for others to change the attribute
        So each inherited class has a new description
        """
        return self._description
    
    @description.setter
    def description(self,description):
        """
        Setter decorator for description
        It is used to set the value of attribute of description
        """
        self._description = description

    @abstractmethod
    def read(self, *args, **kwargs):
        """
        Abstract method that reads data, which will be overriden in inherited class
        """
        pass

    @abstractmethod
    def write(self, *args, **kwargs):
        """
        Abstract method that writes data, which will be overriden in inherited class
        """
        pass 
