import TodoPage from '../../pages/TodoPage'
import { story } from 'allure-cypress'

describe('002_E2E Tests (Cypress)', () => {
  beforeEach(() => {
    story('CRUD')
    cy.clearLocalStorage()
  })

  it('TC-TODO-001: Opret todo med gyldig titel → vises i listen', () => {
    cy.fixture('todo').then((todo) => {
      const newTodo = { id: 1, title: todo.title, completed: todo.completed }

      cy.intercept('GET', '**/todos', { statusCode: 200, body: [] }).as('getEmpty')
      cy.intercept('POST', '**/todos', { statusCode: 201, body: newTodo }).as('postTodo')

      cy.visit('/', {
        onBeforeLoad(win) {
          win.localStorage.setItem('token', 'test-token')
        },
      })
      cy.wait('@getEmpty')

      // Opdater GET intercept så listen returnerer den nye todo efter oprettelse
      cy.intercept('GET', '**/todos', { statusCode: 200, body: [newTodo] }).as('getWithTodo')

      TodoPage.addTodo(todo.title)
      cy.wait('@postTodo')
      cy.wait('@getWithTodo')

      cy.contains('[data-cy="todo-item"]', todo.title).should('be.visible')
    })
  })

  it('TC-TODO-002: Opret todo med tom titel → blokeret', () => {
    cy.intercept('GET', '**/todos', { statusCode: 200, body: [] }).as('getTodos')
    cy.intercept('POST', '**/todos').as('postTodo')

    cy.visit('/', {
      onBeforeLoad(win) {
        win.localStorage.setItem('token', 'test-token')
      },
    })
    cy.wait('@getTodos')

    cy.get('[data-cy="todo-submit"]').click()

    cy.get('@postTodo.all').should('have.length', 0)
    cy.get('[data-cy="todo-item"]').should('not.exist')
  })
})
