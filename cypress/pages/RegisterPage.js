class RegisterPage {
  visit() {
    cy.visit('/register.html')
  }

  enterCvr(cvr) {
    cy.get('input[name="cvr"]').clear().type(cvr)
  }

  lookupCvr() {
    cy.get('button[data-cy="cvr-lookup"]').click()
  }

  enterEmail(email) {
    cy.get('input[type="email"]').clear().type(email)
  }

  enterPassword(password) {
    cy.get('input[type="password"]').clear().type(password)
  }

  submit() {
    cy.get('button[type="submit"]').click()
  }
}

export default new RegisterPage()
