from PySide6.QtCore import QObject, Signal

from config import SLALOM_DISTANCE


class StartFinish(QObject):

    race_started = Signal()
    race_finished = Signal(float, float)   # time(s), speed(km/h)

    def __init__(self):
        super().__init__()

        self.elapsed_time = 0.0
        self.speed = 0.0
        self.reset()

    # =====================================================
    # RESET
    # =====================================================
    def reset(self):

        self.start_time = None

    # =====================================================
    # PROCESS EVENT
    # =====================================================

    def process_event(self, event):

        # ----------------------------
        # START
        # ----------------------------

        if event.sensor == "S1" and event.state == "ON":

            self.start_time = event.timestamp

            self.race_started.emit()

            return

        # ----------------------------
        # FINISH
        # ----------------------------

        if event.sensor == "S2" and event.state == "ON":

            if self.start_time is None:
                return

            elapsed_us = event.timestamp - self.start_time

            self.elapsed_time = elapsed_us / 1_000_000.0

            self.speed = (
                SLALOM_DISTANCE /
                self.elapsed_time
            ) * 3.6

            self.race_finished.emit(
                self.elapsed_time,
                self.speed
            )

            self.reset()

    def clear_result(self):

        self.elapsed_time = 0.0
        self.speed = 0.0
