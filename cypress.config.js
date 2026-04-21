const { defineConfig } = require('cypress')
const { allureCypress } = require('allure-cypress/reporter')

module.exports = defineConfig({
  e2e: {
    baseUrl: process.env.CYPRESS_BASE_URL || 'https://ahmadqnation.github.io/PythonTestAYD/app',
    allowCypressEnv: false,
    viewportWidth: 1280,
    viewportHeight: 720,
    video: false,
    screenshotOnRunFailure: true,
    setupNodeEvents(on, config) {
      allureCypress(on, config, {
        resultsDir: process.env.ALLURE_RESULTS_DIR || 'allure-results-cypress',
      })
      return config
    },
  },
})
