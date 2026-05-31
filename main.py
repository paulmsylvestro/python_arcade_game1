import arcade
import math
import os
from src.plane import PlaneSprite

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "3D Flight Simulator"

class FlightSimGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.CORNFLOWER_BLUE)

        # Scrolling camera
        self.camera = arcade.camera.Camera2D()

        self.player_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()

        # WASD Input tracking
        self.w_pressed = False
        self.s_pressed = False
        self.a_pressed = False
        self.d_pressed = False

        self.player_sprite = None

    def setup(self):
        # Optional: Load background if available
        bg_path = os.path.join(os.path.dirname(__file__), 'assets', 'background.png')
        if os.path.exists(bg_path):
            temp_sprite = arcade.Sprite(bg_path)
            bg_width = temp_sprite.width
            bg_height = temp_sprite.height
            
            # Create a grid of background tiles to cover a large flight area
            start_x = SCREEN_WIDTH / 2
            start_y = SCREEN_HEIGHT / 2
            for grid_x in range(-10, 11):
                for grid_y in range(-10, 11):
                    bg_sprite = arcade.Sprite(bg_path)
                    bg_sprite.center_x = start_x + grid_x * bg_width
                    bg_sprite.center_y = start_y + grid_y * bg_height
                    self.background_list.append(bg_sprite)

        self.player_sprite = PlaneSprite()
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        self.clear()
        
        # Apply the camera viewpoint BEFORE drawing game elements
        self.camera.use()
        
        # Arcade 3.x requires drawing from a SpriteList
        self.background_list.draw()

        self.player_list.draw()

        # Draw an arrow pointing in the direction of movement
        if self.player_sprite:
            start_x = self.player_sprite.center_x
            start_y = self.player_sprite.center_y
            rad = math.radians(self.player_sprite.model.angle)
            
            # Arrow properties
            length = 60
            end_x = start_x + math.cos(rad) * length
            end_y = start_y + math.sin(rad) * length
            
            # Draw main shaft
            arcade.draw_line(start_x, start_y, end_x, end_y, arcade.color.RED, 3)
            
            # Draw arrowhead
            arrow_len = 15
            arrow_angle = math.radians(150)
            
            left_rad = rad + arrow_angle
            right_rad = rad - arrow_angle
            
            left_x = end_x + math.cos(left_rad) * arrow_len
            left_y = end_y + math.sin(left_rad) * arrow_len
            
            right_x = end_x + math.cos(right_rad) * arrow_len
            right_y = end_y + math.sin(right_rad) * arrow_len
            
            arcade.draw_line(end_x, end_y, left_x, left_y, arcade.color.RED, 3)
            arcade.draw_line(end_x, end_y, right_x, right_y, arcade.color.RED, 3)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.w_pressed = True
        elif key == arcade.key.S:
            self.s_pressed = True
        elif key == arcade.key.A:
            self.a_pressed = True
        elif key == arcade.key.D:
            self.d_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.w_pressed = False
        elif key == arcade.key.S:
            self.s_pressed = False
        elif key == arcade.key.A:
            self.a_pressed = False
        elif key == arcade.key.D:
            self.d_pressed = False

    def on_update(self, delta_time):
        # Map WASD states to TDD-verified flight model methods
        if self.w_pressed:
            self.player_sprite.model.apply_thrust(0.2) # Throttle up
        if self.s_pressed:
            self.player_sprite.model.apply_thrust(-0.1) # Throttle down / brake
        if self.a_pressed:
            self.player_sprite.model.turn(3) # Turn Left
        if self.d_pressed:
            self.player_sprite.model.turn(-3) # Turn Right

        # Apply basic drag to prevent infinite speed
        self.player_sprite.model.speed *= 0.98
        
        # This will call our sprite's update(), pulling new x, y, angle
        self.player_list.update()

        self.center_camera_to_player()

    def center_camera_to_player(self):
        target_x = self.player_sprite.center_x
        target_y = self.player_sprite.center_y

        # Smooth lerp
        current_x, current_y = self.camera.position
        new_x = current_x + (target_x - current_x) * 0.1
        new_y = current_y + (target_y - current_y) * 0.1
        
        self.camera.position = (new_x, new_y)

def main():
    window = FlightSimGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
