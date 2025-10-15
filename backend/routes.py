from flask import Blueprint, jsonify


bp = Blueprint("api", __name__)


# ========================================
# Health Check Endpoint
# ========================================
@bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# ========================================
# Borrowers Endpoints
# ========================================





# ========================================
# Applications Endpoints
# ========================================