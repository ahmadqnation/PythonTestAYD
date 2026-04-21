import './commands'
import 'allure-cypress'
import { parameter, epic, feature, suite, subSuite } from 'allure-cypress'

const browserMap = {
  chrome:   { prefix: 'A', name: 'Chrome' },
  edge:     { prefix: 'B', name: 'Edge' },
  firefox:  { prefix: 'C', name: 'Firefox' },
  electron: { prefix: 'D', name: 'Electron' },
}

beforeEach(() => {
  const specPath = Cypress.spec.relative.replace(/\\/g, '/')
  if (specPath.includes('e2e/overview/')) return

  const { prefix, name } = browserMap[Cypress.browser.name] || { prefix: 'X', name: Cypress.browser.displayName }
  parameter('Browser', `${Cypress.browser.displayName} ${Cypress.browser.version}`)
  epic('001_Tests')
  feature(`001${prefix}_${name}`)
  subSuite(`${Cypress.browser.displayName} ${Cypress.browser.version}`)

  if (specPath.includes('e2e/auth/')) suite('Autentificering')
  else if (specPath.includes('e2e/todos/')) suite('Todo CRUD')
  else if (specPath.includes('e2e/non_functional/')) suite('Non-Funktionelle Krav')
})
