import arcade
from src.flight_model import FlightModel
import os

class PlaneSprite(arcade.Sprite):
    def __init__(self):
        # We try to use the image you generate. If you haven't generated it yet,
        # we will use a fallback red box so the game can still be play-tested.
        asset_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'plane.png')
        if os.path.exists(asset_path):
            super().__init__(asset_path)
        else:
            # Fallback red box for TDD execution without blocking on art
            super().__init__(texture=arcade.make_soft_square_texture(40, arcade.color.RED, outer_alpha=255))
        
        # Initialize our testable physics model
        self.model = FlightModel(x=400, y=300, angle=90.0)

    def update(self, delta_time: float = 1/60):
        # Arcade calls update(delta_time) automatically when player_list.update() is firing
        self.model.update()
        
        # Sync the Arcade sprite attributes with our math model
        self.center_x = self.model.x
        self.center_y = self.model.y
        # Add a -90 degree offset. Math 0 degrees is East, 
        # but top-down airplane sprites usually face North natively.
        self.angle = self.model.angle - 90
