# Moodies Undies - Fullstack Data Science Platform

## Project Overview

This project is developed for **Moodies Undies** as part of the AI & Data Science minor.  
It includes:

- A backend Flask API for serving machine learning models and customer analytics
- A React/Next.js frontend interface for interacting with customer segmentation, lifetime value (CLV), product metrics, and dashboards
- A fully containerized Docker setup for easy deployment and reproducibility

The system enables Moodies Undies to analyze customer behavior, predict purchasing patterns, and support data-driven decision making.

---

## ⚙️ Tech Stack

| Layer | Technology |
| ----- | ----------- |
| Backend | Python 3.12, Flask, SQLAlchemy, SQLite |
| Machine Learning | DBSCAN, LightGBM, Random Forest, XGBoost |
| Frontend | React, Next.js 15 (App Router), TypeScript |
| Containerization | Docker, Docker Compose |
| Visualization | Recharts, ResponsiveContainer |
| Data Management | SQLite (resources/data/mydatabase.db) |

---

## 📂 Project Structure

```bash
/project-root
  /backend
    app.py
    requirements.txt
    resources/data/mydatabase.db
  /interfaces/ui/mu-ui
    package.json
    next.config.js
  docker-compose.yml
  .env
