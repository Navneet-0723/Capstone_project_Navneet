# Mamaearth Returns & Growth Intelligence Capstone Project
*For MASAI project*

This repository contains the complete end-to-end data engineering, SQL analytics, Pandas data wrangling/EDA pipeline, visualization suite, and automated Gemini AI narrator module (with a robust offline fallback) for the Mamaearth Returns & Growth Intelligence capstone.

---

## Prerequisites & Setup
* **Python 3.8+** installed with required libraries (see `requirements.txt`).
* **MySQL Database** managed via VS Code (SQLTools) or local MySQL CLI.

---

## Reproduction Guide (Top-to-Bottom)

### 1. Database Setup & Analytical Queries (Part 1)
To set up the relational database and execute the core business report queries:
1. Load and execute the schema script to create tables (`customers`, `products`, `orders`):
   ```sql
   SOURCE sql/schema.sql;
SOURCE sql/seed_data.sql;
SOURCE sql/report.sql;
python analysis/clean_and_eda.py
python analysis/visualize.py

python narrator/generate_narrative.py
$env:GEMINI_API_KEY="your_actual_api_key_here"
python narrator/generate_narrative.py

export GEMINI_API_KEY="your_actual_api_key_here"
python narrator/generate_narrative.py
