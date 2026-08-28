from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)

from ui.participant_panel import ParticipantPanel
from ui.database_table import DatabaseTable

class StartFinishPage(QWidget):

    def __init__(self):

        super().__init__()

        self.init_ui()

    # =====================================================
    # UI
    # =====================================================

    def init_ui(self):

        layout = QVBoxLayout(self)

        layout.setSpacing(20)

        # =====================================================
        # TITLE
        # =====================================================

        title = QLabel("SLALOM")

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
        left_layout.setSpacing(20)
        content_layout.addWidget(left_widget, 2)

        running_frame = QFrame()
        running_layout = QVBoxLayout(running_frame)

        running_layout.setSpacing(8)

        running_title = QLabel("RUNNING TIME")
        running_title.setAlignment(Qt.AlignCenter)

        running_title.setStyleSheet("""
        QLabel{
            font-size:20px;
            font-weight:bold;
        }
        """)

        self.timer_label = QLabel("0.000 s")
        self.timer_label.setAlignment(Qt.AlignCenter)

        self.timer_label.setStyleSheet("""
        QLabel{
            font-size:34px;
            font-weight:bold;
            color:#0066CC;
        }
        """)

        running_layout.addWidget(running_title)
        running_layout.addWidget(self.timer_label)

        left_layout.addWidget(running_frame)

        self.participant = ParticipantPanel()

        content_layout.addWidget(self.participant, 1)

        # =====================================================
        # TIME
        # =====================================================

        time_frame = QFrame()

        time_layout = QVBoxLayout(time_frame)

        time_title = QLabel("TIME")
        time_title.setAlignment(Qt.AlignCenter)

        time_title.setStyleSheet("""
            QLabel{
                font-size:20px;
                font-weight:bold;
            }
        """)

        self.time_label = QLabel("0.000 s")

        self.time_label.setAlignment(Qt.AlignCenter)

        self.time_label.setStyleSheet("""
            QLabel{
                font-size:60px;
                font-weight:bold;
                color:#0066CC;
            }
        """)

        time_layout.addWidget(time_title)
        time_layout.addWidget(self.time_label)

        left_layout.addWidget(time_frame)

        # =====================================================
        # SPEED
        # =====================================================

        speed_frame = QFrame()

        speed_layout = QVBoxLayout(speed_frame)

        speed_title = QLabel("SPEED")
        speed_title.setAlignment(Qt.AlignCenter)

        speed_title.setStyleSheet("""
            QLabel{
                font-size:20px;
                font-weight:bold;
            }
        """)

        self.speed_label = QLabel("0.00 km/h")

        self.speed_label.setAlignment(Qt.AlignCenter)

        self.speed_label.setStyleSheet("""
            QLabel{
                font-size:60px;
                font-weight:bold;
                color:#008000;
            }
        """)

        speed_layout.addWidget(speed_title)
        speed_layout.addWidget(self.speed_label)

        left_layout.addWidget(speed_frame)

        left_layout.addStretch()

        # =====================================================
        # DATABASE TABLE
        # =====================================================

        self.database_table = DatabaseTable(
            title="HASIL SLALOM",
            headers=[
                "No Urut",
                "Nama Team",
                "Universitas",
                "Time (s)",
                "Speed (km/h)",
                "Status",
            ]
        )

        layout.addWidget(self.database_table)

    # =====================================================
    # PUBLIC
    # =====================================================

    def set_time(self, value):

        self.time_label.setText(f"{value:.3f} s")

    def set_speed(self, value):

        self.speed_label.setText(f"{value:.2f} km/h")

    def set_timer(self, value):

        self.timer_label.setText(f"{value:.3f} s")

    def reset(self):
        self.set_timer(0.0)
        self.set_time(0.0)
        self.set_speed(0.0)
