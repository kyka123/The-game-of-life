import time

class time_counter:
    timer = 0
    current_time = 0
    def __init__(self, name):
      self.name = name
    def start(self):
        self.current_time = time.time()
    def pause(self):
        self.timer = self.timer + time.time() - self.current_time
        self.current_time = 0
    def end(self) -> float:
        res = round(self.timer + self.current_time, 4)
        print(f'{self.name}: {res}')
        return res
