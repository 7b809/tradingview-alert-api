from flask import Blueprint, jsonify, redirect, url_for
from db import alerts_collection

alerts_bp = Blueprint("alerts", __name__)

PAGE_SIZE = 25


# ==============================
# REDIRECT: /alerts → /alerts/1
# ==============================
@alerts_bp.route("/", methods=["GET"])
def alerts_root():
    return redirect(url_for("alerts.get_alerts", page=1))


# ==============================
# GET PAGINATED ALERTS
# ==============================
@alerts_bp.route("/<int:page>", methods=["GET"])
def get_alerts(page):
    if page < 1:
        return jsonify({"error": "Invalid page"}), 400

    skip = (page - 1) * PAGE_SIZE

    total = alerts_collection.count_documents({})
    alerts_cursor = alerts_collection.find() \
        .sort("timestamp", -1) \
        .skip(skip) \
        .limit(PAGE_SIZE)

    alerts = []
    for doc in alerts_cursor:
        doc["_id"] = str(doc["_id"])
        alerts.append(doc)

    total_pages = (total + PAGE_SIZE - 1) // PAGE_SIZE

    return jsonify({
        "page": page,
        "page_size": PAGE_SIZE,
        "total_records": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
        "data": alerts
    })