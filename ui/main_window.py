from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QComboBox,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QStackedWidget,
)

from config import (
    MODE_START_FINISH,
    MODE_LAP,
    MODE_BRAKE,
    MODE_HILL,
)

from ui.pages.start_finish_page import StartFinishPage
from ui.pages.lap_page import LapPage
from ui.pages.brake_page import BrakePage
from ui.pages.hill_page import HillPage


class MainWindow(QMainWindow):

    # ==========================================
    # SIGNAL
    # ==========================================

    mode_changed = Signal(str)
    reset_requested = Signal()

    refresh_serial_requested = Signal()
    connect_serial_requested = Signal()

    export_requested = Signal()

    # ==========================================
    # INIT
    # ==========================================

    def __init__(self):

        super().__init__()

        self.setWindowTitle("KMLI System")
        self.resize(900, 700)

        self.init_ui()

    # ==========================================
    # UI
    # ==========================================

    def init_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # =====================================================
        # HEADER
        # =====================================================

        header_layout = QHBoxLayout()

        title = QLabel("<h2>KMLI System</h2>")

        serial_label = QLabel("Serial Port :")

        self.serial_combo = QComboBox()

        self.refresh_button = QPushButton("Refresh")

        self.connect_button = QPushButton("Connect")

        self.status_label = QLabel("🔴 Disconnected")

        header_layout.addWidget(title)

        header_layout.addStretch()

        header_layout.addWidget(serial_label)
        header_layout.addWidget(self.serial_combo, 1)
        header_layout.addWidget(self.refresh_button)
        header_layout.addWidget(self.connect_button)

        header_layout.addSpacing(20)

        header_layout.addWidget(self.status_label)

        main_layout.addLayout(header_layout)

        # =====================================================
        # MODE
        # =====================================================

        mode_group = QGroupBox("Race Mode")

        mode_layout = QHBoxLayout()

        self.mode_combo = QComboBox()

        self.mode_combo.addItem("Slalom", MODE_START_FINISH)
        self.mode_combo.addItem("Endurance", MODE_LAP)
        self.mode_combo.addItem("Akselaris Deselerasi", MODE_BRAKE)
        self.mode_combo.addItem("Daya Tanjak", MODE_HILL)

        mode_layout.addWidget(self.mode_combo)
        mode_group.setLayout(mode_layout)

        main_layout.addWidget(mode_group)

        # =====================================================
        # DASHBOARD
        # =====================================================

        self.dashboard = QStackedWidget()

        self.start_finish_page = StartFinishPage()
        self.lap_page = LapPage()
        self.brake_page = BrakePage()
        self.hill_page = HillPage()

        self.dashboard.addWidget(self.start_finish_page)
        self.dashboard.addWidget(self.lap_page)
        self.dashboard.addWidget(self.brake_page)
        self.dashboard.addWidget(self.hill_page)

        main_layout.addWidget(self.dashboard, 1)

        # =====================================================
        # FOOTER
        # =====================================================

        footer_layout = QHBoxLayout()

        footer_layout.addStretch()

        self.export_button = QPushButton("Export Database")

        self.reset_button = QPushButton("Reset System")

        footer_layout.addWidget(self.export_button)
        footer_layout.addSpacing(10)
        footer_layout.addWidget(self.reset_button)

        main_layout.addLayout(footer_layout)

        # =====================================================
        # SIGNAL
        # =====================================================

        self.mode_combo.currentIndexChanged.connect(
            self.on_mode_changed
        )

        self.reset_button.clicked.connect(
            self.on_reset_clicked
        )

        self.refresh_button.clicked.connect(
            self.refresh_serial_requested.emit
        )

        self.connect_button.clicked.connect(
            self.connect_serial_requested.emit
        )

        self.export_button.clicked.connect(
            self.export_requested.emit
        )

    # ==========================================
    # CALLBACK
    # ==========================================

    def on_mode_changed(self):

        mode = self.mode_combo.currentData()

        self.set_page(mode)

        self.mode_changed.emit(mode)

    def on_reset_clicked(self):

        self.clear_log()

        self.reset_requested.emit()

    # ==========================================
    # SERIAL
    # ==========================================

    def set_serial_ports(self, ports):

        self.serial_combo.clear()
        self.serial_combo.addItems(ports)


    def selected_serial_port(self):

        return self.serial_combo.currentText()


    def set_connect_button_text(self, text):

        self.connect_button.setText(text)

    # ==========================================
    # PUBLIC
    # ==========================================

    def set_status(self, text):

        self.status_label.setText(text)

    def add_log(self, text):

        pass

    def clear_log(self):

        pass

    def set_page(self, mode):

        if mode == MODE_START_FINISH:

            self.dashboard.setCurrentWidget(
                self.start_finish_page
            )

        elif mode == MODE_LAP:

            self.dashboard.setCurrentWidget(
                self.lap_page
            )

        elif mode == MODE_BRAKE:

            self.dashboard.setCurrentWidget(
                self.brake_page
            )

        elif mode == MODE_HILL:

            self.dashboard.setCurrentWidget(
                self.hill_page
            )

    # ==========================================
    # ACCESSOR
    # ==========================================

    def start_finish(self):

        return self.start_finish_page

    def lap(self):

        return self.lap_page

    def brake(self):

        return self.brake_page

    def hill(self):

        return self.hill_page
