class Rectangle:
    def __init__(self, topLeft, bottomRight):
        self.topLeft = topLeft
        self.bottomRight = bottomRight
        self.cluster = -1

    def set_cluster(self, cluster):
        self.cluster = cluster

    def get_cluster(self):
        return self.cluster

    def get_topLeft(self):
        return self.topLeft

    def get_bottomRight(self):
        return self.bottomRight

    def get_middle(self):
        return int((self.topLeft[0] + self.bottomRight[0]) / 2), int((self.topLeft[1] + self.bottomRight[1]) / 2)

    def __str__(self):
        return f"{self.topLeft},{self.bottomRight},{self.cluster}"
