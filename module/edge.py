class Edge:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
    def __str__(self):
        return str(self.start_x) + ' ' + str(self.start_y) + ' ' + str(self.end_x) + ' ' + str(self.end_y)