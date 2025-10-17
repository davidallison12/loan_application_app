// Testing for Application Form Component

// This test fills out the application form and submits it, 
// then checks that the results page displays the expected information.
describe("Loan Application Flow", () => {
    it("submits the application form and shows results", () => {
        // Visit the application form page
        cy.visit("http://localhost:3000/"); // Adjust URL as needed

        // Fill out the form fields
        cy.get('input[name="first_name"]').type("John");
        cy.get('input[name="last_name"]').type("Doe");
        cy.get('input[name="email"]').type("john@email.com");
        cy.get('input[name="phone"]').type("555-555-5555");
        cy.get('input[name="ssn"]').type("123-45-5435");
        cy.get('input[name="address_1"]').type("123 Main St");
        cy.get('input[name="city"]').type("Anytown");
        cy.get('input[name="state"]').type("CA");
        cy.get('input[name="zip_code"]').type("90210");
        cy.get('input[name="requested_amount"]').type("40000");

        // Submit the form
        cy.get("button[type='submit']").click();

        // Verify that we are on the results page
        cy.url().should("include", "/result");

        // Check that status since it appears if approved or denied
        cy.contains("Status:").should("exist"); 


    })
})