# Fullstack Developer Assessment - Python API  

**By: Ravisankkaran I**

## Restaurant Orders & Payments API

This project is a simple backend application built using **Flask**, **SQLAlchemy**, and **SQLite**.  
It provides APIs to view restaurant orders, their items, and payment details.  
All data is taken from the sample dataset provided in the assignment.

---

## Tech Stack
- Python 3  
- Flask  
- Flask SQLAlchemy  
- SQLite  
- Postman (for testing)

---

## Project Setup

### 1. Create Virtual Environment
python -m venv venv

### 2. Activate Environment  
Windows:
venv\Scripts\activate

### 3. Install Requirements
pip install -r requirements.txt

---

##  Database Setup

Run the seeding script to create the database and insert sample data:

python seed_db.py

If you see:

DB seeded.

Then your database was created successfully.

---

##  Run the Application

Start the Flask server:

python app.py

Server will run at:

http://localhost:5000

---

## API Endpoints

### 1. Health Check  
GET /health  
Checks if the server is active.

---

### 2. List Orders  
GET /orders

Supports pagination:  
GET /orders?page=1&per_page=20

Returns:
- Order ID  
- Order date  
- Order status  
- Total amount  
- Number of items  
- Payment summary  

---

### 3. Get Order by ID  
GET /orders/<order_id>

Example:  
GET /orders/11

Returns full order details:
- Order items  
- Item price, size, quantity  
- Line totals  
- All payments for the order  

---

## How AI Was Used (Required in Assignment)

I used ChatGPT mainly for guidance in:
- Understanding Flask relationships  
- Fixing errors during setup  
- Generating sample seed data from the assignment table  

**All coding, debugging, and testing were done manually by me.**

---

## Contact Details

**Ravisankkaran I**  
Email: ravisankkaran@gmail.com  
Phone: +91 7395978321
