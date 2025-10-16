import random
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from extensions import db
from models import Borrower, Application
from schemas import BorrowerRequestSchema, BorrowerSchema, ApplicationRequestSchema, ApplicationResponseSchema
from utils import get_or_create_borrower, get_loan_offer

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
    """Create a new borrower."""
    req_schema = BorrowerRequestSchema()
    res_schema = BorrowerSchema()

    # Load Request
    try:
        data = req_schema.load(request.get_json())
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

    except (IntegrityError, SQLAlchemyError) as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    
    return res_schema.jsonify(new_borrower), 201


# ========================================
# Applications Endpoints
# ========================================

@bp.route("/applications", methods=["POST"])
def create_application():
    """Create a new loan application."""
    req_schema = ApplicationRequestSchema()
    res_schema = ApplicationResponseSchema()
    
    # Load and Validate Request
    try:
        data = req_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    # Check if borrower exists by SSN
    borrower_data = data.pop("borrower")

    result = get_or_create_borrower(borrower_data)
    borrower_info = result['borrower']
    errors = result['errors']
    
    if errors :
        return jsonify({"errors": errors}), 400
    
    
    # At this point we have a borrower (new or existing)
    # Determine open lines of credit for borrower
    open_credit_lines = random.randint(0, 100)

    # Determine loan offer
    loan_offer = get_loan_offer(data['requested_amount'], open_credit_lines)

    try:
        new_application = Application(
            borrower_id=borrower_info['borrower_id'],
            requested_amount=data['requested_amount'],
            open_credit_lines=open_credit_lines,
            approved_amount=loan_offer['approved_amount'],
            interest_rate=loan_offer['interest_rate'],
            term_months=loan_offer['term_months'],
            monthly_payment=loan_offer['monthly_payment'],
            status=loan_offer['status'],
            reason=loan_offer['reason']
        )
        db.session.add(new_application)
        db.session.commit()

    except (IntegrityError, SQLAlchemyError) as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

    return res_schema.jsonify(new_application), 201


        
        