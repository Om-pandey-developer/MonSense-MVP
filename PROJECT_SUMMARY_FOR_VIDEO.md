# 🌧️ MonSense — Project Summary & Video Image Generation Guide

> **Smart India Hackathon 2026 | Problem Statement ID: 26086**  
> **Team:** APPEX ALLIANCE  
> **Platform:** MonSense — Hyperlocal Monsoon Prediction & Crop Advisory Platform  

---

## 📌 Executive Summary

**MonSense** is an AI-powered agricultural intelligence platform designed to protect Indian farmers from climate volatility. Traditional weather forecasts operate on coarse 25–50 km grids, failing to predict localized dry spells or heavy rainfall bursts that cause false-onset sowing and catastrophic crop loss. 

MonSense bridges this gap by delivering **block/village-level (4 km mesh) 7–30 day monsoon predictions**, **crop-specific phenological advisories**, and **multilingual emergency alerts** delivered straight to farmers via SMS and WhatsApp.

---

## 🚀 What Has Been Built So Far

### 1. 🖥️ Interactive Web Dashboard & GIS System (Frontend)
- **Operational Dashboard (`App.jsx`):** 
  - Real-time command center displaying key operational metrics: Monitored Blocks, High-Risk Alerts, Active Forecasts, Crop Advisories, Dispatched Alerts, and Registered Farmers.
  - Live Monsoon Status indicator (Active / Break / Withdrawal) and global teleconnection index tracking (ENSO Niño 3.4, IOD DMI, MJO).
- **GIS Risk Probability Heatmap (`RiskMap.jsx`):**
  - High-resolution interactive Leaflet map featuring color-coded risk layers (Low, Moderate, High, Severe).
  - Spatial block selection and district polygon bounds highlighting.
- **7 to 30-Day Rainfall Forecast Studio (`ForecastChart.jsx`):**
  - Dual-curve visualization showing projected rainfall (mm) alongside confidence interval uncertainty cones (widening over lead times).
  - Risk probability bars showing inversely correlated heavy rainfall vs. dry spell probabilities.
- **Crop-Specific Advisory Engine (`AdvisoryPanel.jsx`):**
  - Actionable recommendations categorized by urgency (`Urgent`, `Warning`, `Advisory`, `Favorable`).
  - Advice tailored to specific crops (Soybean, Cotton, Rice, Wheat, Sugarcane, Maize, Groundnut, Pulses) and growth stages (Pre-sowing, Sowing, Vegetative, Flowering, Maturity, Harvest).
- **Interactive Scenario Simulator (`ScenarioSimulator.jsx`):**
  - A "What-If" sandbox where agricultural officers can slide rainfall (0–200 mm) and dry spell duration (0–14 days) to immediately inspect simulated crop responses and risk mitigations.
- **Visual Mobile Alert Simulator (`AlertSimulator.jsx`):**
  - Realistic smartphone bezel mockup with tabbed WhatsApp & SMS delivery views.
  - Native multilingual messaging in **Marathi (मराठी)**, **Hindi (हिन्दी)**, and **English**.
  - Animated rural telecom gateway terminal showing packet routing and live farmer delivery status tracking.
- **Pan-India Cascading Location Bar:**
  - Full hierarchical selector covering all **30 States & Union Territories**, cascading to districts and blocks.
- **Dual Data Mode (Live vs. Demo Engine):**
  - Real-time switch connecting to the **Open-Meteo ECMWF/GFS live atmospheric API** with live telemetry telemetry HUD (Max Temp, Today's Rain, Volumetric Soil Moisture, API Latency) or offline calibrated hackathon demo data.

---

### 2. 🧠 Machine Learning & Climatological Engine (Backend)
- **Hybrid AI Architecture:**
  - **LSTM Temporal Sequence Model:** Learns historical rainfall sequences, seasonal active-break cycles, and macro-climate drivers (El Niño/La Niña, Indian Ocean Dipole, Madden-Julian Oscillation).
  - **XGBoost Spatial Downscaler:** Refines coarse atmospheric forecasts down to village/block level using micro-topographic features (elevation, slope aspect, terrain roughness, land use).
- **Rule-Based Phenological Agronomic Heuristics:**
  - Calibrated rules for critical farming operations: delaying sowing during false onset, opening drainage channels prior to waterlogging bursts, and halting pesticide spraying before heavy precipitation.

---

### 3. ⚙️ Backend Infrastructure & APIs (FastAPI)
- **Modular REST API Routers:**
  - `/forecast`: Endpoints for single-location forecasts, time-series horizons (7–30 days), GIS risk polygons, and live Open-Meteo telemetry fetching.
  - `/advisory`: Dynamic advisory generator based on phenological crop stages and precipitation thresholds.
  - `/alerts`: Broadcast triggering, farmer registry management, and delivery statistics.
  - `/dashboard`: Consolidated status metrics and teleconnection indices.
  - `/locations`: Pan-India spatial metadata and district coordinates.
- **Telecom & Messaging Service:**
  - Twilio (SMS) and GupShup (WhatsApp) integration layer with automatic retry queues and multi-channel fallback.

---

## 🎨 Prompts for Gemini: Generating 2 Images for Video Creation

Use the two prompts below in Gemini to generate complementary visual assets for the presentation or video intro:

---

### 🖼️ Image Prompt 1: The Ground Reality & Farmer Impact
> **Prompt:**  
> A cinematic, high-resolution realistic photograph of an Indian farmer standing in a lush green agricultural field with rows of soybean and cotton crops under a dramatic monsoon sky with passing rain clouds. The farmer is holding a smartphone that displays a clean, glowing green weather notification with the MonSense logo and Marathi/Hindi text saying "Safe to Sow — Rain Predicted". In the background, subtle holographic data visualizations of weather radar rings and raindrop probability graphs gently float in the atmosphere, symbolizing AI climate intelligence empowering rural agriculture. Golden hour soft lighting, 8k resolution, photorealistic, uplifting and hopeful atmosphere.

---

### 🖼️ Image Prompt 2: The High-Tech AI Command & Prediction Dashboard
> **Prompt:**  
> A sleek, state-of-the-art modern agricultural command center and dashboard interface titled "MonSense — Hyperlocal Monsoon AI". The main screen showcases a 3D topographic GIS heatmap of India with glowing color-coded risk zones (emerald green, amber yellow, and crimson red) down to the village level. Adjacent panels show an advanced 30-day LSTM rainfall forecast chart with glowing confidence cones, teleconnection gauges for El Niño and Indian Ocean Dipole, and an interactive smartphone alert preview broadcasting multilingual emergency warnings. Ultra-modern dark-mode glassmorphism UI design, vibrant cyan and emerald accents, crisp typography, clean futuristic aesthetic, 8k render.

---

## 📊 Summary Table of Key Highlights

| Component | Status | Highlights |
| :--- | :--- | :--- |
| **Geographic Scope** | Complete | Pan-India coverage (30 States & Union Territories, down to blocks) |
| **Prediction Horizon** | Complete | 7 to 30-day probabilistic forecasts with uncertainty intervals |
| **GIS Mapping** | Complete | 4km resolution choropleth risk map with interactive block inspection |
| **Crop Intelligence** | Complete | 8 major crops across 6 growth stages with "What-If" simulator |
| **Disaster Alerts** | Complete | Multilingual (Marathi, Hindi, English) WhatsApp & SMS emulator |
| **Live Satellite Link** | Complete | Live Open-Meteo ECMWF telemetry feed + offline demo fallback |
