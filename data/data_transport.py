from dataclasses import dataclass


@dataclass
class SmartHome:
    __slots__ = ('date', 'temperature', 'water_level', 'fire_level', 'beam', 'co', 'move', 'humidity')
    date: str
    temperature: float
    water_level: float
    fire_level: float
    beam: float
    co: float
    move: int
    humidity: float
