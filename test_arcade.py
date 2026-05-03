import arcade
import math

class TestWindow(arcade.Window):
    def __init__(self):
        super().__init__(400, 400, "Test")
        # create a rectangle texture pointing right
        self.sprite1 = arcade.Sprite(texture=arcade.make_soft_square_texture(40, arcade.color.RED))
        self.sprite1.center_x = 200
        self.sprite1.center_y = 200
        self.sprite1.angle = 45 # Try positive 45
        
    def on_draw(self):
        self.clear()
        self.sprite1.draw()

TestWindow()
print("Arcade version:", arcade.__version__)
