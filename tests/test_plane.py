import sys
import os
import pytest
import arcade

# Add parent dir to path so we can import src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.plane import PlaneSprite

def test_plane_sprite_rotation_mapping():
    """
    Test that the plane sprite correctly maps the standard math angle (counter-clockwise)
    to the Arcade Sprite angle (clockwise in this version).
    
    If the flight model turns left (counter-clockwise, so model.angle increases), 
    the sprite's visual angle must map such that it also rotates visually counter-clockwise.
    Since Arcade's Sprite.angle is clockwise, this means the Sprite.angle value must decrease.
    """
    # Arcade requires a window to be open to create Sprites sometimes, but PlaneSprite
    # creates a soft_square_texture if the image is missing, which might need a context.
    # Let's use a hidden window just in case.
    window = arcade.Window(100, 100, visible=False)
    
    try:
        plane = PlaneSprite()
        
        # Test moving East
        plane.model.angle = 0
        plane.update()
        # 0 math degrees (East) maps to 90 Arcade degrees (Clockwise from North)
        assert plane.angle == 90.0, f"Expected 90 degrees for East, got {plane.angle}"
        
        # Test moving North (turned 90 degrees left / counter-clockwise)
        plane.model.angle = 90
        plane.update()
        # 90 math degrees (North) maps to 0 Arcade degrees (North)
        assert plane.angle == 0.0, f"Expected 0 degrees for North, got {plane.angle}"
        
        # Test turning slightly left
        plane.model.angle = 93
        plane.update()
        # A left turn (increasing math angle) should result in a smaller Arcade angle
        # since positive Arcade angle rotates clockwise.
        assert plane.angle == -3.0, f"Expected -3 degrees for a slight left turn from North, got {plane.angle}"
        
        # Test moving West
        plane.model.angle = 180
        plane.update()
        assert plane.angle == -90.0, f"Expected -90 degrees for West, got {plane.angle}"
        
    finally:
        window.close()
