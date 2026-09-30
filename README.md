# 🌧️ MonSense — Hyperlocal Monsoon Prediction & Crop Advisory Platform

> **Smart India Hackathon 2026 | Problem Statement ID: 26086**
> **Team: APPEX ALLIANCE**

## 🎯 Problem
Farmers often sow crops based on early rains (false-onset) or face unexpected dry spells and heavy rainfall, leading to crop loss and income instability.

## 💡 Solution
MonSense provides **block/village-level monsoon prediction and crop advisories** to help farmers make the right decisions at the right time.

### Key Features
1. **7-30 Day Outlook** — Advance warning of monsoon onset, dry spells and heavy rain
2. **Block/Village Risk Maps** — Color-coded probability maps down to Panchayat level
3. **Crop-Specific Advisory** — Clear advice: delay sowing, arrange irrigation, change crop
4. **Regional Language Alerts** — Delivered via mobile app, SMS and WhatsApp in local language

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Data Sources** | IMD, NCMRWF, NASA GPM-IMERG, ECMWF ERA5, ENSO/IOD/MJO Indices |
| **ML Models** | TensorFlow/Keras (LSTM), XGBoost (Downscaling) |
| **Backend** | Python, FastAPI, Uvicorn |
| **Frontend** | React.js, Leaflet.js, Vite |
| **Database** | PostgreSQL + PostGIS, Redis |
| **Alerts** | Twilio (SMS), GupShup (WhatsApp) |
| **Deployment** | Docker, AWS/Google Cloud Run |

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ with PostGIS
- Redis 7+
- Docker & Docker Compose (optional)

### Using Docker (Recommended)
```bash
docker-compose up --build
```

### Manual Setup

#### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Access
- **Frontend Dashboard**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📁 Project Structure
```
monsense/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration management
│   │   ├── database.py          # Database connection
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── routers/             # API route handlers
│   │   ├── services/            # Business logic
│   │   ├── ml/                  # ML model pipeline
│   │   └── utils/               # Utilities
│   ├── tests/                   # Test suites
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API service layer
│   │   ├── hooks/               # Custom hooks
│   │   └── assets/              # Static assets
│   ├── package.json
│   └── Dockerfile
├── ml/
│   ├── models/                  # Trained model weights
│   ├── notebooks/               # Training notebooks
│   └── data/                    # Sample datasets
├── docker-compose.yml
└── README.md
```

## 🌍 Impact
- **Farmers**: Timely sowing decisions, alerts for dry spells and heavy rainfall
- **Extension Officers**: Block/village level risk maps, data-driven advisories
- **Government/NCMRWF**: Better monsoon monitoring, disaster preparedness
- **Environment**: Optimized water/fertilizer use, sustainable agriculture

## 📜 License
MIT License — Open source for public good

## 🙏 Data Attribution
- India Meteorological Department (IMD)
- National Centre for Medium Range Weather Forecasting (NCMRWF)
- European Centre for Medium-Range Weather Forecasts (ECMWF) ERA5
- NASA Global Precipitation Measurement (GPM) IMERG
