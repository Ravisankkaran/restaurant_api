# app.py
from flask import Flask, jsonify, request, abort
from config import Config
from models import db, MenuItem, Order, OrderItem, Payment
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from math import isclose

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # simple rate limiter to protect from abuse
    limiter = Limiter(key_func=get_remote_address, app=app, default_limits=["200 per hour"])

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status":"ok"}), 200

    @app.route("/orders", methods=["GET"])
    @limiter.limit("60/minute")
    def list_orders():
        """
        Returns: list of orders with basic details and payment summary.
        Query params:
          - page (int) optional
          - per_page (int) optional
        """
        # simple pagination
        try:
            page = int(request.args.get("page", 1))
            per_page = min(int(request.args.get("per_page", 20)), 100)
        except:
            page = 1; per_page = 20

        q = Order.query.order_by(Order.order_date, Order.order_id)
        pag = q.paginate(page=page, per_page=per_page, error_out=False)

        out = []
        for order in pag.items:
            payments = [{
                "payment_id": p.payment_id,
                "total_paid": round(p.total_paid, 2),
                "payment_type": p.payment_type,
                "payment_status": p.payment_status,
                "payment_date": p.payment_date
            } for p in order.payments]

            out.append({
                "order_id": order.order_id,
                "order_date": order.order_date,
                "order_status": order.order_status,
                "total": round(order.total if order.total else 0.0, 2),
                "payments": payments,
                "total_transactions": len(order.items)  # number of line items
            })

        return jsonify({
            "page": page,
            "per_page": per_page,
            "total_orders": pag.total,
            "orders": out
        }), 200

    @app.route("/orders/<int:order_id>", methods=["GET"])
    @limiter.limit("60/minute")
    def get_order(order_id):
        """
        Returns full order details: items with sizes/prices/qty, and payments.
        We lookup by business order_id (the order_id column), not the internal PK.
        """
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            return jsonify({"error":"Order not found"}), 404

        items = []
        for oi in order.items:
            items.append({
                "item_id": oi.item_id,
                "size": oi.size,
                "price": round(oi.price, 2),
                "qty": oi.qty,
                "line_total": round(oi.line_total, 2)
            })

        payments = []
        for p in order.payments:
            payments.append({
                "payment_id": p.payment_id,
                "amount": round(p.amount, 2),
                "due": round(p.due, 2) if p.due is not None else 0.0,
                "tips": round(p.tips, 2) if p.tips is not None else 0.0,
                "discount": round(p.discount, 2) if p.discount is not None else 0.0,
                "total_paid": round(p.total_paid, 2),
                "payment_type": p.payment_type,
                "payment_status": p.payment_status,
                "payment_date": p.payment_date
            })

        response = {
            "order_id": order.order_id,
            "order_date": order.order_date,
            "status": order.order_status,
            "total": round(order.total if order.total else 0.0, 2),
            "items": items,
            "payments": payments
        }
        return jsonify(response), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
