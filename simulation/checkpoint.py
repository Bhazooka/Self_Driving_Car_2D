class Checkpoint:
    def __init__(self, position):
        self.position = position
        self.last_crossed = 0 

    def is_active(self, current_time):
        return current_time - self.last_crossed >= 2
