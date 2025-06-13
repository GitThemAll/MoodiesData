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

## How to run:
prerequisite:
Make sure you have the raw data in the `resources/data/raw` folder so that it can be processed by the app

### On your machine:
#### run the backend:
run `python -m flask -m run`
#### run the front-end
go to the ui directory: run `cd interfaces/ui/mu-ui/Dockerfile`
donwload npm packages: run `npm ci` 
build: run `npm run build`

### on docker locally:
simply run `docker compose up --build`

-----------
However you ran the app, you can access it on localhost:3000
Accessing the api directly can also be done localhost:5004