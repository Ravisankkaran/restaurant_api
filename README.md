README.md
Restaurant Orders & Payments API

This project is a simple backend application built using Flask, SQLAlchemy, and SQLite.
It provides APIs to view restaurant orders, their items, and payment details.
The data is taken from the sample dataset provided in the assignment.

Tech Stack
-Python 3
-Flask
-Flask SQLAlchemy
-SQLite
-Postman (for testing)

Project Setup
1. Create Virtual Environment
python -m venv venv

2. Activate Environment
Windows -venv\Scripts\activate

3. Install Requirements
pip install -r requirements.txt

Database Setup
Run the seeding script

This will create the database and insert all the sample menu, order, and payment data.

python seed_db.py


If you see:

DB seeded.


It means your database was created successfully.

Run the Application

Start the server using:

python app.py


Server runs at:

http://localhost:5000

API Endpoints
1. Health Check
GET /health


Used to check if the server is running.

2. List Orders
GET /orders


You can also use:

GET /orders?page=1&per_page=20


Returns:
-Order ID
-Order date
-Order status
-Total amount
-Number of items in the order
-Payment summary

3. Get Order by ID
GET /orders/<order_id>


Example:

GET /orders/11


Returns full details:
-Order items
-Item price, size, quantity
-Line totals
-All payments for that order


How AI Was Used (Required in Assignment)

I used ChatGPT mainly for guidance in:

    -Understanding Flask relationships

    -Fixing errors during setup

    -Generating sample seed data from the assignment table

    -All the coding, debugging, and testing were done by me manually.


