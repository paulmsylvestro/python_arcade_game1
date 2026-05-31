import math
import pytest
import sys
import os

# Add parent dir to path so we can import src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.flight_model import FlightModel

def test_initial_state():
    model = FlightModel(x=100.0, y=200.0, z=50.0, pitch=10.0, yaw=90.0, roll=0.0)
    assert model.x == 100.0
    assert model.y == 200.0
    assert model.z == 50.0
    assert model.pitch == 10.0
    assert model.yaw == 90.0
    assert model.roll == 0.0
    assert model.speed == 0.0

def test_thrust():
    model = FlightModel()
    model.apply_thrust(10)
    assert model.speed == 10.0
    model.apply_thrust(-5)
    assert model.speed == 5.0

def test_steering():
    model = FlightModel(yaw=90.0)
    model.turn(-15)
    assert model.yaw == 75.0
    model.turn(30)
    assert model.yaw == 105.0

def test_pitching():
    model = FlightModel(pitch=0.0)
    model.pitch_plane(10)
    assert model.pitch == 10.0
    model.pitch_plane(-20)
    assert model.pitch == 350.0

def test_update_position_forward():
    model = FlightModel(x=0, y=0, z=0, pitch=0, yaw=0) # yaw 0 = Forward along Z
    model.speed = 10.0
    model.update() 
    assert model.x == pytest.approx(0.0, abs=1e-5)
    assert model.y == pytest.approx(0.0, abs=1e-5)
    assert model.z == pytest.approx(10.0, abs=1e-5)

def test_update_position_right():
    model = FlightModel(x=0, y=0, z=0, pitch=0, yaw=90) # yaw 90 = Right along X
    model.speed = 10.0
    model.update()
    assert model.x == pytest.approx(10.0, abs=1e-5)
    assert model.y == pytest.approx(0.0, abs=1e-5)
    assert model.z == pytest.approx(0.0, abs=1e-5)

def test_update_position_up():
    model = FlightModel(x=0, y=0, z=0, pitch=90, yaw=0) # pitch 90 = Up along Y
    model.speed = 10.0
    model.update()
    assert model.x == pytest.approx(0.0, abs=1e-5)
    assert model.y == pytest.approx(10.0, abs=1e-5)
    assert model.z == pytest.approx(0.0, abs=1e-5)
