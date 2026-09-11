from PySide6.QtCore import QObject, Signal

from config import (
    START_DISTANCE,
    BRAKE_SENSOR_DISTANCE,
)

from models import SensorEvent


class BrakeSystem(QObject):

    # =====================================================
    # SIGNAL
    # =====================================================

    brake_finished = Signal(
        bool,       # Passed
        object,     # Acceleration (m/s²)
        object,     # Brake speed at S2 (internal only, not displayed)
        object      # Deceleration (m/s²)
    )

    # =====================================================
    # INIT
    # =====================================================

    def __init__(self):

        super().__init__()

        self.reset()

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.s1_on = None
        self.s1_off = None

        self.s2_on = None
        self.s2_off = None

        self.s3_on = None
        self.s3_off = None

        self.acceleration = None
        self.brake_speed = None
        self.deceleration = None

    # =====================================================
    # PROCESS EVENT
    # =====================================================

    def process_event(self, event: SensorEvent):

        if event.sensor == "S1":

            if event.state == "ON":
                self.s1_on = event.timestamp

            elif event.state == "OFF":
                self.s1_off = event.timestamp

        elif event.sensor == "S2":

            if event.state == "ON":
                self.s2_on = event.timestamp

            elif event.state == "OFF":
                self.s2_off = event.timestamp

        elif event.sensor == "S3":

            if event.state == "ON":
                self.s3_on = event.timestamp

            elif event.state == "OFF":
                self.s3_off = event.timestamp

    # =====================================================
    # CALCULATE
    # =====================================================

    def calculate(self):

        # -------------------------------------------------
        # Validasi S1 -> S2
        # -------------------------------------------------

        if self.s1_on is None or self.s2_on is None:
            return

        dt_accel = (
            self.s2_on - self.s1_on
        ) / 1_000_000.0

        if dt_accel <= 0:
            return

        # -------------------------------------------------
        # AKSELERASI S1 -> S2
        #
        # V0 = 0 m/s
        # S  = 30 m
        #
        # s = 1/2 a t²
        # a = 2s / t²
        # -------------------------------------------------

        acceleration = (
            2.0 * START_DISTANCE
        ) / (
            dt_accel ** 2
        )

        # Kecepatan tepat di S2.
        # Digunakan internal untuk menghitung deselerasi.
        brake_speed = acceleration * dt_accel

        self.acceleration = acceleration
        self.brake_speed = brake_speed

        # -------------------------------------------------
        # S3 harus tersedia untuk menghitung deselerasi
        # -------------------------------------------------

        if self.s3_on is None:

            self.brake_finished.emit(
                False,
                acceleration,
                brake_speed,
                None
            )

            return

        # -------------------------------------------------
        # Waktu pengereman S2 -> S3
        # -------------------------------------------------

        dt_brake = (
            self.s3_on - self.s2_on
        ) / 1_000_000.0

        if dt_brake <= 0:
            self.brake_finished.emit(
                False,
                self.acceleration,
                self.brake_speed,
                0.0
            )
            return

        # -------------------------------------------------
        # DESELERASI S2 -> S3
        #
        # s = v0*t + 1/2*a*t²
        #
        # a = 2(s - v0*t) / t²
        #
        # s  = 0.30 m
        # v0 = kecepatan saat S2
        # -------------------------------------------------

        deceleration = (
            2.0 * (
                BRAKE_SENSOR_DISTANCE
                - (
                    brake_speed * dt_brake
                )
            )
        ) / (
            dt_brake ** 2
        )

        self.deceleration = deceleration

        # -------------------------------------------------
        # S2 dan S3 harus OFF untuk hasil PASS
        # -------------------------------------------------

        if self.s2_off is None or self.s3_off is None:

            self.brake_finished.emit(
                False,
                acceleration,
                brake_speed,
                deceleration
            )

            return

        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        self.brake_finished.emit(
            True,
            acceleration,
            brake_speed,
            deceleration
        )
