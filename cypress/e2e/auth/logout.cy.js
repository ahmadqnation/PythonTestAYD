import TodoPage from '../../pages/TodoPage'
import { story } from 'allure-cypress'

describe('002_E2E Tests (Cypress)', () => {
  beforeEach(() => {
    story('AUTH')
  })

  it('TC-AUTH-008: Klik Log ud → token fjernet og redirect til login', () => {
    cy.intercept('GET', '**/todos', { statusCode: 200, body: [] }).as('getTodos')

    cy.visit('/', {
      onBeforeLoad(win) {
        win.localStorage.setItem('token', 'test-token')
      },
    })

    cy.get('[data-cy="logout-btn"]', { timeout: 10000 }).should('be.visible')

    cy.get('[data-cy="logout-btn"]').click()

    cy.url().should('include', 'login.html')
    cy.window().its('localStorage').invoke('getItem', 'token').should('be.null')
  })
})
