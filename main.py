from ursina import Ursina, Entity, color, camera, window, held_keys, load_texture, Sky
from src.plane import PlaneEntity
import os

app = Ursina()

window.title = "3D Flight Simulator"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True
window.color = color.cyan # Light blue sky background if Skybox fails

Sky() # Adds a default skybox

# Attempt to load the existing background.png as a ground texture
bg_path = os.path.join(os.path.dirname(__file__), 'assets', 'background.png')
ground_texture = None
if os.path.exists(bg_path):
    ground_texture = load_texture(bg_path)

# Create a massive 3D ground plane
ground = Entity(
    model='plane',
    texture=ground_texture,
    scale=(2000, 1, 2000), # Very large ground
    color=color.white if ground_texture else color.lime,
    position=(0, 0, 0),
    collider='box'
)
if ground_texture:
    # Tile the texture so it doesn't look stretched
    ground.texture_scale = (200, 200)

# Instantiate the plane (starting in the air)
player = PlaneEntity(position=(0, 50, 0))
# Override the physics starting Y so it matches the entity position
player.physics.y = 50

# Setup a chase camera to follow the player
camera.parent = player
camera.position = (0, 5, -20)  # Behind and slightly above the plane
# Tilt the camera down slightly to look at the plane
camera.rotation_x = 10

def update():
    # Throttle (W/S)
    if held_keys['w']:
        player.physics.apply_thrust(0.1)
    if held_keys['s']:
        player.physics.apply_thrust(-0.05)
        
    # Yaw / Turning (A/D)
    if held_keys['a']:
        player.physics.turn(-1.5)
        player.physics.roll_plane(-2) # Bank left
    elif held_keys['d']:
        player.physics.turn(1.5)
        player.physics.roll_plane(2)  # Bank right
    else:
        # Auto-level the roll when not turning
        if player.physics.roll > 0 and player.physics.roll < 180:
            player.physics.roll -= min(2, player.physics.roll)
        elif player.physics.roll >= 180 and player.physics.roll < 360:
            player.physics.roll += min(2, 360 - player.physics.roll)
        player.physics.roll %= 360
            
    # Pitch (Up/Down Arrows) - Standard flight controls
    if held_keys['up arrow']: # Push stick forward -> Nose down
        player.physics.pitch_plane(-1)   
    if held_keys['down arrow']: # Pull stick back -> Nose up
        player.physics.pitch_plane(1)  
        
    # Apply basic drag
    player.physics.speed *= 0.98

    # Collision Detection
    hit_info = player.intersects()
    if hit_info.hit:
        print(f"CRASH! You hit an object.")
        # Reset plane on crash
        player.physics.x, player.physics.y, player.physics.z = (0, 50, 0)
        player.physics.speed = 0
        player.physics.pitch = 0
        player.physics.yaw = 0
        player.physics.roll = 0

import random

def generate_environment():
    # Generate Mountains
    for _ in range(80):
        m_x = random.uniform(-900, 900)
        m_z = random.uniform(-900, 900)
        # Avoid putting mountains exactly where the player spawns
        if abs(m_x) < 100 and abs(m_z) < 100:
            continue
            
        m_scale_y = random.uniform(100, 300)
        m_scale_xz = random.uniform(100, 250)
        
        # Mountain base (using a rotated cube for a low-poly jagged look)
        Entity(
            model='cube',
            color=color.dark_gray,
            scale=(m_scale_xz, m_scale_y, m_scale_xz),
            position=(m_x, m_scale_y/2, m_z),
            rotation_y=45,
            collider='box'
        )
        # Snow cap
        Entity(
            model='cube',
            color=color.white,
            scale=(m_scale_xz * 0.4, m_scale_y * 0.4, m_scale_xz * 0.4),
            position=(m_x, m_scale_y * 0.8, m_z),
            rotation_y=45,
            collider='box'
        )

    # Generate Forests (Trees)
    for _ in range(400):
        t_x = random.uniform(-900, 900)
        t_z = random.uniform(-900, 900)
        # Tree trunk (Ursina has no default cylinder, so we use a stretched cube)
        Entity(model='cube', color=color.brown, scale=(2, 8, 2), position=(t_x, 4, t_z), collider='box')
        # Tree leaves
        Entity(model='cube', color=color.color(120, 0.8, 0.4), scale=(8, 8, 8), position=(t_x, 10, t_z), collider='box')

    # Generate Rivers
    for _ in range(20):
        r_x = random.uniform(-900, 900)
        r_z = random.uniform(-900, 900)
        r_rot = random.uniform(0, 360)
        r_length = random.uniform(300, 1000)
        r_width = random.uniform(20, 60)
        
        Entity(
            model='plane',
            color=color.blue,
            scale=(r_width, 1, r_length),
            position=(r_x, 0.1, r_z), # Slightly above ground to prevent Z-fighting
            rotation_y=r_rot,
            collider='box'
        )

generate_environment()

if __name__ == "__main__":
    app.run()
