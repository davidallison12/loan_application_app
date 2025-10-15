from app import db

class Borrower(db.Model):
    borrower_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address_1 = db.Column(db.String(200), nullable=False) # Street address, required for most users
    address_2 = db.Column(db.String(200))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20))
    ssn = db.Column(db.String(11), unique=True, nullable=False)  # Format: XXX-XX-XXXX

    applications = db.relationship("Application", backref="borrower", lazy=True)



class Application(db.Model):
    application_id = db.Column(db.Integer, primary_key=True)
    borrower_id = db.Column(db.Integer, db.ForeignKey('borrower.borrower_id'), nullable=False)
    requested_amount = db.Column(db.Float, nullable=False)
    open_credit_lines = db.Column(db.Integer, nullable=False)
    approved_amount = db.Column(db.Float)
    interst_rate = db.Column(db.Float)
    term_months = db.Column(db.Integer)
    monthly_payment = db.Column(db.Float)
    status = db.Column(db.String(50), nullable=False, default='Pending')  
    reason = db.Column(db.String(200))