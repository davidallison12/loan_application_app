#  💰 Loan Application Project

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node-24.4.0-green)](https://nodejs.org/)

Single page-application to submit and process loan applications. The app allows borrowers to fill out a loan application form, validate the data given, caluclate the loan details and display the results in real time. 

[🎬 Watch the live demo on Loom](https://www.loom.com/share/c3d30cf74bb4412bb1d791ab76355eae)

#### Links to Live Deployments

**Frontend:** https://loan-application-app-rose.vercel.app

**Backend:** https://loan-application-app.onrender.com

**Backend Health Endpoint**: https://loan-application-app.onrender.com/api/health


---

## ✅ Acceptance Criteria 
 - User can access app through a website
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
 - Open credit lines based on randomly generated number between 0 and 100


---
## 🧩 Tech Stack 
**Frontend:** React 18, Tailwind CSS, Axios, React Router

**Backend:** Python 3.13, Flask, SQLAlchemy, Marshmallow 

**Database:** SQlite

**Testing:** Pytest(Backend), Cypress(Frontend)

**Linters:** Prettier(Frontend), Flake8 + Black(Backend)


---

## 🏛️ Architecture Overview and Approach
**Frontend**
  - Single Page Application using React containing a form page for loan applications and results page for displaying approval/denial details. This includes validations on the frontend for required fields and formatting validiation for SSN. 
  - Tailwind CSS used for scalable and manageble frontend design. Also greate for managing responsive design needs.
  - React Router for Single-Page Navigation. This is quick to implement for an app with limited pages
  - Cypress used to for e2e test on full application flow. Developer friendly and simple to implement and scale. Improve consistency across the application.


**Backend**
  - Contains a Flask REST endpoint that is responsible for the follwing:
    - loan application form validation
    - borrower creation validation (utiliy function)
    - loan calculations using standard loan formulas and application creation (utility function)
  
  Using:
  - Marshmallow: To ensure consistency across API requests and responses
  - Pytest: To test application creation flow
    - Scenarios
      - Credit lines < 10
      - Credit lines >=10 and <= 50
      - Credit lines > 50

**Database**
- SQLAlchemy ORM with SQLite for data persistance
- PostgreSQL for Render deployment

**Deployment**
- **Vercel:** Frontend Deployment
  - Easy React hosting and deployment
  - Seperation of concerns 
- **Render:** Backend Deployment
  - Built in Database (PostgreSQL)
  - Handles HTTPS and builds automatically
  - Straightforward setup
  - Unfortunately needs to be booted up when getting accessed. This can take up to 30 seconds. 


---
## 🧠 Design and Thought Process

### DB Design

#### Tables

**Borrowers**
- **Pupose** Stores all personal info of each borrower applicant
- **Fields**
  - `borrower_id` - `Integer`: Primary Key
  - `first_name`, `last_name` – `String`
  - `email` – `String`,
  - `phone` – `String` 
  - `address_1` – `String`,
  - `address_2` – `String`,
  - `city` – `String`,
  - `state` – `String`,
  - `zip_code` – `String`
  - `ssn` – `String`: Unique identifier for validation and duplication prevention.
  - `created_at` – `Datetime`: Timestamp for when the borrower was added.
- **Thought Process:** Create a seperate table that stores all borrower identification and contact information. This allows for a normalized table and avoidance of data redundancy. 

**Applications**
- **Purpose:** Track loan requests, approvals, and calculated metrics.
- **Fields:**
  - `application_id` - `Integer`: Primary key
  - `borrower_id` – `Integer` Foreign key linking to the Borrowers table.
  - `requested_amount` – `Float`
  - `approved_amount` – `Float`: Assumed this was the amount requested at this time. This however could change in the future as more complex rules are implemented for loan determinations. 
  - `interest_rate` – `Float`: Determined based on internal rules listed in acceptance criteria
  - `monthly_payment` – `Float` Calculated using standard loan formulas.
  - `term_months` – `Integer`: Determined based on internal rules listed in acceptance criteria
  - `status` – `String`: Tracks whether the loan is `Approved` or `Denied`.
  - `reason` – `String`: Optional field providing reason for denial.
- **Thought Process:** Seperating applications from borrowers allows for borrowers to have multiple applications. This will also make tracking approval decisions simpler.

#### API Design 

**POST /api/applications**
- **Purpose:** Endpoint for submitting new loan applications
- **Features**
  - Accepts borrower data and requested loan amount
  - Validates borrower data (includes ssn format and uniqueness)
  - Determines approval based off internal rules
  - Returns full application object with status and loan details excluding SSN(PII)
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
- **Response Structure:**
```json
{
  "application_id": 27,
  "approved_amount": 15000.0,
  "borrower": {
    "address_1": "123 Main St",
    "address_2": "Apt 4B",
    "borrower_id": 16,
    "city": "Anytown",
    "created_at": "2025-10-18T22:01:05.251684",
    "email": "email@email.com",
    "first_name": "John",
    "last_name": "Soe",
    "phone": "555-123-4567",
    "state": "CA",
    "updated_at": "2025-10-18T22:01:05.251695",
    "zip_code": "12345"
  },
  "borrower_id": 16,
  "created_at": "2025-10-18T22:01:05.253806",
  "interest_rate": 0.2,
  "monthly_payment": 763.44,
  "open_credit_lines": 27,
  "reason": null,
  "requested_amount": 15000.0,
  "status": "Approved",
  "term_months": 24,
  "updated_at": "2025-10-18T22:01:05.253808"
}
```
- **Though Process:** Combining both the borrower information and financial request information in the same endpoint allows for the quick creation or lookup of new borrower data. Followed by immediate processing of loan applicaiton. In the future, we can potentially use the link between applications and borrowers to gain greater understanding in the how ouo customers used our product. 


---
## 🖥️ How to Use Live URL
NOTE: Backend API can take up to 30 seconds to start up. To ensure quick operation go to https://loan-application-app.onrender.com before beginning. If you do not do this, the first submission on front-end will take up to 30 seconds to process

1. Open the application in your browser at https://loan-application-app-rose.vercel.app

2. Fill out the loan application form with all required fields.
   Note: If you use a requested amount < $10,000 or > $50,000 application will be denied

3. Submit the form.

4. Results page displays (Based on scenarios listed in acceptance criteria):
  - ✅ Approved: monthly payment, interest rate, approved amount, term.

  - ❌ Denied: reason for denial.


---
## 🚀 Local Setup

### Backend
#### 1. Clone the Repo
```bash
git clone git@github.com:davidallison12/loan_application_app.git (SSH link)
cd loan_application_app
```

#### 2. Backend Setup
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
Check health by going to `http://localhost:5000/api/health`

#### 3. Frontend Setup (Ideally use a separate tab for running front end as well)
```bash
cd ../frontend
npm install
npm start
```
Frontend runs on `http://localhost:3000`


---
## 🖥️ How to Use Locally

1. **Locallly:** Open the application in your browser at http://localhost:3000.

2. Fill out the loan application form with all required fields.
   Note: If you use a requested amount < $10,000 or > $50,000 application will be denied

4. Submit the form.

5. Results page displays (Based on scenarios listed in acceptance criteria):
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

#### Example Curl For Testing Endpoint
```bash
curl -X POST http://127.0.0.1:5000/api/applications \
-H "Content-Type: application/json" \
-d '{
  "borrower": {
    "first_name": "John",
    "last_name": "Doe",
    "address_1": "123 Main St",
    "address_2": "Apt 4B",
    "city": "Anytown",
    "state": "CA",
    "zip_code": "12345",
    "email": "email@email.com",
    "phone": "555-123-4567",
    "ssn": "213-44-6989"
  },
  "requested_amount": 15000
}'
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

**Backend**
- Expand Application endpoints (GET, PUT/PATCH, DELETE)
- Add specific Borrower Endpoints
- Create Authentication and Authorization based off Borrower Table
- Additional Backend Validations on inputs
  -   Using Google Maps to confirm addresses
- SSN Encryption and Masking
- Replace SQLite with PostgreSQL for scalability and more robust security (Postgres used with Render but SQLite locally)
- Add logging for more advanced troubleshooting


**Frontend**
- Improve Error Handling on Frontend for better user experience
  - More robust messaging for specfic errors. Along with Action step for borrower.
- Build out Frontend w/ a review page and added input validations
  - Phone
  - Zip Code
  - State (Use Abbreviation instead of allowing user to type what they want)
- Have a loading icon or animation to alert people page is loading and not frozen or erroring.

---
## ✉️ Contact 
If you have any questions regarding this application, please reach out to David Allison at dgreenal@gmail.com
 
    




