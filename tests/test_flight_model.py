import math
import pytest
import sys
import os

# Add parent dir to path so we can import src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.flight_model import FlightModel

def test_initial_state():
    model = FlightModel(x=100.0, y=200.0, angle=90.0)
    assert model.x == 100.0
    assert model.y == 200.0
    assert model.angle == 90.0
    assert model.speed == 0.0

def test_thrust():
    model = FlightModel()
    model.apply_thrust(10)
    assert model.speed == 10.0
    model.apply_thrust(-5)
    assert model.speed == 5.0

def test_steering():
    model = FlightModel(angle=90.0)
    model.turn(-15)
    assert model.angle == 75.0
    model.turn(30)
    assert model.angle == 105.0

def test_update_position_east():
    model = FlightModel(x=0, y=0, angle=0) # 0 degrees = East (Right)
    model.speed = 10.0
    model.update() 
    assert model.x == 10.0
    assert model.y == 0.0

def test_update_position_north():
    model = FlightModel(x=0, y=0, angle=90) # 90 degrees = North (Up)
    model.speed = 10.0
    model.update()
    assert model.x == pytest.approx(0.0, abs=1e-5)
    assert model.y == pytest.approx(10.0, abs=1e-5)
