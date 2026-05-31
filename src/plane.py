from ursina import Entity, color
from src.flight_model import FlightModel
import os

class PlaneEntity(Entity):
    def __init__(self, **kwargs):
        # Initialize as an empty parent entity with a box collider encompassing the plane
        super().__init__(collider='box', **kwargs)
        
        # Build the plane using primitive shapes
        # Fuselage (main body)
        self.fuselage = Entity(parent=self, model='cube', color=color.white, scale=(1, 1, 4))
        
        # Main Wings
        self.wings = Entity(parent=self, model='cube', color=color.red, scale=(5, 0.2, 1.2), position=(0, 0, 0.5))
        
        # Tail - Horizontal Stabilizer
        self.tail_h = Entity(parent=self, model='cube', color=color.red, scale=(2.5, 0.2, 0.8), position=(0, 0, -1.7))
        
        # Tail - Vertical Stabilizer
        self.tail_v = Entity(parent=self, model='cube', color=color.red, scale=(0.2, 1.2, 0.8), position=(0, 0.6, -1.7))

        # Cockpit Window
        self.cockpit = Entity(parent=self, model='cube', color=color.black, scale=(0.8, 0.4, 1), position=(0, 0.5, 1))
        
        # Initialize our testable physics model
        self.physics = FlightModel(x=0, y=10, z=0, pitch=0.0, yaw=0.0, roll=0.0)

    def update(self):
        # Ursina calls update() automatically every frame
        self.physics.update()
        
        # Sync the Ursina entity attributes with our math model
        self.x = self.physics.x
        self.y = self.physics.y
        self.z = self.physics.z
        
        # Ursina uses rotation_x for pitch, rotation_y for yaw, rotation_z for roll
        # Ursina's coordinate system requires inverting pitch and roll to match standard flight math
        self.rotation_x = -self.physics.pitch # Negative X rotation pitches the nose UP
        self.rotation_y = self.physics.yaw    # Positive Y rotation turns RIGHT
        self.rotation_z = -self.physics.roll  # Positive Z rotation banks LEFT
