# Capstone_project_Navneet
For MASAI project
# Mamaearth Returns & Growth Intelligence Capstone Project

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
