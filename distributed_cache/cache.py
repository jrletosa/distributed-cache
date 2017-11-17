

class Storage(object):
    '''Wrapper around the storage implementation.
    In this case, storage is handled by a simple built-in dictionary
    '''
    
    def __init__(self):
        self.map = {}
    
    def add(self, key, value):
        self.map[key] = value
    
    def get(self, key):
        return self.map.get(key)
        
    def remove(self, key):
        self.map.pop(key, None)