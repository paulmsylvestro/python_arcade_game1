import math

class FlightModel:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, pitch: float = 0.0, yaw: float = 0.0, roll: float = 0.0):
        self.x = x
        self.y = y
        self.z = z
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        self.speed = 0.0

    def apply_thrust(self, amount: float):
        self.speed += amount

    def turn(self, amount: float):
        self.yaw += amount
        self.yaw %= 360

    def pitch_plane(self, amount: float):
        self.pitch += amount
        self.pitch %= 360
        
    def roll_plane(self, amount: float):
        self.roll += amount
        self.roll %= 360

    def update(self):
        # Math functions require radians
        p_rad = math.radians(self.pitch)
        y_rad = math.radians(self.yaw)
        
        # Calculate forward vector based on pitch and yaw
        # Ursina coordinate system: Z is forward, X is right, Y is up
        fx = math.sin(y_rad) * math.cos(p_rad)
        fy = math.sin(p_rad)
        fz = math.cos(y_rad) * math.cos(p_rad)
        
        self.x += fx * self.speed
        self.y += fy * self.speed
        self.z += fz * self.speed
