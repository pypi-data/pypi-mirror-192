def sub_uint(x, y):
    result = x - y
    if result < 0:
        return -result

class Collision:
    def __init__(self, canvas, element1, element2):
        self.canvas = canvas
        self.e1 = self.canvas.bbox(element1)
        self.e2 = self.canvas.bbox(element2)
        self.a_y_len = sub_uint(self.e1[1], self.e1[3])
        self.b_x_len = sub_uint(self.e2[0], self.e2[2])
    
    def collision_loop(self, side_1, side_2):
        for x in range(self.e2[0], self.e2[0] + self.b_x_len):
            for i in range(self.e1[1], self.e1[1] + self.a_y_len):
                if self.e2[side_2] == i and self.e1[side_1] == x:
                    return True

    def collide(self):
        if self.collision_loop(2, 1): # right to top
            return True
        elif self.collision_loop(2, 3): # right to bottom
            return True
        if self.collision_loop(0, 1): # left to top
            return True
        elif self.collision_loop(0, 3): # left to bottom
            return True
        else:
            return False