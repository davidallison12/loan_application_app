#  💰 Loan Application Project

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node-24.4.0-green)](https://nodejs.org/)

Single page-application to submit and process loan applications. The app allows borrowers to fill out a loan application form, validate the data given, caluclate the loan details and display the results in real time. 

---

## ✅ Acceptance Criteria 
 - Submit a loan application with borrower info
 - Approve or deny applications based on internal rules using loan amount and open credit lines:
   - If loan < $10,000 or > $50,000 -> Denied
   - If credit lines <10 -> Approved w/ 36-month term + 10% interest rate
   - If credit lines >=10 and <=50 -> Approved w/ 24-month term + 20% interst rate
   - if credit line >50 -> Denied
 - Offer shoudl clearly be presenter to borrower
 - Borrower applications should persist in database
 - Open credit lines will be randomly generated
 - Borrowers can use web or mobile device to apply for loan (Responsive)
 - Must at least include test case for scenario if credit lines >=10 and <=50


---
## 🧩 Tech Stack 
**Frontend:** 
- React 18
- Tailwind CSS
- Axios
- React Router

**Backend**
- Python 3.13
- Flask
- SQLAlchemy - ORM for DB Models and DB Operations
- Marshmallow - Input Validation + Serialization for API requests

**Database**
- SQlite

**Testing**
- Pytest(backend)
- Cypress(frontend)

**Linters**
- Prettier (Frontend)
- Flake8 + Black (Backend)

---

## 🏛️ Architecture Overview
**Frontend**
  - SPA w/ form page for loan applications and results page for displaying approval/denial details.
  - Tailwind CSS for manageable responsive design
  - React Router for Single-Page Navigation
  - Cypress used to for e2e test on full application flow


**Backend**
  - Contains Flask REST endpoint for handling handle form validation, borrower creation, validation, loan calculations and application creation.
  - Marshmallow - To ensure consistency across API requests and responses
  - Pytest in order to test application creation flow
    - Scenarios
      - Credit lines < 10
      - Credit lines >=10 and <= 50
      - Credit lines > 50

**Database**
- SQLAlchemy ORM with SQLite for data persistance

---
## 🧠 Design and Thought Process

### DB Design

Two Tables:

**Borrowers**
- Stores all borrower personal info
- Unique constraint on "ssn" to prevent duplication
- One Borrower to Many Applications

**Applications**
- Linked to `Borrowers` through `borrower_id`
- Stores requested amount, approved amount, interest rate, monthly payment, term, status and reason for denial if applicable
- Calculate interest, term, and monthly payment based off terms on approved applications

**POST /api/applications**
- Accepts borrower data and requested loan amount
- Validates borrower data (includes ssn format and uniqueness)
- Determines approval based off internal rules
- Returns full application object w/ status and loan details excluding SSN(PII)
- **Payload Structure:**
    ```json
    {
      "borrower": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@email.com",
        "phone": "555-555-5555",
        "address_1": "123 Main St",
        "address_2": "Apt 4B",
        "city": "Anytown",
        "state": "CA",
        "zip_code": "90210",
        "ssn": "123-45-6789"
      },
      "requested_amount": 40000
    }
    ```


### Schema Diagram

```
Borrowers
+-------------------+
| id (PK) |
| first_name |
| last_name |
| email |
| phone |
| address_1 |
| address_2 |
| city |
| state |
| zip_code |
| ssn |
| created_at |
+-------------------+


Applications
+-------------------+
| id (PK) |
| borrower_id (FK) |
| requested_amount |
| approved_amount |
| interest_rate |
| monthly_payment |
| term_months |
| status |
| reason |
+-------------------+
```

---
## 🚀 Local Setup

### Backend
#### 1. Clone the Repo
```bash
git clone git@github.com:davidallison12/loan_application_app.git (SSH link)
cd loan_application_app
```

#### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
Backend will now run on `http://localhost:5000`

#### Frontend Setup (Ideally use a separate tab for running front end as well)
```bash
cd ../frontend
npm install
npm run dev
```
Frontend runs on http://localhost:3000

---
## 🖥️ How to Use 

1. Open the application in your browser at http://localhost:3000.

2. Fill out the loan application form with all required fields.

3. Submit the form.

4. Results page displays:
  - ✅ Approved: monthly payment, interest rate, approved amount, term.

  - ❌ Denied: reason for denial.


---
## 🧪 Testing

- Backend: Pytest for Unit Tests for API Endpoints
- Frontend: Cypress for E2E tesing of form submission and results validation

#### Accessing/Running Backend Tests
```bash
cd backend
pytest -v tests/  # Verbose testing
```

#### Accessing/Running Frontend Test 
1. Run following:
```bash
cd frontend
npx cypress open
```
2. Once in navigate to E2E testing and select desired browser
3. Navigate to test_application_form.cy.js to run test

**OR** 

```bash
cd frontend
npx cypress run # Run tests headlessly
```
---
## 🔮 Future Improvements 
- Expand Application endpoint(GET, PUT/PATCH, DELETE)
- Add specific Borrower Endpoints
- Create Authentication and Authorization based off Borrower Table
- Improve Error Handling on Frontend
  - More robust messaging for specfic errors. Along with Action step for borrower.
- Build out Frontend w/ a review page and added input validations
  - Phone
  - Zip Code
  - State (Use Abbreviation instead of allowing user to type what they want)
- Additional Backend Validations on inputs
  -   Using Google Maps to confirm addresses
  -   Phone number format validation
- SSN Encryption and Masking
- Replace SQLite with PostgreSQL for scalability more robust security
- Logging for more advanced troubleshooting
- More use of environment variables for urls and additonal fields 

---
## ✉️ Contact 
If you have any questions regarding this application, please reach out to David Allison at dgreenal@gmail.com
 
    




