import LoginPage from '../../pages/LoginPage'

describe('Autentificering — Login', () => {
  beforeEach(() => {
    cy.clearLocalStorage()
  })

  it('TC-AUTH-001: Åbn app når logget ind → redirect til Todo App', () => {
    cy.intercept('GET', '**/todos', { statusCode: 200, body: [] }).as('getTodos')
    cy.visit('/', {
      onBeforeLoad(win) {
        win.localStorage.setItem('token', 'test-token')
      },
    })
    cy.url().should('not.include', 'login.html')
    cy.get('#logout-btn').should('be.visible')
  })

  it('TC-AUTH-002: Åbn app uden login → redirect til login side', () => {
    cy.visit('/')
    cy.url().should('include', 'login.html')
    cy.get('input[type="email"]').should('be.visible')
  })

  it('TC-AUTH-003: Login med gyldige credentials → Token gemt og redirect til Todo App', () => {
    cy.intercept('POST', '**/auth/login', {
      statusCode: 200,
      body: { access_token: 'test-token-123' },
    }).as('loginRequest')
    cy.intercept('GET', '**/todos', { statusCode: 200, body: [] }).as('getTodos')

    cy.fixture('user').then((user) => {
      LoginPage.visit()
      LoginPage.enterEmail(user.email)
      LoginPage.enterPassword(user.password)
      LoginPage.submit()
      cy.wait('@loginRequest')
      cy.url({ timeout: 10000 }).should('include', 'index.html')
      cy.window().its('localStorage').invoke('getItem', 'token').should('eq', 'test-token-123')
    })
  })

  it('TC-AUTH-004: Login med forkerte credentials → Fejlbesked vises', () => {
    LoginPage.visit()
    LoginPage.enterEmail('forkert@email.dk')
    LoginPage.enterPassword('ForkertPassword123!')
    LoginPage.submit()
    cy.get('#error-msg', { timeout: 15000 }).should('be.visible')
  })
})
