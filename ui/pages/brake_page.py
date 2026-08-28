from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

from ui.participant_panel import ParticipantPanel
from ui.database_table import DatabaseTable

from PySide6.QtCore import (
    Qt,
    Signal,
)


class BrakePage(QWidget):

    calculate_requested = Signal()
    reset_requested = Signal()

    def __init__(self):

        super().__init__()

        title = QLabel("AKSELERASI DESELERASI")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size:30px;
            font-weight:bold;
        """)

        status_title = QLabel("STATUS")
        status_title.setAlignment(Qt.AlignCenter)
        status_title.setStyleSheet("""
            font-size:16px;
            font-weight:bold;
        """)

        self.status_label = QLabel("READY")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
            color:blue;
        """)

        timer_title = QLabel("RUNNING TIME")
        timer_title.setAlignment(Qt.AlignCenter)
        timer_title.setStyleSheet("""
            font-size:16px;
            font-weight:bold;
        """)

        self.timer_label = QLabel("0.000 s")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("""
            font-size:34px;
            font-weight:bold;
            color:#0066CC;
        """)

        acceleration_title = QLabel("ACCELERATION")
        acceleration_title.setAlignment(Qt.AlignCenter)
        acceleration_title.setStyleSheet("""
            font-size:16px;
            font-weight:bold;
        """)

        self.acceleration_label = QLabel("0.00 m/s²")
        self.acceleration_label.setAlignment(Qt.AlignCenter)
        self.acceleration_label.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
        """)

        dec_title = QLabel("DECELERATION")
        dec_title.setAlignment(Qt.AlignCenter)
        dec_title.setStyleSheet("""
            font-size:16px;
            font-weight:bold;
        """)

        self.dec_label = QLabel("0.00 m/s²")
        self.dec_label.setAlignment(Qt.AlignCenter)
        self.dec_label.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
        """)

        self.calculate_btn = QPushButton("CALCULATE")
        self.calculate_btn.setMinimumHeight(55)
        self.calculate_btn.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)
        self.calculate_btn.clicked.connect(
            self.calculate_requested.emit
        )

        self.reset_btn = QPushButton("RESET")
        self.reset_btn.setMinimumHeight(55)
        self.reset_btn.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)
        self.reset_btn.clicked.connect(
            self.reset_requested.emit
        )

        self.participant = ParticipantPanel()

        self.database_table = DatabaseTable(
            title="HASIL AKSELERASI DESELERASI",
            headers=[
                "No Urut",
                "Nama Team",
                "Universitas",
                "Acceleration",
                "Deceleration",
                "Status",
            ]
        )

        layout = QVBoxLayout()

        content_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        layout.setSpacing(12)

        left_layout.addWidget(status_title)
        left_layout.addWidget(self.status_label)

        left_layout.addSpacing(15)

        left_layout.addWidget(timer_title)
        left_layout.addWidget(self.timer_label)

        left_layout.addSpacing(15)

        left_layout.addWidget(acceleration_title)
        left_layout.addWidget(self.acceleration_label)

        left_layout.addSpacing(10)

        left_layout.addWidget(dec_title)
        left_layout.addWidget(self.dec_label)

        left_layout.addStretch()

        left_layout.addWidget(self.calculate_btn)
        left_layout.addWidget(self.reset_btn)

        right_layout.addWidget(self.participant)
        right_layout.addStretch()

        content_layout.addLayout(left_layout, 1)
        content_layout.addLayout(right_layout, 1)

        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addLayout(content_layout)
        layout.addWidget(self.database_table)

        self.setLayout(layout)

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.timer_label.setText("0.000 s")

        self.set_status("READY")

        self.set_acceleration(None)
        self.set_deceleration(None)

    # =====================================================
    # STATUS
    # =====================================================

    def set_status(self, status):

        colors = {
            "READY": "blue",
            "WAITING": "orange",
            "CALCULATING": "purple",
            "PASS": "green",
            "FAIL": "red",
        }

        self.status_label.setText(status)

        self.status_label.setStyleSheet(f"""
            font-size:26px;
            font-weight:bold;
            color:{colors.get(status, "black")};
        """)

    # =====================================================
    # ACCELERATION
    # =====================================================

    def set_acceleration(self, value):

        if value is None:
            self.acceleration_label.setText("0.00 m/s²")
        else:
            self.acceleration_label.setText(
                f"{value:.2f} m/s²"
            )

    # =====================================================
    # DECELERATION
    # =====================================================

    def set_deceleration(self, value):

        if value is None:
            self.dec_label.setText("0.00 m/s²")
        else:
            self.dec_label.setText(
                f"{value:.2f} m/s²"
            )

    # =====================================================
    # SET TIMER
    # =====================================================

    def set_timer(self, seconds):

        self.timer_label.setText(
            f"{seconds:.3f} s"
        )
