from PySide6.QtCore import QObject, Signal

import serial
import serial.tools.list_ports

from models import SensorEvent


class SerialManager(QObject):

    # =====================================================
    # SIGNAL
    # =====================================================

    connected = Signal()
    disconnected = Signal()

    error = Signal(str)

    raw_data = Signal(str)

    status_received = Signal(str)

    clock_received = Signal(int)

    sensor_event = Signal(SensorEvent)

    # =====================================================
    # INIT
    # =====================================================

    def __init__(self):

        super().__init__()

        self.serial = None
        self.current_clock = 0

    # =====================================================
    # AVAILABLE PORTS
    # =====================================================

    def available_ports(self):

        return [
            port.device
            for port in serial.tools.list_ports.comports()
        ]

    # =====================================================
    # CONNECT
    # =====================================================

    def connect(self, port, baudrate):

        try:

            self.serial = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=0.01
            )
            self.current_clock = 0
            self.connected.emit()

        except Exception as e:

            self.error.emit(str(e))

    # =====================================================
    # DISCONNECT
    # =====================================================

    def disconnect(self):

        if self.serial is None:
            return

        if self.serial.is_open:
            self.serial.close()

        self.serial = None
        self.current_clock = 0
        self.disconnected.emit()

    # =====================================================
    # WRITE
    # =====================================================

    def write(self, text):

        if self.serial is None:
            return

        if not self.serial.is_open:
            return

        self.serial.write(f"{text}\n".encode())

    # =====================================================
    # READ
    # =====================================================

    def read(self):

        if self.serial is None:
            return

        if not self.serial.is_open:
            return

        while self.serial.in_waiting:

            try:

                line = (
                    self.serial
                    .readline()
                    .decode(errors="ignore")
                    .strip()
                )

            except Exception:

                continue

            if not line:
                continue

            self.raw_data.emit(line)

            self.parse(line)

    # =====================================================
    # PARSE
    # =====================================================

    def parse(self, line):

        part = line.split(",")

        if len(part) == 0:
            return

        packet_type = part[0]

        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        if packet_type == "STATUS":

            if len(part) >= 2:

                self.status_received.emit(part[1])

            return

        # -------------------------------------------------
        # CLOCK
        # -------------------------------------------------

        if packet_type == "CLOCK":
            if len(part) != 2:
                return

            try:

                clock = int(part[1])

            except Exception:

                return

            self.current_clock = clock

            self.clock_received.emit(clock)

            return

        # -------------------------------------------------
        # EVENT
        # -------------------------------------------------

        if packet_type == "EVENT":

            if len(part) != 3:
                return

            try:
                sensor, state = part[1].split("_")
                timestamp = int(part[2])

            except Exception:
                return

            event = SensorEvent(
                sensor=sensor,
                state=state,
                timestamp=timestamp
            )

            self.sensor_event.emit(event)
