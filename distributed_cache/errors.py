class CacheException(Exception):
    code = 400

    def __init__(self, *args, **kwargs):
        super(CacheException, self).__init__(*args)
        self.kwargs = kwargs
