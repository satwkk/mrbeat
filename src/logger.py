import time

class LogException(Exception):
    pass

class Logger:
    def __init__(self):
        pass
    
    def log(self, msg):
        try:
            print(f"[{time.ctime()}] : {msg}")
        except LogException:
            print("Problem in logging. Passed some unparsable data to the logger.")
