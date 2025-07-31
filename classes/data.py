# im lazy and want dot syntax
class Data:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
