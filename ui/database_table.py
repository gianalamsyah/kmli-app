from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)


class DatabaseTable(QWidget):

    def __init__(self,title="DATABASE",headers=None):

        super().__init__()

        self.title = title
        if headers is None:
            headers = []
        self.headers = headers

        self.init_ui()

    # =====================================================
    # UI
    # =====================================================

    def init_ui(self):

        layout = QVBoxLayout(self)

        layout.setSpacing(10)

        # =====================================================
        # TITLE
        # =====================================================

        title_label = QLabel(self.title)

        title_label.setAlignment(Qt.AlignCenter)

        title_label.setStyleSheet("""
            QLabel{
                font-size:18px;
                font-weight:bold;
            }
        """)

        layout.addWidget(title_label)

        # =====================================================
        # TABLE
        # =====================================================

        self.table = QTableWidget()

        self.table.setMinimumHeight(120)

        self.table.setColumnCount(len(self.headers))

        self.table.setHorizontalHeaderLabels(
            self.headers
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        self.table.setAlternatingRowColors(True)

        self.table.verticalHeader().setVisible(False)

        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        layout.addWidget(self.table)

    # =====================================================
    # PUBLIC
    # =====================================================

    def load_data(self, rows):

        self.table.setRowCount(len(rows))

        for row_index, row in enumerate(rows):

            for col_index, value in enumerate(row):

                item = QTableWidgetItem(str(value))

                item.setTextAlignment(Qt.AlignCenter)

                self.table.setItem(
                    row_index,
                    col_index,
                    item
                )

    def clear(self):

        self.table.setRowCount(0)
