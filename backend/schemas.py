from app import ma
from models import Borrower, Application
from marshmallow import fields


# ========================================
# Borrowers Schemas
# ========================================

# Validate Incoming POST data 
class BorrowerRequestSchema(ma.Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    address_1 = fields.String(required=True)
    address_2 = fields.String()
    city = fields.String(required=True)
    state = fields.String(required=True)
    zip_code = fields.String(required=True)
    email = fields.Email(required=True)
    phone = fields.String()
    ssn = fields.String(required=True) # Mask/encrypt at later date for production app


# Serialize Outgoing Response data
class BorrowerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Borrower
        load_instance = True
        exclude = ("ssn",)  # Exclude SSN from response for security