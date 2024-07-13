
class ParcelSmsString:
    def __init__(self, sender_name, string):
        self.sender_name = sender_name
        self.string = string
        return
    
    def value(self):
        return str(self.sender_name) + " " + str(self.string)
    
    # Controls what gets pickled
    def __getstate__(self):
        attributes = self.__dict__.copy()
        return attributes
    
    # Controls how things get unpickled
    def __setstate__(self, state):
        self.__dict__ = state

class ParcelDisconnect:
    def __init__(self):
        pass

    # Controls what gets pickled
    def __getstate__(self):
        attributes = self.__dict__.copy()
        return attributes
    
    # Controls how things get unpickled
    def __setstate__(self, state):
        self.__dict__ = state

class ParcelPing:
    def __init__(self):
        pass

    # Controls what gets pickled
    def __getstate__(self):
        attributes = self.__dict__.copy()
        return attributes
    
    # Controls how things get unpickled
    def __setstate__(self, state):
        self.__dict__ = state

class ParcelEmpty:
    def __init__(self):
        pass

    # Controls what gets pickled
    def __getstate__(self):
        attributes = self.__dict__.copy()
        return attributes
    
    # Controls how things get unpickled
    def __setstate__(self, state):
        self.__dict__ = state