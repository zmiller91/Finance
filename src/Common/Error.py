__author__ = 'zmiller'

class CustomException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def throw(strMessage):
    raise CustomException(strMessage)