import time
class Timer:
    def __init__(self):
        self.start = time.time()
    def elapsed(self):
        return time.time()-self.start
if __name__ == '__main__':
    t = Timer()
    while(True):
        print(t.elapsed())
