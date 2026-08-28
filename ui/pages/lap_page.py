from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
)

from ui.participant_panel import ParticipantPanel
from ui.database_table import DatabaseTable


class LapPage(QWidget):

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

        title = QLabel("ENDURANCE")
        running_title = QLabel("RUNNING TIME")
        self.timer_label = QLabel("0.000 s")
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

        running_title.setAlignment(Qt.AlignCenter)

        running_title.setStyleSheet("""
            QLabel{
                font-size:16px;
                font-weight:bold;
            }
        """)

        self.timer_label.setAlignment(Qt.AlignCenter)

        self.timer_label.setStyleSheet("""
            QLabel{
                font-size:34px;
                font-weight:bold;
                color:#0066CC;
            }
        """)

        left_layout.addSpacing(10)
        left_layout.addWidget(running_title)
        left_layout.addWidget(self.timer_label)
        left_layout.addSpacing(15)

        # =====================================================
        # LAP TABLE
        # =====================================================

        frame = QFrame()

        grid = QGridLayout(frame)

        self.lap_labels = []

        for i in range(2):

            name = QLabel(f"Lap {i+1}")

            name.setStyleSheet("""
                QLabel{
                    font-size:20px;
                    font-weight:bold;
                }
            """)

            value = QLabel("0.000 s")

            value.setAlignment(Qt.AlignRight)

            value.setStyleSheet("""
                QLabel{
                    font-size:24px;
                }
            """)

            grid.addWidget(name, i, 0)
            grid.addWidget(value, i, 1)

            self.lap_labels.append(value)

        left_layout.addWidget(frame)

        # =====================================================
        # TOTAL
        # =====================================================

        total_frame = QFrame()

        total_grid = QGridLayout(total_frame)

        total_title = QLabel("TOTAL")

        total_title.setStyleSheet("""
            QLabel{
                font-size:22px;
                font-weight:bold;
            }
        """)

        self.total_label = QLabel("0.000 s")

        self.total_label.setAlignment(Qt.AlignRight)

        self.total_label.setStyleSheet("""
            QLabel{
                font-size:34px;
                font-weight:bold;
                color:#0066CC;
            }
        """)

        total_grid.addWidget(total_title, 0, 0)
        total_grid.addWidget(self.total_label, 0, 1)

        left_layout.addWidget(total_frame)

        # =====================================================
        # RESULT
        # =====================================================

        result_frame = QFrame()

        result_grid = QGridLayout(result_frame)

        result_title = QLabel("RESULT")

        result_title.setStyleSheet("""
            QLabel{
                font-size:22px;
                font-weight:bold;
            }
        """)

        self.result_label = QLabel("READY")

        self.result_label.setAlignment(Qt.AlignRight)

        self.result_label.setStyleSheet("""
            QLabel{
                font-size:34px;
                font-weight:bold;
                color:gray;
            }
        """)

        result_grid.addWidget(result_title, 0, 0)
        result_grid.addWidget(self.result_label, 0, 1)

        left_layout.addWidget(result_frame)

        self.participant = ParticipantPanel()
        content_layout.addWidget(
            self.participant,
            1
        )

        left_layout.addStretch()

        self.database_table = DatabaseTable(
            title="HASIL ENDURANCE",
            headers=[
                "No Urut",
                "Nama Team",
                "Universitas",
                "Lap 1 (s)",
                "Lap 2 (s)",
                "Total (s)",
                "Status",
            ]
        )

        layout.addWidget(self.database_table)

    # =====================================================
    # PUBLIC
    # =====================================================

    def set_lap(self, lap_number, value):

        if 1 <= lap_number <= 2:

            self.lap_labels[lap_number - 1].setText(f"{value:.3f} s")

    def set_total(self, value):

        self.total_label.setText(f"{value:.3f} s")

    def set_result(self, passed):

        if passed is None:

            self.result_label.setText("READY")
            self.result_label.setStyleSheet("""
                QLabel{
                    font-size:34px;
                    font-weight:bold;
                    color:gray;
                }
            """)

        elif passed:

            self.result_label.setText("PASS")
            self.result_label.setStyleSheet("""
                QLabel{
                    font-size:34px;
                    font-weight:bold;
                    color:green;
                }
            """)

        else:

            self.result_label.setText("FAIL")
            self.result_label.setStyleSheet("""
                QLabel{
                    font-size:34px;
                    font-weight:bold;
                    color:red;
                }
            """)

    def reset(self):

        for label in self.lap_labels:

            label.setText("0.000 s")

        self.set_total(0.0)
        self.set_timer(0.0)
        self.set_result(None)

    def set_timer(self, seconds):

        self.timer_label.setText(f"{seconds:.3f} s")
