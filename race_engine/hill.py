from PySide6.QtCore import QObject, Signal

from config import (
    HILL_DISTANCE,
    HILL_HEIGHT,
    GRAVITY,
)


class Hill(QObject):

    # ==========================================
    # SIGNAL
    # ==========================================

    race_started = Signal()

    race_finished = Signal(
        float,      # elapsed (s)
        float,      # speed (km/h)
        float,      # climb power (kW)
    )

    # ==========================================
    # INIT
    # ==========================================

    def __init__(self):

        super().__init__()

        self.mass = 0.0

        self.elapsed_time = None
        self.speed = None
        self.power = None

        self.reset()

    # ==========================================
    # PUBLIC
    # ==========================================

    def set_mass(self, mass):

        self.mass = mass

    def reset(self):

        self.start_time = None
        self.running = False

    def process_event(self, event):

        sensor = event.sensor
        timestamp = event.timestamp
        state = event.state

        if sensor == "S1" and state == "ON":

            self.start(timestamp)

        elif sensor == "S2" and state == "ON":

            self.finish(timestamp)

    # ==========================================
    # PRIVATE
    # ==========================================

    def start(self, timestamp):

        if self.running:

            return

        if self.mass <= 0:

            return

        self.running = True

        self.start_time = timestamp

        self.race_started.emit()

    def finish(self, timestamp):

        if not self.running:

            return

        elapsed = (timestamp - self.start_time) / 1_000_000.0

        if elapsed <= 0:

            self.reset()

            return

        # --------------------------------------
        # SPEED (km/h)
        # --------------------------------------

        speed = (HILL_DISTANCE / elapsed) * 3.6

        # --------------------------------------
        # CLIMB POWER (kW)
        # --------------------------------------

        power = (
            self.mass *
            GRAVITY *
            HILL_HEIGHT
        ) / elapsed

        power /= 1000.0

        self.elapsed_time = elapsed
        self.speed = speed
        self.power = power

        self.race_finished.emit(
            elapsed,
            speed,
            power,
        )

        self.reset()
