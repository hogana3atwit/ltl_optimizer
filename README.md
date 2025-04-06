# LTL Optimizer App

This full-stack application models an LTL (Less-than-Truckload) freight network to calculate optimized shipment routes, determine opportunities for bypassing service centers, and predict trailer utilization using machine learning. The system is built with:

- **Backend:** FastAPI (Python)
- **Frontend:** React (Vite + Tailwind CSS)
- **ML & Data:** Scikit-learn, Pandas

---

## 🚀 Features

### 🔁 Smart Routing Engine
- Calculates multi-leg shipment paths between origin and destination.
- Uses real-world LTL logic to simulate load legs through service centers.
- Bypasses intermediate centers only when valid freight consolidation is possible.

### 🚚 Bypass Optimization
- A center is bypassed only if the **previous** center has enough freight to build a trailer directly to the final destination.
- Matching is based on shipment cube (≤ 100 total), using data from `sample_shipments.csv`.

### 📦 Machine Learning
- Predicts trailer utilization based on weight and cube.
- Users can trigger model training directly from the dashboard.

### 📊 Dashboard Interface
- Input origin, destination, weight, and cube.
- View calculated routes, bypasses, and trailer efficiency.
- See valid service centers and logic justifications.

---

## 🧱 Project Structure

```
ltl_optimizer_app/
├── app/                   # FastAPI application
│   ├── main.py            # FastAPI routes and server entry
│   ├── models.py          # SQLAlchemy models (if used)
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py            # CRUD database logic
│   ├── ml/optimizer.py    # ML training and prediction
│   └── routing/engine.py  # Route + bypass engine
│
├── data/                 # Data files for routing and model training
│   ├── sample_shipments.csv
│   ├── service_centers_v2.csv
│   └── sample_data.csv
│
├── frontend/             # React app
│   ├── public/data/      # Service center data used by dashboard
│   └── src/Dashboard.jsx # UI logic and inputs
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-user/ltl_optimizer_app.git
cd ltl_optimizer_app
```

### 2. Run the Backend
```bash
chmod +x start.sh
./start.sh
```
This sets up a virtual environment, installs dependencies, and runs FastAPI with Uvicorn on `http://localhost:8000`.

### 3. Run the Frontend
```bash
cd frontend
npm install
npm run dev
```
The React dashboard runs at `http://localhost:5173`.

---

## 🛠 Dependencies

### Backend
- FastAPI
- Pandas
- Scikit-learn
- Uvicorn

### Frontend
- React + Vite
- Tailwind CSS

---

## 🧪 Testing the App

1. Open your browser at `http://localhost:5173`
2. Select origin and destination (e.g., BOS → LAX)
3. Input weight and cube
4. Click "Calculate Route"
5. View routing decision, bypass reasoning, and predicted utilization

---

## 🎥 Application Demo

[![YouTube](http://i.ytimg.com/vi/eyyUXmFxxP0/hqdefault.jpg)](https://www.youtube.com/watch?v=eyyUXmFxxP0)

## 📂 Data Notes
- `sample_shipments.csv`: Used to evaluate bypass eligibility
- `service_centers.csv`: Defines all available SCs with trailer availability
- `sample_data.csv`: Training data for the ML model

---

## 📌 Future Ideas
- Real-time trailer optimization and capacity charts
- Map visualizations of routes
- Dynamic learning from user-submitted shipments

---
