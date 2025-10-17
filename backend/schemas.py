from marshmallow import fields, validate

from extensions import ma
from models import Application, Borrower

# ========================================
# Borrower Schemas
# ========================================


# Validate Incoming POST data
class BorrowerRequestSchema(ma.Schema):
    class Meta:
        model = Borrower
        unknown = "EXCLUDE"  # Ignore unknown fields in the input data

    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    address_1 = fields.String(required=True)
    address_2 = fields.String()
    city = fields.String(required=True)
    state = fields.String(required=True)
    zip_code = fields.String(required=True)
    email = fields.Email(required=True)
    phone = fields.String()
    ssn = fields.String(
        required=True,
        validate=[
            # validate.Length(equal=11, error="SSN must be exactly 11 characters."),
            validate.Regexp(r"^\d{3}-\d{2}-\d{4}$", error="SSN must be in the format ###-##-####")
        ]
    )  # Mask/encrypt at later date for production app


# Serialize Outgoing Response data
class BorrowerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Borrower
        load_instance = True
        exclude = ("ssn",)  # Exclude SSN from response for security

    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)


# ========================================
# Application Schemas
# ========================================


# Validate Incoming POST data
class ApplicationRequestSchema(ma.Schema):
    borrower = fields.Nested(BorrowerRequestSchema, required=True)
    requested_amount = fields.Float(required=True)


# Serialize Outgoing Response data
class ApplicationResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Application
        include_fk = True
        include_relationships = True

    borrower = fields.Nested(BorrowerSchema)
    created_at = ma.auto_field(dump_only=True)
    updated_at = ma.auto_field(dump_only=True)
