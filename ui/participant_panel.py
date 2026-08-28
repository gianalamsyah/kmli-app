from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QButtonGroup,
    QGroupBox,
    QFormLayout,
    QHBoxLayout,
    QVBoxLayout,
)


class ParticipantPanel(QGroupBox):

    def __init__(self):

        super().__init__("DATA PESERTA")

        self.init_ui()

    # =====================================================
    # UI
    # =====================================================

    def init_ui(self):

        layout = QVBoxLayout(self)

        form = QFormLayout()

        # No Urut

        self.no_urut_edit = QLineEdit()

        form.addRow("No Urut", self.no_urut_edit)

        # Nama Team

        self.team_edit = QLineEdit()

        form.addRow("Nama Team", self.team_edit)

        # Universitas

        self.university_edit = QLineEdit()

        form.addRow("Universitas", self.university_edit)

        layout.addLayout(form)

        # =====================================================
        # STATUS
        # =====================================================

        status_title = QLabel("Status")

        status_title.setAlignment(Qt.AlignLeft)

        layout.addWidget(status_title)

        status_layout = QHBoxLayout()

        self.pass_radio = QRadioButton("PASS")
        self.fail_radio = QRadioButton("FAIL")

        self.pass_radio.setChecked(True)

        self.status_group = QButtonGroup(self)

        self.status_group.addButton(self.pass_radio)
        self.status_group.addButton(self.fail_radio)

        status_layout.addWidget(self.pass_radio)
        status_layout.addWidget(self.fail_radio)

        layout.addLayout(status_layout)

        # =====================================================
        # SAVE
        # =====================================================

        self.save_button = QPushButton("SAVE")

        self.save_button.setMinimumHeight(40)

        layout.addSpacing(10)

        layout.addWidget(self.save_button)

        layout.addStretch()

    # =====================================================
    # PUBLIC
    # =====================================================

    def data(self):

        return {
            "no_urut": self.no_urut_edit.text().strip(),
            "nama_team": self.team_edit.text().strip(),
            "universitas": self.university_edit.text().strip(),
            "status": "PASS" if self.pass_radio.isChecked() else "FAIL"
        }

    def is_valid(self):

        data = self.data()

        if not data["no_urut"]:
            return False

        if not data["nama_team"]:
            return False

        if not data["universitas"]:
            return False

        return True

    def clear(self):

        self.no_urut_edit.clear()
        self.team_edit.clear()
        self.university_edit.clear()

        self.pass_radio.setChecked(True)
