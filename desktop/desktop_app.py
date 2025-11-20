import sys
import pandas as pd
import requests
from io import StringIO

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QFileDialog, QTableWidget,
    QTableWidgetItem, QLabel, QMessageBox
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# Import API URL & TOKEN from config file
from config import API_URL, TOKEN


# ------------------------------------
# Matplotlib Canvas
# ------------------------------------
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        fig = Figure(figsize=(5, 4))
        self.ax = fig.add_subplot(111)
        super().__init__(fig)


# ------------------------------------
# Main Window
# ------------------------------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer — Desktop")
        self.setMinimumSize(900, 600)

        self.layout = QVBoxLayout()

        # Upload button
        self.btn = QPushButton("Upload CSV")
        self.btn.clicked.connect(self.upload_csv)

        # Info label
        self.info_label = QLabel("Upload a CSV file to begin.")
        self.info_label.setStyleSheet("font-size: 14px; font-weight: bold;")

        # Table preview
        self.table = QTableWidget()

        # Chart area
        self.chart = MplCanvas(self)

        # Add to layout
        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.info_label)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.chart)

        self.setLayout(self.layout)

    # ------------------------------------
    # Upload CSV to backend
    # ------------------------------------
    def upload_csv(self):
        fname, _ = QFileDialog.getOpenFileName(
            self, "Choose CSV File", "", "CSV Files (*.csv)"
        )

        if not fname:
            return

        # Send to backend
        try:
            files = {"file": open(fname, "rb")}
            data = {"name": fname.split("/")[-1]}
            headers = {"Authorization": f"Token {TOKEN}"}

            res = requests.post(API_URL + "upload/", files=files, data=data, headers=headers)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Upload failed: {str(e)}")
            return

        if res.status_code != 201:
            QMessageBox.critical(self, "Error", f"Server Error: {res.text}")
            return

        result = res.json()

        # Update UI with backend data
        self.show_table(result["preview_csv"])
        self.show_chart(result["summary"])

        self.info_label.setText(
            f"Uploaded: {result['name']} | Total Rows: {result['summary']['total_count']}"
        )

    # ------------------------------------
    # Table Preview (first 10 rows)
    # ------------------------------------
    def show_table(self, preview_csv):
        df = pd.read_csv(StringIO(preview_csv))

        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df))
        self.table.setHorizontalHeaderLabels(df.columns)

        for i in range(len(df)):
            for j in range(len(df.columns)):
                self.table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))

    # ------------------------------------
    # Bar Chart for Type Distribution
    # ------------------------------------
    def show_chart(self, summary):
        type_dist = summary["type_distribution"]

        labels = list(type_dist.keys())
        values = list(type_dist.values())

        self.chart.ax.clear()
        self.chart.ax.bar(labels, values)
        self.chart.ax.set_title("Equipment Type Distribution")
        self.chart.ax.set_xlabel("Type")
        self.chart.ax.set_ylabel("Count")
        self.chart.draw()


# ------------------------------------
# Start Application
# ------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
