from dataclasses import dataclass


@dataclass
class SensorEvent:
    sensor: str
    state: str
    timestamp: int
