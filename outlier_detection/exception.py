# In the name of Allah


class IllegalIndexException(Exception):
    def __init__(self):
        Exception.__init__(self)


class MalformedTimeFrameException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
