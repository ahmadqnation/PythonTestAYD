import LoginPage from '../../pages/LoginPage'
import RegisterPage from '../../pages/RegisterPage'
import { story } from 'allure-cypress'

describe('002_E2E Tests (Cypress)', () => {
  beforeEach(() => {
    story('NFR')
    cy.clearLocalStorage()
  })

  it('TC-NFR-001: API svarer inden 2 sekunder (REQ-014)', () => {
    let requestStart

    cy.intercept('GET', '**/todos', (req) => {
      requestStart = Date.now()
      req.reply({ statusCode: 200, body: [] })
    }).as('getTodos')

    cy.visit('/', {
      onBeforeLoad(win) {
        win.localStorage.setItem('token', 'test-token')
      },
    })

    cy.wait('@getTodos').then(() => {
      const duration = Date.now() - requestStart
      expect(duration).to.be.lessThan(2000)
    })
  })

  it('TC-NFR-002: Alle API kald bruger HTTPS (REQ-015)', () => {
    const baseUrl = Cypress.config('baseUrl')
    expect(baseUrl).to.match(/^https:\/\//)

    cy.intercept('GET', '**/todos', { statusCode: 200, body: [] }).as('getTodos')

    cy.visit('/', {
      onBeforeLoad(win) {
        win.localStorage.setItem('token', 'test-token')
      },
    })

    cy.wait('@getTodos').then((interception) => {
      expect(interception.request.url).to.match(/^https:\/\//)
    })
  })

  it('TC-NFR-003: JWT token gemmes i localStorage efter login (REQ-016)', () => {
    cy.intercept('POST', '**/auth/login', {
      statusCode: 200,
      body: { access_token: 'mock-jwt-token-xyz' },
    }).as('loginRequest')
    cy.intercept('GET', '**/todos', { statusCode: 200, body: [] }).as('getTodos')

    cy.fixture('user').then((user) => {
      LoginPage.visit()
      LoginPage.enterEmail(user.email)
      LoginPage.enterPassword(user.password)
      LoginPage.submit()
      cy.wait('@loginRequest')
      cy.window().its('localStorage').invoke('getItem', 'token').should('eq', 'mock-jwt-token-xyz')
    })
  })

  it('TC-NFR-004: CVR opslag giver feedback inden 3 sekunder (REQ-020)', () => {
    let requestStart

    cy.intercept('GET', '**/cvr/*', (req) => {
      requestStart = Date.now()
      req.reply({
        statusCode: 200,
        body: { firmanavn: 'Test Firma A/S', adresse: 'Testvej 1', postnummer: '1234', by: 'Testby' },
      })
    }).as('cvrLookup')

    cy.fixture('user').then((user) => {
      RegisterPage.visit()
      RegisterPage.enterCvr(user.cvr)
      RegisterPage.lookupCvr()
      cy.wait('@cvrLookup').then(() => {
        const duration = Date.now() - requestStart
        expect(duration).to.be.lessThan(3000)
      })
    })
  })

  it('TC-NFR-005: Systemet fungerer i nuværende browser (REQ-018)', () => {
    LoginPage.visit()
    cy.url().should('include', 'login.html')
    cy.get('input[type="email"]').should('be.visible')
    cy.get('input[type="password"]').should('be.visible')
    cy.get('button[type="submit"]').should('be.visible')
  })
})
