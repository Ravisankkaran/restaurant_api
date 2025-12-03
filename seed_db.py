# seed_db.py
from app import create_app
from models import db, MenuItem, Order, OrderItem, Payment

app = create_app()
app.app_context().push()

# Drop and recreate for a fresh seed
db.drop_all()
db.create_all()

# --- Menu (from PDF) ---
menu_rows = [
    # id, name, cat_id, menu_id, sizes, prices
    (1,"Item1",1,1,"Small,Large","1.50,2.50"),
    (2,"Item2",1,1,"","3"),
    (3,"Item3",2,2,"","2.5"),
    (4,"Item4",2,2,"","1.5"),
    (5,"Item5",2,1,"","1"),
    (6,"Item6",3,1,"Small,Large","2.50,3.6"),
    (7,"Item7",3,1,"","2.5"),
    (8,"Item8",4,2,"Small,Large","3.75,6.5"),
    (9,"Item9",4,2,"","1.5"),
    (10,"Item10",5,2,"","2"),
]

for r in menu_rows:
    mi = MenuItem(id=r[0], name=r[1], cat_id=r[2], menu_id=r[3], sizes=r[4], prices=r[5])
    db.session.add(mi)
db.session.commit()

# --- Orders History (we will group by Order ID) ---
# PDF rows (sample): we'll map order_id -> multiple items
order_items_rows = [
    # (order_date, order_id, item_id, size, price, qty, status, total_line)
    ("01 Oct 2025", 10, 2, None, 2.5, 1, "Completed", 2.5),
    ("01 Oct 2025", 10, 3, None, 1.5, 2, "Completed", 3.0),
    ("01 Oct 2025", 10, 1, "Small", 3.75, 1, "Completed", 3.75),
    # ... continue inserting a representative subset from the PDF, you can expand as needed
    ("01 Oct 2025", 11, 5, None, 2.75, 1, "Completed", 2.75),
    ("01 Oct 2025", 11, 6, None, 1.75, 2, "Completed", 3.5),
    ("01 Oct 2025", 11, 2, None, 2.5, 1, "Completed", 2.5),
    ("01 Oct 2025", 11, 3, None, 3.5, 1, "Completed", 3.5),
    ("01 Oct 2025", 11, 4, None, 3.75, 2, "Completed", 7.5),
    ("01 Oct 2025", 11, 5, None, 1.5, 1, "Completed", 1.5),
    # 12
    ("01 Oct 2025", 12, 6, "Large", 5.5, 2, "Completed", 11.0),
    ("01 Oct 2025", 12, 7, None, 2.5, 1, "Completed", 2.5),
    ("01 Oct 2025", 12, 1, "Large", 3.5, 1, "Completed", 3.5),
    # 13
    ("01 Oct 2025", 13, 1, "Small", 2.75, 2, "Completed", 5.5),
    ("01 Oct 2025", 13, 6, "Small", 1.5, 1, "Completed", 1.5),
    ("01 Oct 2025", 13, 8, "Small", 3.5, 1, "Completed", 3.5),
    ("01 Oct 2025", 13, 1, "Small", 2.5, 2, "Completed", 5.0),
    # ... add more rows as in the PDF if you want
]

# We'll create an Order row per unique order_id and attach items
orders = {}
for od in order_items_rows:
    order_date, order_id, item_id, size, price, qty, status, line_total = od
    if order_id not in orders:
        # create Order entry (we'll compute total after adding items)
        o = Order(order_id=order_id, order_date=order_date, order_status=status, total=0.0)
        db.session.add(o)
        db.session.flush()  # get o.id
        orders[order_id] = o
    else:
        o = orders[order_id]
    oi = OrderItem(order_id=o.id, item_id=item_id, size=size, price=price, qty=qty, line_total=line_total)
    db.session.add(oi)
    o.total = (o.total or 0.0) + float(line_total)

db.session.commit()

# --- Payments (use PDF sample) ---
# Each payment row: (payment_id, payment_date, payment_id_field, order_id, amount, due, tips, discount, total_paid, type, status)
payments_rows = [
    ("01 Oct 2025", 100, 10, 9.25, 0, 0, 9.25, "Card", "Completed"),
    ("01 Oct 2025", 101, 11, 21.25, 0, 0, 10.00, "Cash", "Completed"),
    ("01 Oct 2025", 102, 11, 21.25, 0, 0, 11.25, "Card", "Completed"),
    ("02 Oct 2025", 103, 12, 17.00, 3.0, 4.0, 16.0, "Card", "Completed"),
    ("03 Oct 2025", 104, 13, 15.5, 0, 2.0, 13.5, "Card", "Completed"),
    ("01 Oct 2025", 105, 14, 42.8193, 0, 0, 20.0, "Cash", "Completed"),
    ("01 Oct 2025", 106, 14, 42.8193, 0, 0, 22.82, "Card", "Completed"),
    ("02 Oct 2025", 107, 15, 5.136, 0, 0, 5.14, "Card", "Refunded"),
    ("03 Oct 2025", 108, 16, 19.758, 0, 0, 10.0, "Cash", "Completed"),
    ("03 Oct 2025", 109, 16, 19.758, 0, 0, 9.76, "Card", "Completed"),
    ("01 Oct 2025", 110, 17, 10.8918, 0, 0, 10.9, "Card", "Completed"),
    ("05 Oct 2025", 111, 18, 26.33588, 2, 0, 25.0, "Cash", "Completed"),
    ("05 Oct 2025", 115, 18, 26.33588, 0, 0, 3.34, "Card", "Completed"),
    ("01 Oct 2025", 116, 19, 72.13188, 0, 0, 50.0, "Cash", "Completed"),
    ("01 Oct 2025", 119, 19, 72.13188, 0, 0, 22.13, "Card", "Completed"),
    ("01 Oct 2025", 120, 20, 52.2573, 0, 0, 25.0, "Cash", "Completed"),
    ("01 Oct 2025", 121, 20, 52.2573, 0, 0, 27.28, "Card", "Completed"),
]

# attach payments to orders: find order DB row by order_id from orders dict
for p in payments_rows:
    payment_date, payment_id_field, order_id_field, amount, due, tips, total_paid, ptype, pstatus = p
    # find Order object by business order_id:
    order_obj = None
    for od_obj in orders.values():
        if od_obj.order_id == order_id_field:
            order_obj = od_obj
            break
    if order_obj:
        pay = Payment(payment_id=payment_id_field, order_id=order_obj.id, amount=amount, due=due,
                      tips=tips, discount=0.0, total_paid=total_paid, payment_type=ptype, payment_status=pstatus,
                      payment_date=payment_date)
        db.session.add(pay)
db.session.commit()

print("DB seeded.")
