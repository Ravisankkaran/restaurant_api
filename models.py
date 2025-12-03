from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class MenuItem(db.Model):
    __tablename__ = "menu_items"
    id = db.Column(db.Integer, primary_key=True)        # Item ID
    name = db.Column(db.String(128), nullable=False)
    cat_id = db.Column(db.Integer, nullable=True)
    menu_id = db.Column(db.Integer, nullable=True)
    # store sizes & prices as JSON-like text for simplicity; can normalize further
    sizes = db.Column(db.String(256), nullable=True)   # e.g. "Small,Large"
    prices = db.Column(db.String(256), nullable=True)  # e.g. "1.50,2.50"

    def __repr__(self): return f"<MenuItem {self.id} {self.name}>"

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)         # internal PK
    order_id = db.Column(db.Integer, nullable=False, index=True)  # business order id (as in PDF)
    order_date = db.Column(db.String(64))                # keep as string for sample data (or use Date)
    order_status = db.Column(db.String(64))
    total = db.Column(db.Float)

    items = db.relationship("OrderItem", backref="order", cascade="all,delete-orphan")
    payments = db.relationship("Payment", backref="order", cascade="all,delete-orphan")

    def __repr__(self): return f"<Order {self.order_id}>"

class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(64), nullable=True)
    price = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    line_total = db.Column(db.Float, nullable=False)

    def __repr__(self): return f"<OrderItem order:{self.order_id} item:{self.item_id}>"

class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, nullable=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due = db.Column(db.Float, nullable=True)
    tips = db.Column(db.Float, nullable=True)
    discount = db.Column(db.Float, nullable=True)
    total_paid = db.Column(db.Float, nullable=False)
    payment_type = db.Column(db.String(32), nullable=True)
    payment_status = db.Column(db.String(32), nullable=True)
    payment_date = db.Column(db.String(64), nullable=True)

    def __repr__(self): return f"<Payment {self.payment_id} for order {self.order_id}>"
