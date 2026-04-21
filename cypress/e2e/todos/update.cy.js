import TodoPage from '../../pages/TodoPage'
import { story } from 'allure-cypress'

describe('002_E2E Tests (Cypress)', () => {
  beforeEach(() => {
    story('CRUD')
    cy.clearLocalStorage()
  })

  it('TC-TODO-003: Marker todo som completed → strikethrough vises', () => {
    cy.fixture('todo').then((todo) => {
      const existingTodo = { id: 1, title: todo.title, completed: false }
      const updatedTodo = { ...existingTodo, completed: true }

      cy.intercept('GET', '**/todos', { statusCode: 200, body: [existingTodo] }).as('getTodos')
      cy.intercept('PUT', '**/todos/1', { statusCode: 200, body: updatedTodo }).as('putTodo')

      cy.visit('/', {
        onBeforeLoad(win) {
          win.localStorage.setItem('token', 'test-token')
        },
      })
      cy.wait('@getTodos')

      TodoPage.toggleTodo(todo.title)
      cy.wait('@putTodo')

      cy.get('[data-cy="todo-item"]').should('have.class', 'completed')
    })
  })

  it('TC-TODO-004: Rediger todo titel → opdateret titel vises', () => {
    cy.fixture('todo').then((todo) => {
      const existingTodo = { id: 1, title: todo.title, completed: false }
      const newTitle = 'Opdateret todo titel'
      const updatedTodo = { ...existingTodo, title: newTitle }

      cy.intercept('GET', '**/todos', { statusCode: 200, body: [existingTodo] }).as('getTodosInitial')
      cy.intercept('PUT', '**/todos/1', { statusCode: 200, body: updatedTodo }).as('putTodo')

      cy.visit('/', {
        onBeforeLoad(win) {
          win.localStorage.setItem('token', 'test-token')
        },
      })
      cy.wait('@getTodosInitial')

      // Opdater GET intercept til fetchTodos() kaldet efter Gem
      cy.intercept('GET', '**/todos', { statusCode: 200, body: [updatedTodo] }).as('getTodosUpdated')

      TodoPage.editTodo(todo.title, newTitle)
      cy.wait('@putTodo')
      cy.wait('@getTodosUpdated')

      cy.contains('[data-cy="todo-item"]', newTitle).should('be.visible')
    })
  })
})
