from PySide6.QtCore import QObject, Signal


class Lap(QObject):

    # Tetap mempertahankan signature signal agar main.py
    # kompatibel dengan struktur aplikasi yang sudah ada.
    #
    # lap1, lap2, lap3, lap4, lap5, total_time, passed
    #
    # Untuk sistem sekarang hanya lap1 dan lap2 yang digunakan.
    lap_finished = Signal(
        float, float, float, float, float, float, bool
    )

    lap_completed = Signal(int, float)

    def __init__(self):

        super().__init__()

        self.reset()

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.start_time = None
        self.last_time = None

        self.laps = []

        self.lap1 = 0.0
        self.lap2 = 0.0
        self.lap3 = 0.0
        self.lap4 = 0.0
        self.lap5 = 0.0

        self.total_time = 0.0
        self.passed = False

    # =====================================================
    # PROCESS EVENT
    # =====================================================

    def process_event(self, event):

        # Hanya gunakan S1_ON
        if event.sensor != "S1":
            return

        if event.state != "ON":
            return

        # Trigger pertama = mulai
        if self.start_time is None:

            self.start_time = event.timestamp
            self.last_time = event.timestamp

            return

        # Hitung lap
        lap_time = (
            event.timestamp - self.last_time
        ) / 1_000_000.0

        if lap_time <= 0:
            return

        self.laps.append(lap_time)

        self.last_time = event.timestamp

        self.lap_completed.emit(
            len(self.laps),
            lap_time
        )

        # =================================================
        # SELESAI SETELAH 2 PUTARAN
        # =================================================

        if len(self.laps) == 2:

            total_time = sum(self.laps)

            passed = total_time >= 60.0

            self.lap1 = self.laps[0]
            self.lap2 = self.laps[1]

            # Tidak digunakan lagi
            self.lap3 = 0.0
            self.lap4 = 0.0
            self.lap5 = 0.0

            self.total_time = total_time
            self.passed = passed

            self.lap_finished.emit(
                self.lap1,
                self.lap2,
                0.0,
                0.0,
                0.0,
                total_time,
                passed
            )
