from datetime import datetime as dt

def myConverter(obj):
        if isinstance(obj,dt):
            return obj.__str__()
