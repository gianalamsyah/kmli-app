from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QDoubleSpinBox,
)

from ui.participant_panel import ParticipantPanel
from ui.database_table import DatabaseTable

class HillPage(QWidget):

    # ==========================================
    # SIGNAL
    # ==========================================

    mass_changed = Signal(float)

    # ==========================================
    # INIT
    # ==========================================

    def __init__(self):

        super().__init__()

        self.init_ui()

    # ==========================================
    # UI
    # ==========================================

    def init_ui(self):

        layout = QVBoxLayout(self)

        # =====================================================
        # TITLE
        # =====================================================

        title = QLabel("DAYA TANJAK")
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            QLabel{
                font-size:28px;
                font-weight:bold;
            }
        """)

        layout.addWidget(title)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        layout.addLayout(content_layout)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        content_layout.addWidget(left_widget, 1)
        self.participant = ParticipantPanel()

        content_layout.addWidget(
            self.participant,
            1
        )

        # =====================================================
        # MASS
        # =====================================================

        mass_group = QGroupBox("Massa Kendaraan")

        mass_layout = QVBoxLayout()

        self.mass_input = QDoubleSpinBox()
        self.mass_input.setStyleSheet("""
            QDoubleSpinBox{
                font-size:20px;
                min-height:40px;
            }
        """)
        self.mass_input.setDecimals(1)
        self.mass_input.setRange(0.0, 5000.0)
        self.mass_input.setSingleStep(10.0)
        self.mass_input.setSuffix(" kg")

        mass_layout.addWidget(self.mass_input)

        mass_group.setLayout(mass_layout)

        left_layout.addWidget(mass_group)

        # =====================================================
        # STATUS
        # =====================================================

        status_group = QGroupBox("Status")

        status_layout = QVBoxLayout()

        self.status_label = QLabel("Masukkan massa kendaraan")
        self.status_label.setStyleSheet("""
            QLabel{
                font-size:22px;
                font-weight:bold;
                color:gray;
            }
        """)
        self.status_label.setAlignment(Qt.AlignCenter)

        status_layout.addWidget(self.status_label)

        status_group.setLayout(status_layout)

        left_layout.addWidget(status_group)

        # =====================================================
        # RUNNING TIME
        # =====================================================

        running_group = QGroupBox("Running Time")

        running_layout = QVBoxLayout()

        self.timer_label = QLabel("0.000 s")
        self.timer_label.setStyleSheet("""
            QLabel{
                font-size:34px;
                font-weight:bold;
                color:#0066CC;
            }
        """)
        self.timer_label.setAlignment(Qt.AlignCenter)

        running_layout.addWidget(self.timer_label)

        running_group.setLayout(running_layout)

        left_layout.addWidget(running_group)

        # =====================================================
        # TIME
        # =====================================================

        time_group = QGroupBox("Time")

        time_layout = QVBoxLayout()

        self.time_label = QLabel("0.000 s")
        self.time_label.setStyleSheet("""
            QLabel{
                font-size:34px;
                font-weight:bold;
                color:#0066CC;
            }
        """)
        self.time_label.setAlignment(Qt.AlignCenter)

        time_layout.addWidget(self.time_label)

        time_group.setLayout(time_layout)

        left_layout.addWidget(time_group)

        # =====================================================
        # SPEED
        # =====================================================

        speed_group = QGroupBox("Speed")

        speed_layout = QVBoxLayout()

        self.speed_label = QLabel("0.00 km/h")
        self.speed_label.setStyleSheet("""
            QLabel{
                font-size:34px;
                font-weight:bold;
                color:#0066CC;
            }
        """)
        self.speed_label.setAlignment(Qt.AlignCenter)

        speed_layout.addWidget(self.speed_label)

        speed_group.setLayout(speed_layout)

        left_layout.addWidget(speed_group)

        # =====================================================
        # POWER
        # =====================================================

        power_group = QGroupBox("Climb Power")

        power_layout = QVBoxLayout()

        self.power_label = QLabel("0.00 kW")
        self.power_label.setStyleSheet("""
            QLabel{
                font-size:34px;
                font-weight:bold;
                color:#0066CC;
            }
        """)
        self.power_label.setAlignment(Qt.AlignCenter)

        power_layout.addWidget(self.power_label)

        power_group.setLayout(power_layout)

        left_layout.addWidget(power_group)

        left_layout.addStretch()

        self.database_table = DatabaseTable(
            title="HASIL HILL",
            headers=[
                "No Urut",
                "Nama Team",
                "Universitas",
                "Massa",
                "Waktu",
                "Kecepatan",
                "Daya",
                "Status",
            ]
        )

        layout.addWidget(self.database_table)

        # =====================================================
        # SIGNAL
        # =====================================================

        self.mass_input.valueChanged.connect(
            self.mass_changed.emit
        )

    # ==========================================
    # PUBLIC
    # ==========================================

    def mass(self):

        return self.mass_input.value()

    def set_status(self, text):

        self.status_label.setText(text)

    def set_timer(self, value):

        self.timer_label.setText(f"{value:.3f} s")

    def set_time(self, value):

        self.time_label.setText(f"{value:.3f} s")

    def set_speed(self, value):

        self.speed_label.setText(f"{value:.2f} km/h")

    def set_power(self, value):

        self.power_label.setText(f"{value:.2f} kW")

    def reset(self):

        self.set_status("Masukkan massa kendaraan")

        self.set_timer(0.0)
        self.set_time(0.0)
        self.set_speed(0.0)
        self.set_power(0.0)
