class TodoPage {
  addTodo(title) {
    cy.get('input[data-cy="todo-input"]').clear().type(title)
    cy.get('button[data-cy="todo-submit"]').click()
  }

  deleteTodo(title) {
    cy.contains('[data-cy="todo-item"]', title)
      .find('button[data-cy="todo-delete"]')
      .click()
  }

  editTodo(oldTitle, newTitle) {
    cy.contains('[data-cy="todo-item"]', oldTitle)
      .find('button[data-cy="todo-edit"]')
      .click()
    cy.get('input[data-cy="todo-edit-input"]').clear().type(newTitle)
    cy.get('button[data-cy="todo-save"]').click()
  }

  toggleTodo(title) {
    cy.contains('[data-cy="todo-item"]', title)
      .find('input[type="checkbox"]')
      .click()
  }
}

export default new TodoPage()
