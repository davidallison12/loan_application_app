from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models import db, Borrower, Application
from schemas import BorrowerRequestSchema, BorrowerSchema


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

@bp.route("/borrowers", methods=["POST"])
def create_borrower():
    req_schema = BorrowerRequestSchema()
    res_schema = BorrowerSchema()

    try:
        data = req_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    # Check for existing SSN
    existing_borrower = Borrower.query.filter_by(ssn=data['ssn']).first()
    if existing_borrower:
        return jsonify({"error": "Borrower with this SSN already exists."}), 409 # Conflict Status Code
    
    # Create new borrower
    try:
        new_borrower = Borrower(**data)
        db.session.add(new_borrower)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error: Please check for duplicates or missing requered fields."}), 400

    except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": "Unexpected database error occurred.", "details": str(e)}), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":"Unexpected server error", "details": str(e)}), 500
    
    return res_schema.jsonify(new_borrower), 201

# ========================================
# Applications Endpoints
# ========================================