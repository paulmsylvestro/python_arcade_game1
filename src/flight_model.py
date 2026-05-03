import math

class FlightModel:
    def __init__(self, x: float = 0.0, y: float = 0.0, angle: float = 0.0):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 0.0

    def apply_thrust(self, amount: float):
        self.speed += amount

    def turn(self, amount: float):
        self.angle += amount
        self.angle %= 360  # Normalize to 0-359

    def update(self):
        # Math functions require radians
        rad = math.radians(self.angle)
        # 0 deg = East, 90 deg = North
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed
