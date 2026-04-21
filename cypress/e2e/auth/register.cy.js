import RegisterPage from '../../pages/RegisterPage'
import { story } from 'allure-cypress'

describe('002_E2E Tests (Cypress)', () => {
  beforeEach(() => {
    story('AUTH')
    cy.clearLocalStorage()
  })

  it('TC-AUTH-005: Gyldigt CVR opslag → firmanavn og adresse vises', () => {
    cy.intercept('GET', '**/cvr/*', {
      statusCode: 200,
      body: {
        firmanavn: 'Q Nation ApS',
        adresse: 'Testvej 1',
        postnummer: '8000',
        by: 'Aarhus',
      },
    }).as('cvrLookup')

    cy.fixture('user').then((user) => {
      RegisterPage.visit()
      RegisterPage.enterCvr(user.cvr)
      RegisterPage.lookupCvr()
      cy.wait('@cvrLookup')
      cy.get('#cvr-info').should('be.visible')
      cy.get('#cvr-info strong').should('have.text', 'Q Nation ApS')
    })
  })

  it('TC-AUTH-006: Registrering med gyldige data → konto oprettet og auto-login', () => {
    cy.intercept('GET', '**/cvr/*', {
      statusCode: 200,
      body: {
        firmanavn: 'Test Firma A/S',
        adresse: 'Testvej 1',
        postnummer: '1234',
        by: 'Testby',
      },
    }).as('cvrLookup')
    cy.intercept('POST', '**/auth/register', {
      statusCode: 201,
      body: { id: 1, email: 'testuser@test.dk' },
    }).as('register')
    cy.intercept('POST', '**/auth/login', {
      statusCode: 200,
      body: { access_token: 'mock-token-abc' },
    }).as('login')
    cy.intercept('GET', '**/todos', { statusCode: 200, body: [] }).as('getTodos')

    cy.fixture('user').then((user) => {
      RegisterPage.visit()
      RegisterPage.enterCvr(user.cvr)
      RegisterPage.lookupCvr()
      cy.wait('@cvrLookup')
      cy.get('#cvr-info').should('be.visible')
      RegisterPage.enterEmail(user.email)
      RegisterPage.enterPassword(user.password)
      RegisterPage.submit()
      cy.wait('@register')
      cy.url({ timeout: 10000 }).should('include', 'index.html')
    })
  })

  it('TC-AUTH-007: Ugyldigt CVR → fejlbesked vises', () => {
    cy.intercept('GET', '**/cvr/99999999', {
      statusCode: 404,
      body: { detail: 'CVR ikke fundet' },
    }).as('cvrNotFound')

    RegisterPage.visit()
    RegisterPage.enterCvr('99999999')
    RegisterPage.lookupCvr()
    cy.wait('@cvrNotFound')
    cy.get('#error-msg', { timeout: 5000 }).should('be.visible')
  })
})
