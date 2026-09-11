import sys

from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
    QFileDialog,
)
from PySide6.QtCore import QTimer

from config import (
    SERIAL_PORT,
    BAUDRATE,
    MODE_START_FINISH,
    MODE_LAP,
    MODE_BRAKE,
    MODE_HILL,
)

from serial_manager import SerialManager
from database.database import DatabaseManager
from database.excel_export import export_database

from race_engine.start_finish import StartFinish
from race_engine.lap import Lap
from race_engine.brake_system import BrakeSystem
from race_engine.hill import Hill

from ui.main_window import MainWindow
from datetime import datetime


class Application:

    def __init__(self):

        # =====================================================
        # DATABASE
        # =====================================================

        self.database = DatabaseManager()

        # =====================================================
        # GUI
        # =====================================================

        self.window = MainWindow()

        # =====================================================
        # SERIAL
        # =====================================================

        self.serial = SerialManager()
        self.serial_connected = False

        # =====================================================
        # RACE ENGINE
        # =====================================================

        self.start_finish = StartFinish()
        self.lap = Lap()
        self.brake = BrakeSystem()
        self.hill = Hill()

        # =====================================================
        # CURRENT ENGINE
        # =====================================================

        self.current_mode = MODE_START_FINISH
        self.current_engine = self.start_finish

        self.brake_start_timestamp = None
        self.brake_timer_running = False

        # =====================================================
        # GUI SIGNAL
        # =====================================================

        self.window.mode_changed.connect(
            self.set_race_mode
        )

        self.window.reset_requested.connect(
            self.on_reset_requested
        )

        self.window.brake_page.calculate_requested.connect(
            self.on_brake_calculate
        )

        self.window.brake_page.reset_requested.connect(
            self.on_brake_reset
        )

        self.window.hill_page.mass_changed.connect(
            self.on_hill_mass_changed
        )

        self.window.start_finish_page.participant.save_button.clicked.connect(
            self.on_save_slalom
        )

        self.window.lap_page.participant.save_button.clicked.connect(
            self.on_save_lap
        )

        self.window.brake_page.participant.save_button.clicked.connect(
            self.on_save_brake
        )

        self.window.hill_page.participant.save_button.clicked.connect(
            self.on_save_hill
        )

        self.window.refresh_serial_requested.connect(
            self.refresh_serial_ports
        )

        self.window.connect_serial_requested.connect(
            self.on_connect_serial
        )

        self.window.export_requested.connect(
            self.on_export_database
        )

        self.window.clear_database_requested.connect(
            self.on_clear_database
        )

        # =====================================================
        # SERIAL SIGNAL
        # =====================================================

        self.serial.connected.connect(self.on_connected)
        self.serial.disconnected.connect(self.on_disconnected)
        self.serial.error.connect(self.on_error)
        self.serial.raw_data.connect(self.on_raw_data)
        self.serial.sensor_event.connect(self.on_sensor_event)
        self.serial.clock_received.connect(self.on_clock_received)

        # =====================================================
        # START FINISH SIGNAL
        # =====================================================

        self.start_finish.race_started.connect(
            self.on_race_started
        )

        self.start_finish.race_finished.connect(
            self.on_race_finished
        )

        # =====================================================
        # HILL SIGNAL
        # =====================================================

        self.hill.race_started.connect(
            self.on_hill_started
        )

        self.hill.race_finished.connect(
            self.on_hill_finished
        )

        # =====================================================
        # LAP SIGNAL
        # =====================================================

        self.lap.lap_finished.connect(
            self.on_lap_finished
        )

        self.lap.lap_completed.connect(
            self.on_lap_completed
        )

        self.brake.brake_finished.connect(
            self.on_brake_finished
        )

        # =====================================================
        # SERIAL POLLING
        # =====================================================

        self.timer = QTimer()
        self.timer.timeout.connect(self.serial.read)
        self.timer.start(1)

        # =====================================================
        # CONNECT SERIAL
        # =====================================================

        self.refresh_serial_ports()

        # =====================================================
        # DEFAULT MODE
        # =====================================================

        self.set_race_mode(MODE_START_FINISH)

        self.load_slalom_table()
        self.load_lap_table()
        self.load_brake_table()
        self.load_hill_table()

        # =====================================================
        # SHOW
        # =====================================================

        self.window.show()

    # =====================================================
    # CHANGE MODE
    # =====================================================

    def set_race_mode(self, mode):

        self.current_mode = mode

        if mode == MODE_START_FINISH:

            self.current_engine = self.start_finish

        elif mode == MODE_LAP:

            self.current_engine = self.lap

        elif mode == MODE_BRAKE:

            self.current_engine = self.brake
            self.brake.reset()
            self.brake_start_timestamp = None
            self.brake_timer_running = False
            self.window.brake_page.reset()

        elif mode == MODE_HILL:

            self.current_engine = self.hill
            self.hill.reset()
            self.window.hill_page.reset()

        self.window.set_page(mode)

        self.window.add_log("")
        self.window.add_log(f"Race Mode : {mode}")
        self.window.add_log("--------------------------------")

    # =====================================================
    # SAVE HILL
    # =====================================================

    def on_save_hill(self):

        participant = (
            self.window
            .hill_page
            .participant
        )

        if not participant.is_valid():

            QMessageBox.warning(
                self.window,
                "Data Belum Lengkap",
                "Silakan isi No Urut, Nama Team, dan Universitas terlebih dahulu."
            )

            return

        data = participant.data()

        self.database.save_hill(
            data["nama_team"],
            data["no_urut"],
            data["universitas"],
            self.hill.mass,
            self.hill.elapsed_time,
            self.hill.speed,
            self.hill.power,
            data["status"]
        )

        self.load_hill_table()

        self.window.add_log(
            "[DATABASE] Data hill berhasil disimpan."
        )

        QMessageBox.information(
            self.window,
            "Berhasil",
            "Data berhasil disimpan ke database."
        )

        participant.clear()

    # =====================================================
    # LOAD HILL TABLE
    # =====================================================

    def load_hill_table(self):

        rows = self.database.get_hill()

        self.window.hill_page.database_table.load_data(
            rows
        )

    # =====================================================
    # SAVE SLALOM
    # =====================================================

    def on_save_slalom(self):

        participant = (
            self.window
            .start_finish_page
            .participant
        )

        if not participant.is_valid():

            QMessageBox.warning(
                self.window,
                "Data Belum Lengkap",
                "Silakan isi No Urut, Nama Team, dan Universitas terlebih dahulu."
            )

            return

        data = participant.data()

        self.database.save_slalom(
            data["nama_team"],
            data["no_urut"],
            data["universitas"],
            self.start_finish.elapsed_time,
            self.start_finish.speed,
            data["status"]
        )

        self.load_slalom_table()

        self.window.add_log(
            "[DATABASE] Data slalom berhasil disimpan."
        )

        QMessageBox.information(
            self.window,
            "Berhasil",
            "Data berhasil disimpan ke database."
        )

        participant.clear()

    # =====================================================
    # SAVE LAP
    # =====================================================

    def on_save_lap(self):

        participant = (
            self.window
            .lap_page
            .participant
        )

        if not participant.is_valid():

            QMessageBox.warning(
                self.window,
                "Data Belum Lengkap",
                "Silakan isi No Urut, Nama Team, dan Universitas terlebih dahulu."
            )

            return

        data = participant.data()

        self.database.save_lap(
            data["nama_team"],
            data["no_urut"],
            data["universitas"],
            self.lap.lap1,
            self.lap.lap2,
            self.lap.total_time,
            data["status"]
        )

        self.load_lap_table()

        self.window.add_log(
            "[DATABASE] Data endurance berhasil disimpan."
        )

        QMessageBox.information(
            self.window,
            "Berhasil",
            "Data berhasil disimpan ke database."
        )

        participant.clear()

    # =====================================================
    # RESET SYSTEM
    # =====================================================

    def on_reset_requested(self):

        self.lap.reset()
        self.brake.reset()
        self.hill.reset()
        self.start_finish.clear_result()

        self.brake_start_timestamp = None
        self.brake_timer_running = False

        self.window.start_finish_page.reset()
        self.window.lap_page.reset()
        self.window.brake_page.reset()
        self.window.hill_page.reset()

        self.serial.write("CMD,RESET")


    # =====================================================
    # LAP COMPLETED CALLBACK
    # =====================================================
    def on_lap_completed(self, lap_number, lap_time):

        self.window.lap_page.set_lap(
            lap_number,
            lap_time
        )

        self.window.add_log(
            f"Lap {lap_number} : {lap_time:.3f} s"
        )

    # =====================================================
    # SERIAL CALLBACK
    # =====================================================

    def on_connected(self):

        self.serial_connected = True

        self.window.set_status("🟢 Connected")

        self.window.set_connect_button_text(
            "Disconnect"
        )

    def on_disconnected(self):

        self.serial_connected = False

        self.window.set_status("🔴 Disconnected")

        self.window.set_connect_button_text(
            "Connect"
        )

    def on_error(self, message):

        self.window.add_log(f"[ERROR] {message}")

    def on_raw_data(self, data):

        self.window.add_log(f"[RAW] {data}")

    def on_sensor_event(self, event):

        self.window.add_log(
        f"[EVENT] {event.sensor} {event.state} {event.timestamp}"
        )

        if self.current_mode == MODE_HILL:

            self.hill.set_mass(
                self.window.hill_page.mass()
            )

        if self.current_engine is not None:

            self.current_engine.process_event(event)

        if self.current_mode == MODE_BRAKE:
            if event.sensor == "S1" and event.state == "ON":
                self.brake_start_timestamp = event.timestamp
                self.brake_timer_running = True
                self.window.brake_page.set_status("WAITING")
            elif event.sensor == "S2" and event.state == "ON":
                self.brake_timer_running = False

    # =====================================================
    # HILL CALLBACK
    # =====================================================
    def on_hill_started(self):

        self.window.hill_page.set_status("RUNNING")

        self.window.add_log("")
        self.window.add_log("========== HILL STARTED ==========")

    def on_hill_finished(self, elapsed,speed,power):

        self.window.hill_page.set_timer(elapsed)
        self.window.hill_page.set_time(elapsed)
        self.window.hill_page.set_speed(speed)
        self.window.hill_page.set_power(power)
        self.window.hill_page.set_status("FINISH")

        self.window.add_log("")
        self.window.add_log("========== HILL RESULT ==========")
        self.window.add_log(
            f"Mass  : {self.hill.mass:.1f} kg"
        )
        self.window.add_log(
            f"Time  : {elapsed:.3f} s"
        )
        self.window.add_log(
            f"Speed : {speed:.2f} km/h"
        )
        self.window.add_log(
            f"Power : {power:.2f} kW"
        )
        self.window.add_log("")

    def on_hill_mass_changed(self, mass):

        self.hill.set_mass(mass)

        if mass > 0:
            self.window.hill_page.set_status("READY")
        else:
            self.window.hill_page.set_status("Masukkan massa kendaraan")

    # =====================================================
    # START FINISH CALLBACK
    # =====================================================

    def on_race_started(self):

        self.window.add_log("")
        self.window.add_log("========== RACE STARTED ==========")

    def on_race_finished(self, elapsed_time, speed):
        # Sinkronkan Running Time dengan hasil akhir
        self.window.start_finish_page.set_timer(elapsed_time)
        self.window.start_finish_page.set_time(elapsed_time)
        self.window.start_finish_page.set_speed(speed)

        self.window.add_log("")
        self.window.add_log("========== RACE FINISHED ==========")
        self.window.add_log(f"Time  : {elapsed_time:.3f} s")
        self.window.add_log(f"Speed : {speed:.2f} km/h")
        self.window.add_log("")

    # =====================================================
    # LAP CALLBACK
    # =====================================================

    def on_lap_finished(
        self,
        lap1,
        lap2,
        lap3,
        lap4,
        lap5,
        total,
        passed
    ):

        self.window.lap_page.set_lap(1, lap1)
        self.window.lap_page.set_lap(2, lap2)

        self.window.lap_page.set_timer(total)
        self.window.lap_page.set_total(total)
        self.window.lap_page.set_result(passed)

        self.window.add_log("")
        self.window.add_log("========== LAP RESULT ==========")

        self.window.add_log(f"Lap 1 : {lap1:.3f} s")
        self.window.add_log(f"Lap 2 : {lap2:.3f} s")

        self.window.add_log("-------------------------------")
        self.window.add_log(f"Total : {total:.3f} s")

        if passed:
            self.window.add_log("Result : PASS")
        else:
            self.window.add_log("Result : FAIL")

        self.window.add_log("")

    # =====================================================
    # BRAKE CALCULATE
    # =====================================================

    def on_brake_calculate(self):

        self.window.brake_page.set_status("CALCULATING")

        self.brake.calculate()

    def on_save_brake(self):

        participant = (
            self.window
            .brake_page
            .participant
        )

        if not participant.is_valid():

            QMessageBox.warning(
                self.window,
                "Data Belum Lengkap",
                "Silakan isi No Urut, Nama Team, dan Universitas terlebih dahulu."
            )

            return

        data = participant.data()

        self.database.save_brake(
            data["nama_team"],
            data["no_urut"],
            data["universitas"],
            self.brake.acceleration,
            self.brake.deceleration,
            data["status"]
        )

        self.load_brake_table()

        self.window.add_log(
            "[DATABASE] Data brake berhasil disimpan."
        )

        QMessageBox.information(
            self.window,
            "Berhasil",
            "Data berhasil disimpan ke database."
        )

        participant.clear()

    def load_brake_table(self):

        rows = self.database.get_brake()

        self.window.brake_page.database_table.load_data(
            rows
        )

    # =====================================================
    # CLOCK CALLBACK
    # =====================================================

    def on_clock_received(self, clock):

        # =============================
        # HILL
        # =============================

        if self.current_mode == MODE_HILL:

            if self.hill.start_time is None:
                return

            elapsed = (
                clock - self.hill.start_time
            ) / 1_000_000.0

            self.window.hill_page.set_timer(elapsed)

            return

        # =============================
        # BRAKE
        # =============================

        if self.current_mode == MODE_BRAKE:

            if not self.brake_timer_running:
                return

            if self.brake_start_timestamp is None:
                return

            elapsed = (
                clock - self.brake_start_timestamp
            ) / 1_000_000.0

            self.window.brake_page.set_timer(elapsed)

            return

        # =============================
        # SLALOM
        # =============================

        if self.current_mode == MODE_START_FINISH:

            if self.start_finish.start_time is None:
                return

            elapsed = (
                clock - self.start_finish.start_time
            ) / 1_000_000.0

            self.window.start_finish_page.set_timer(elapsed)

            return

        # =============================
        # LAP
        # =============================

        if self.current_mode == MODE_LAP:

            if self.lap.start_time is None:
                return

            elapsed = (
                clock - self.lap.start_time
            ) / 1_000_000.0

            self.window.lap_page.set_timer(elapsed)

    # =====================================================
    # EXPORT DATABASE
    # =====================================================

    def on_export_database(self):

        default_name = (
            f"KMLI_Results_"
            f"{datetime.now():%Y-%m-%d_%H-%M-%S}.xlsx"
        )

        filename, _ = QFileDialog.getSaveFileName(
            self.window,
            "Export Database",
            default_name,
            "Excel Workbook (*.xlsx)"
        )

        if not filename:
            return

        export_database(
            self.database,
            filename
        )

        QMessageBox.information(
            self.window,
            "Export Berhasil",
            "Database berhasil diekspor."
        )

    # =====================================================
    # CLEAR DATABASE
    # =====================================================

    def on_clear_database(self):

        reply = QMessageBox.question(
            self.window,
            "Clear Database",
            "PERINGATAN! Semua data hasil race di database akan dihapus.\n\n"
            "Data yang sudah dihapus tidak dapat dikembalikan.\n\n"
            "Apakah Anda yakin ingin menghapus seluruh database?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        self.database.clear_all_data()

        # Refresh seluruh tabel agar data yang tampil ikut kosong.
        self.load_slalom_table()
        self.load_lap_table()
        self.load_brake_table()
        self.load_hill_table()

        self.window.add_log(
            "[DATABASE] Seluruh data berhasil dihapus."
        )

        QMessageBox.information(
            self.window,
            "Database Dikosongkan",
            "Seluruh data race berhasil dihapus dari database."
        )

    # =====================================================
    # BRAKE CALLBACK
    # =====================================================

    def on_brake_finished(
        self,
        passed,
        acceleration,
        brake_speed,
        deceleration
    ):

        # Brake speed tetap dihitung internal oleh engine,
        # tetapi tidak ditampilkan maupun disimpan/export.
        self.window.brake_page.set_acceleration(
            acceleration
        )
        self.window.brake_page.set_deceleration(
            deceleration
        )

        if passed:
            self.window.brake_page.set_status("PASS")
        else:
            self.window.brake_page.set_status("FAIL")

        self.window.add_log("")
        self.window.add_log(
            "========== ACCELERATION / BRAKE RESULT =========="
        )

        if acceleration is not None:
            self.window.add_log(
                f"Acceleration : {acceleration:.2f} m/s²"
            )

        if deceleration is not None:
            self.window.add_log(
                f"Deceleration : {deceleration:.2f} m/s²"
            )

        self.window.add_log("-------------------------------")

        if passed:
            self.window.add_log("Result : PASS")
        else:
            self.window.add_log("Result : FAIL")

        self.window.add_log("")

    # =====================================================
    # BRAKE RESET
    # =====================================================

    def on_brake_reset(self):

        self.brake.reset()

        self.window.brake_page.reset()
        self.brake_start_timestamp = None
        self.brake_timer_running = False
        self.serial.write("CMD,RESET")

        self.window.add_log("")
        self.window.add_log("========== BRAKE RESET ==========")
        self.window.add_log("")

    # =====================================================
    # CLOSE
    # =====================================================

    def closeEvent(self, event):

        self.database.close()

        super().closeEvent(event)

    def close(self):

        self.serial.disconnect()

    # =====================================================
    # LOAD SLALOM TABLE
    # =====================================================

    def load_slalom_table(self):

        rows = self.database.get_slalom()

        self.window.start_finish_page.database_table.load_data(
            rows
        )

    # =====================================================
    # LOAD LAP TABLE
    # =====================================================

    def load_lap_table(self):

        rows = self.database.get_lap()

        self.window.lap_page.database_table.load_data(
            rows
        )

    # =====================================================
    # SERIAL PORT
    # =====================================================

    def refresh_serial_ports(self):

        ports = self.serial.available_ports()

        self.window.set_serial_ports(ports)

    def on_connect_serial(self):

        if self.serial_connected:

            self.serial.disconnect()

            return

        port = self.window.selected_serial_port()

        if not port:

            QMessageBox.warning(
                self.window,
                "Serial",
                "Silakan pilih Serial Port."
            )

            return

        self.serial.connect(
            port,
            BAUDRATE
        )


if __name__ == "__main__":

    qt_app = QApplication(sys.argv)

    application = Application()

    try:

        sys.exit(qt_app.exec())

    finally:

        application.close()
