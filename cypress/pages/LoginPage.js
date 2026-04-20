class LoginPage {
  visit() {
    cy.visit('/login.html')
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

export default new LoginPage()
