class LookupDict(dict):
    """Dictionary lookup object"""

    def __init__(self, name=None):
        self.name = name
        super(LookupDict, self).__init__()

    def __repr__(self):
        return f"<lookup '{self.name}'>"

    def __getitem__(self, key):
        # allow fallthrough, defualt to None
        return self.__dict__.get(key, None)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)
