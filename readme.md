
# Chemical Equipment Parameter Visualizer (Hybrid Web + Desktop App)

A full-stack hybrid application that runs as both:

- 🌐 **Web Application (React + Chart.js)**
- 💻 **Desktop Application (PyQt5 + Matplotlib)**  
- ⚙️ **Backend REST API (Django + DRF)**

The app allows users to upload chemical equipment datasets (CSV), view automated summaries, visualize charts, store upload history, and generate PDF reports — all using a **single shared backend**.

---

# 📌 Features

### 🔹 **1. CSV Upload (Web + Desktop)**
Users upload CSV files containing:
- Equipment Name  
- Type  
- Flowrate  
- Pressure  
- Temperature  

The backend processes and stores the dataset.

### 🔹 **2. Automated Summary Statistics**
Backend (Pandas) computes:
- Total record count  
- Averages (Flowrate, Pressure, Temperature)  
- Equipment type distribution  

### 🔹 **3. Data Visualization**
- **Web:** Chart.js  
- **Desktop:** Matplotlib  
Displays equipment type distribution and preview tables.

### 🔹 **4. History Management**
Backend stores last **5 uploaded datasets** in SQLite.

### 🔹 **5. PDF Report Generator**
Backend generates downloadable PDF report containing:
- Dataset info  
- Summary  
- Type chart information  

### 🔹 **6. Authentication**
Implemented using **Django Token Authentication**.  
React + PyQt send token using headers.

### 🔹 **7. Hybrid Frontend**
- Web Frontend (React/Vite)  
- Desktop Frontend (PyQt5)

Both communicate with the same REST API.

---

# 🛠 Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend (Web) | React.js, Chart.js | CSV upload, table, charts |
| Frontend (Desktop) | PyQt5, Matplotlib | Desktop GUI with visualizations |
| Backend | Django, Django REST Framework | API + Auth + PDF |
| Data Processing | Pandas | CSV parsing & analytics |
| Database | SQLite | Store uploaded datasets |
| Version Control | Git + GitHub | Submission + collaboration |

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
│ ├── package.json
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

yaml
Copy code

---

# 🚀 Backend Setup (Django REST API)

### **1. Create virtual environment**
```bash
python -m venv .venv
Activate:

PowerShell:

bash
Copy code
.\.venv\Scripts\Activate.ps1
2. Install dependencies
bash
Copy code
pip install -r requirements.txt
3. Run migrations
bash
Copy code
python manage.py makemigrations
python manage.py migrate
4. Create superuser
bash
Copy code
python manage.py createsuperuser
5. Start backend
bash
Copy code
python manage.py runserver
Backend URL:
👉 http://127.0.0.1:8000/

🔑 Authentication (Token Based)
Generate token using:

bash
Copy code
POST /api/token-auth/
React & PyQt store token inside:

web/src/config.js

desktop/config.py

Token header for all API calls:

makefile
Copy code
Authorization: Token <your_token>
🌐 Web Frontend Setup (React + Vite)
bash
Copy code
cd web
npm install
npm run dev
Web App URL:
👉 http://localhost:5173/

Features:

Upload CSV

View Preview Table

View Bar Chart

View History

Download PDF

💻 Desktop App Setup (PyQt5)
bash
Copy code
cd desktop
python desktop_app.py
Features:

Upload CSV

Table preview

Matplotlib charts

Summary view

📡 API Endpoints
Method	Endpoint	Description
POST	/api/upload/	Upload CSV file
GET	/api/history/	Fetch last 5 uploads
GET	/api/summary/<id>/	Get summary of dataset
GET	/api/report/<id>/	Download PDF report
POST	/api/token-auth/	Generate auth token