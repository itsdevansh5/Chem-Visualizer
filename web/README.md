# Chemical Equipment Parameter Visualizer  
### Hybrid Web + Desktop Application  
(React + Django REST + PyQt5 + Matplotlib)

This project is a **hybrid application** that runs both as a **Web App** (React.js) and a **Desktop App** (PyQt5), powered by a **single shared Django REST API backend**. It allows users to upload chemical equipment CSV files, generate summary analytics, view visualizations, browse upload history, and download a PDF report.

---

# 📌 Features

### 🔹 1. CSV Upload (Web & Desktop)
Upload CSV files containing:
- Equipment Name  
- Type  
- Flowrate  
- Pressure  
- Temperature  

The backend processes the CSV using **Pandas**.

### 🔹 2. Automated Data Summary
Backend computes:
- Total count of records  
- Average Flowrate, Pressure, Temperature  
- Equipment Type distribution  

### 🔹 3. Data Visualization
**Web:** Chart.js  
**Desktop:** Matplotlib  
Visualizations include equipment-type distribution charts.

### 🔹 4. Data Preview
Shows first 10 rows of uploaded dataset in both frontends.

### 🔹 5. Upload History
Backend stores the **last 5 uploaded datasets** using SQLite.

### 🔹 6. PDF Report Generator
Backend generates a PDF containing:
- Dataset name  
- Upload time  
- Summary statistics  
- Type distribution  

### 🔹 7. Authentication
Implemented using:
- **Django Token Authentication**
React & PyQt send token in headers for every API request.

---

# 🛠 Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Backend | Django, DRF, Pandas, ReportLab | API, CSV parsing, summaries, PDF |
| Database | SQLite | Store dataset metadata |
| Web Frontend | React.js (Vite), Axios, Chart.js | UI, CSV upload, charts |
| Desktop Frontend | PyQt5, Matplotlib, Requests | Desktop UI |
| Version Control | Git + GitHub | Project submission |

---

# 📂 Project Structure

chem-visualizer/
│
├── backend/
│ ├── chemviz/
│ ├── api/
│ ├── db.sqlite3
│ ├── manage.py
│ └── sample_equipment_data.csv
│
├── web/
│ ├── index.html
│ ├── vite.config.js
│ └── src/
│ ├── App.jsx
│ ├── UploadForm.jsx
│ ├── DataTable.jsx
│ ├── Charts.jsx
│ ├── HistoryList.jsx
│ └── config.js
│
├── desktop/
│ ├── desktop_app.py
│ └── config.py
│
├── requirements.txt
├── README.md
└── .gitignore


---

# 🚀 Backend Setup (Django REST API)

### 1️⃣ Create Virtual Environment
```bash
python -m venv .venv


Activate (Windows PowerShell):

.\.venv\Scripts\Activate.ps1

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate

4️⃣ Create Superuser
python manage.py createsuperuser

5️⃣ Run Backend
python manage.py runserver


Backend runs at:
👉 http://127.0.0.1:8000/

🔑 Authentication Setup (Token Based)
Generate token using:
POST http://127.0.0.1:8000/api/token-auth/


Payload:

username=<your_username>
password=<your_password>


Response:

{"token": "your_generated_token"}


Store this token in:

Web:
web/src/config.js

Desktop:
desktop/config.py


All API requests send:

Authorization: Token <your_token>

🌐 Web Frontend Setup (React + Vite)
1️⃣ Install dependencies
cd web
npm install

2️⃣ Run Web App
npm run dev


Open in browser:
👉 http://localhost:5173/

Web Features:

Upload CSV

Show preview

Show charts

Show history

Download PDF

💻 Desktop App Setup (PyQt5)
1️⃣ Run the app
cd desktop
python desktop_app.py

Desktop Features:

Upload CSV

Show preview table

Bar chart visualization

View upload history

Load previous datasets

Download PDF

📡 API Endpoints
Method	Endpoint	Description
POST	/api/upload/	Upload new CSV
GET	/api/history/	Fetch last 5 uploads
GET	/api/summary/<id>/	Get summary of dataset
GET	/api/report/<id>/	Download dataset PDF
POST	/api/token-auth/	Generate API token
🧪 Sample CSV File
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-A,Pump,120.5,2.5,75
Pump-B,Pump,110.0,2.1,72
Valve-C,Valve,0,1.2,60
Reactor-1,Reactor,500,5.2,200
HeatEx-1,HeatExchanger,300,3.8,150
Condenser-1,Condenser,250,3.0,120
Filter-1,Filter,50,1.0,40