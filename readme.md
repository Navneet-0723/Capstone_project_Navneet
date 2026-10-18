# Mamaearth Returns & Growth Intelligence Capstone Project
*For MASAI Capstone Submission*

This repository contains the complete end-to-end data engineering, SQL analytics, Pandas data wrangling/EDA pipeline, visualization suite, and automated Gemini AI narrator module (with a robust offline fallback) for the Mamaearth Returns & Growth Intelligence capstone project.

---

## Prerequisites & Setup
* **Python 3.8+** installed with required libraries (see `requirements.txt`).
* **SQLite / MySQL Database** managed via VS Code or CLI.

---

## Reproduction Guide (Top-to-Bottom)

### 1. Database Setup & Analytical Queries (Part 1)
To set up the relational database and execute the core business report queries:
1. Load and execute the schema script to create tables (`customers`, `products`, `orders`):
   ```sql
   SOURCE sql/schema.sql;
   ```
2. Seed the database with the provided initial data:
   ```sql
   SOURCE sql/seed_data.sql;
   ```
3. Run the analytical report queries to generate baseline figures:
   ```sql
   SOURCE sql/report.sql;
   ```

### 2. Data Cleaning, EDA & Visualizations (Part 2)
To execute the Python data pipeline and generate the required charts:
1. Run the cleaning, deduplication, imputation, IQR outlier detection, and statistical analysis script:
   ```bash
   python analysis/clean_and_eda.py
   ```
   *Note: Running this automatically generates and updates `narrator/findings.json`.*
2. Run the visualization script to generate and save charts into the `visualizations/` folder:
   ```bash
   python analysis/visualize.py
   ```

### 3. Automated Gemini AI Narrator & Offline Fallback (Part 3)
To generate the Situation-Complication-Resolution (SCR) business report narrative and validate numeric accuracy:

* **Option A: Running with No API Key (Offline Fallback Path)**
  If no API key is provided, the script automatically triggers the keyless offline fallback mode:
  ```bash
  python narrator/generate_narrative.py
  ```

* **Option B: Running with a Live Gemini API Key**
  To use the live Gemini API model with locked parameters, set your API key as an environment variable or store it locally in `API.txt`:
  * **Windows (PowerShell):**
    ```powershell
    $env:GEMINI_API_KEY="your_actual_api_key_here"
    python narrator/generate_narrative.py
    ```
  * **Mac / Linux / Bash:**
    ```bash
    export GEMINI_API_KEY="your_actual_api_key_here"
    python narrator/generate_narrative.py
    ```

---

## Repository Structure
```text
.
├── README.md
├── requirements.txt
├── sql/
│   ├── schema.sql
│   ├── seed_data.sql
│   └── report.sql
├── data/
│   ├── customer.csv
│   ├── order.csv
│   └── product.csv
├── analysis/
│   ├── clean_and_eda.py
│   └── visualize.py
├── visualizations/
│   ├── return_rate_by_payment.png
│   └── monthly_revenue_trend.png
└── narrator/
    ├── findings.json
    ├── generate_narrative.py
    └── sample_output.txt
```