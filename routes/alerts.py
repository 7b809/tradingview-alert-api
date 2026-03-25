from flask import Blueprint, jsonify, request
from db import alerts_collection
from utils.serializer import serialize
from config import Config

alerts_bp = Blueprint("alerts", __name__)

# redirect /alerts → /alerts/1
@alerts_bp.route("/", methods=["GET"])
def default_page():
    return get_alerts(1)


@alerts_bp.route("/<int:page>", methods=["GET"])
def get_alerts(page):
    page_size = Config.PAGE_SIZE
    skip = (page - 1) * page_size

    total = alerts_collection.count_documents({})
    cursor = alerts_collection.find().sort("timestamp", -1).skip(skip).limit(page_size)

    data = [serialize(doc) for doc in cursor]

    return jsonify({
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": (total + page_size - 1) // page_size,
        "data": data
    })