import sys
import pandas as pd
import requests
from io import StringIO

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QTableWidget,
    QTableWidgetItem, QLabel, QMessageBox, QListWidget
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

# Import API URL & Token from config file
from config import API_URL, TOKEN


# ------------------------------------
# Matplotlib canvas for charts
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
        self.setMinimumSize(1200, 650)

        # Main layouts
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Upload button
        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)

        # History list
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.load_from_history)

        # ---------- SUMMARY CARDS ----------
        self.summary_layout = QHBoxLayout()

        self.count_label = QLabel("")
        self.flow_label = QLabel("")
        self.press_label = QLabel("")
        self.temp_label = QLabel("")

        summary_labels = [self.count_label, self.flow_label, self.press_label, self.temp_label]

        for lbl in summary_labels:
            lbl.setStyleSheet("""
                font-size: 14px;
                padding: 12px;
                border: 1px solid #ccc;
                border-radius: 8px;
                background: #ffffff;
                min-width: 160px;
                text-align: center;
            """)
            self.summary_layout.addWidget(lbl)

        # Table preview
        self.table = QTableWidget()

        # Chart
        self.chart = MplCanvas(self)

        # PDF button
        self.pdf_btn = QPushButton("Download PDF Report")
        self.pdf_btn.clicked.connect(self.download_pdf)
        self.pdf_btn.setEnabled(False)

        # Assemble layouts
        left_layout.addWidget(self.upload_btn)
        left_layout.addWidget(QLabel("History (Last 5 Uploads):"))
        left_layout.addWidget(self.history_list)

        right_layout.addLayout(self.summary_layout)
        right_layout.addWidget(self.table)
        right_layout.addWidget(self.chart)
        right_layout.addWidget(self.pdf_btn)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

        # Load history on startup
        self.load_history()


    # ------------------------------------
    # Load history from backend
    # ------------------------------------
    def load_history(self):
        try:
            headers = {"Authorization": f"Token {TOKEN}"}
            res = requests.get(API_URL + "history/", headers=headers)

            if res.status_code != 200:
                return

            self.history_list.clear()
            for item in res.json():
                self.history_list.addItem(f"{item['id']} - {item['name']}")

        except Exception:
            pass


    # ------------------------------------
    # Load data from history selection
    # ------------------------------------
    def load_from_history(self, item):
        text = item.text()
        dataset_id = text.split(" - ")[0]

        try:
            headers = {"Authorization": f"Token {TOKEN}"}
            res = requests.get(API_URL + f"summary/{dataset_id}/", headers=headers)

            if res.status_code != 200:
                QMessageBox.warning(self, "Error", "Failed to load summary.")
                return

            data = res.json()
            self.update_ui(data)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


    # ------------------------------------
    # Upload CSV to backend
    # ------------------------------------
    def upload_csv(self):
        fname, _ = QFileDialog.getOpenFileName(
            self, "Choose CSV File", "", "CSV Files (*.csv)"
        )
        if not fname:
            return

        try:
            files = {"file": open(fname, "rb")}
            data = {"name": fname.split("/")[-1]}
            headers = {"Authorization": f"Token {TOKEN}"}

            res = requests.post(API_URL + "upload/", files=files, data=data, headers=headers)

            if res.status_code != 201:
                QMessageBox.critical(self, "Error", f"Upload failed: {res.text}")
                return

            data = res.json()
            self.update_ui(data)

            # Refresh history list
            self.load_history()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Upload failed: {e}")


    # ------------------------------------
    # Update table + chart + summary
    # ------------------------------------
    def update_ui(self, data):
        self.current_id = data["id"]
        self.pdf_btn.setEnabled(True)

        summary = data["summary"]
        avg = summary["averages"]

        # Summary cards update
        self.count_label.setText(f"<b>Total Count</b><br>{summary['total_count']}")
        self.flow_label.setText(f"<b>Avg Flowrate</b><br>{avg['Flowrate']:.2f}")
        self.press_label.setText(f"<b>Avg Pressure</b><br>{avg['Pressure']:.2f}")
        self.temp_label.setText(f"<b>Avg Temperature</b><br>{avg['Temperature']:.2f}")

        # Update table
        self.show_table(data["preview_csv"])

        # Update chart
        self.show_chart(summary)


    # ------------------------------------
    # Preview table
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
    # Bar Chart
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
    # Download PDF
    # ------------------------------------
    def download_pdf(self):
        try:
            headers = {"Authorization": f"Token {TOKEN}"}
            res = requests.get(API_URL + f"report/{self.current_id}/", headers=headers)

            if res.status_code != 200:
                QMessageBox.warning(self, "Error", "Could not download PDF.")
                return

            fname, _ = QFileDialog.getSaveFileName(
                self, "Save PDF Report", f"report_{self.current_id}.pdf", "PDF Files (*.pdf)"
            )

            if fname:
                with open(fname, "wb") as f:
                    f.write(res.content)

                QMessageBox.information(self, "Success", "PDF saved successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


# ------------------------------------
# Run App
# ------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
