# 🌱 EcoMetrics Corporate Carbon Footprint Platform

A full-stack sustainability metrics platform built to track direct **Scope 1 (Direct Fuel)** and indirect **Scope 2 (Electricity)** corporate greenhouse gas emissions. The system calculates impact matrices automatically and generates real-time green engineering action plans via the **Google Gemini API**.

## 🛠️ Infrastructure Stack
* **Backend Framework:** Python Flask
* **Database Management:** MySQL Relational Database
* **Styling Rules:** Pure CSS3 Architecture
* **Artificial Intelligence Engine:** Google GenAI Client (Gemini 3.8 Flash)

## 📊 Environmental Math Formulas Applied
The engine references institutional conversion baselines (EPA eGRID / DEFRA standards) to convert consumption volumes into Metric Tons of CO₂ equivalent (MTCO₂e):
* **Electricity:** `Usage (kWh) × 0.00037 = MTCO₂e`
* **Natural Gas:** `Usage (therms) × 0.00530 = MTCO₂e`
* **Fleet Fuels:** `Usage (gallons) × 0.00890 = MTCO₂e`

## 🚀 Local Deployment Instructions
1. Clone this repository structure.
2. Spin up your local database using the schema tables inside `eco.sql`.
3. Configure your local system environment credentials:
   ```bash
   \$env:GEMINI_API_KEY="your_api_key_here"
   ```
4. Fire up the local platform runtime server:
   ```bash
   python app.py
   ```
