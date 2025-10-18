from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from extensions import db
from models import Borrower
from schemas import BorrowerSchema


def get_or_create_borrower(borrower_data):
    """
    Retrieve a borrower by SSN or create a new one if not found.
    param:
        - borrower_data: dict - borrower details including 'ssn'

    Returns:
        dict:
            {
                "borrower": dict,       # serialized borrower data
                "errors": dict or None, # errors if any
                "created": bool         # True if newly created, False if existing
            }
    """
    borrower = Borrower.query.filter_by(ssn=borrower_data["ssn"]).first()
    borrower_schema = BorrowerSchema()

    if borrower:
        # Borrower exists, return it with Borrower Exists Error
        return {
            "borrower": borrower_schema.dump(borrower),
            "errors": None,  # Borrower exists, return it with False indicating not created
            "created": False,
        }

    # Create new borrower
    try:
        new_borrower = Borrower(**borrower_data)
        db.session.add(new_borrower)
        db.session.commit()

        # Returning new barrower data with no errors
        return {
            "borrower": borrower_schema.dump(new_borrower),
            "errors": None,
            "created": True,
        }

        # Returning NO barrower data with errors
    except (IntegrityError, SQLAlchemyError) as e:
        db.session.rollback()
        return {"borrower": None, "errors": {"database": [str(e)]}, "created": False}


def get_loan_offer(requested_amount, open_credit_lines):
    """
    Determine loan offer based on requested amount and open credit lines.
    param:
        - requested_amount: float - Amount requested by borrower
        - open_credit_lines: int  - Number of open credit lines the borrower has
    Conditions:
    - Requested amount outside $10,000-$50,000 = Denied
    - Credit lines of <10 = 36-month term + 10% interest
    - Credit lines of <=50 and >=10 = 24-month term + 20% interest
    - Credit lines of >50 = Denied

    Returns:
        dict:
            {
                "approved_amount": float or None,
                "interest_rate": float or None,
                "term_months": int or None,
                "monthly_payment": float or None,
                "status": str,  # 'Approved' or 'Denied'
                "reason": str or None
            }
    """
    offer = {}

    if requested_amount < 10000 or requested_amount > 50000:
        offer.update(
            {
                "status": "Denied",
                "reason": "Requested amount must be between $10,000 and $50,000.",
            }
        )

    elif open_credit_lines < 10:
        offer.update(
            {
                "status": "Approved",
                "reason": None,
                "interest_rate": 0.10,
                "term_months": 36,
            }
        )

    elif 10 <= open_credit_lines <= 50:
        offer.update(
            {
                "status": "Approved",
                "reason": None,
                "interest_rate": 0.20,
                "term_months": 24,
            }
        )
    else:
        offer["status"] = "Denied"
        offer["reason"] = "Too many open credit lines."

    if offer["status"] == "Approved":
        # If approved: Determine monthly payment using amortization formula
        term_months = offer["term_months"]
        interest_rate = offer["interest_rate"]

        monthly_rate = interest_rate / 12
        monthly_payment = requested_amount * (
            monthly_rate / (1 - (1 + monthly_rate) ** -term_months)
        )
        monthly_payment = round(monthly_payment, 2)  # Round to 2 decimal places

        offer.update(
            {"monthly_payment": monthly_payment, "approved_amount": requested_amount}
        )

    else:
        # If denied: financial fields are None
        offer.update(
            {
                "approved_amount": None,
                "interest_rate": None,
                "term_months": None,
                "monthly_payment": None,
            }
        )

    return offer
