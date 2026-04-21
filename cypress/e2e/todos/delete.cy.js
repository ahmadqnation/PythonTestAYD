import TodoPage from '../../pages/TodoPage'
import { story } from 'allure-cypress'

describe('002_E2E Tests (Cypress)', () => {
  beforeEach(() => {
    story('CRUD')
    cy.clearLocalStorage()
  })

  it('TC-TODO-005: Slet todo → fjernes fra listen', () => {
    cy.fixture('todo').then((todo) => {
      const existingTodo = { id: 1, title: todo.title, completed: false }

      cy.intercept('GET', '**/todos', { statusCode: 200, body: [existingTodo] }).as('getTodos')
      cy.intercept('DELETE', '**/todos/1', { statusCode: 200, body: {} }).as('deleteTodo')

      cy.visit('/', {
        onBeforeLoad(win) {
          win.localStorage.setItem('token', 'test-token')
        },
      })
      cy.wait('@getTodos')

      cy.contains('[data-cy="todo-item"]', todo.title).should('be.visible')

      TodoPage.deleteTodo(todo.title)
      cy.wait('@deleteTodo')

      cy.get('[data-cy="todo-item"]').should('not.exist')
    })
  })
})
