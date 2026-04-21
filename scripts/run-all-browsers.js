const { execSync } = require('child_process')
const fs = require('fs')
const path = require('path')

const browsers = ['electron', 'chrome', 'edge', 'firefox']
const mergedDir = 'allure-results-cypress'
const overviewSpec = 'cypress/e2e/overview/kravsoversigt.cy.js,cypress/e2e/overview/e2e_overview.cy.js'
const browserSpec = [
  'cypress/e2e/auth/**/*.cy.js',
  'cypress/e2e/todos/**/*.cy.js',
  'cypress/e2e/non_functional/**/*.cy.js',
].join(',')

if (fs.existsSync(mergedDir)) {
  fs.rmSync(mergedDir, { recursive: true })
}
fs.mkdirSync(mergedDir)

function mergeResults(resultsDir) {
  if (fs.existsSync(resultsDir)) {
    const files = fs.readdirSync(resultsDir)
    for (const file of files) {
      fs.copyFileSync(path.join(resultsDir, file), path.join(mergedDir, file))
    }
    console.log(`  Merged ${files.length} result files from ${resultsDir}/`)
  }
}

let totalPassed = 0
let totalFailed = 0

// Overview tests køres KUN én gang med Electron
const overviewResultsDir = 'allure-results-overview'
if (fs.existsSync(overviewResultsDir)) {
  fs.rmSync(overviewResultsDir, { recursive: true })
}

console.log(`\n${'='.repeat(60)}`)
console.log(`  Overview: ELECTRON (én gang)`)
console.log(`${'='.repeat(60)}`)

try {
  execSync(`npx cypress run --spec "${overviewSpec}" --env allure=true`, {
    stdio: 'inherit',
    env: { ...process.env, ALLURE_RESULTS_DIR: overviewResultsDir },
  })
  console.log(`\n  overview PASSED`)
} catch {
  console.error(`\n  overview FAILED`)
}
mergeResults(overviewResultsDir)

// Browser tests køres 4 gange (én per browser)
for (const browser of browsers) {
  const resultsDir = `allure-results-${browser}`

  if (fs.existsSync(resultsDir)) {
    fs.rmSync(resultsDir, { recursive: true })
  }

  const cmd =
    browser === 'electron'
      ? `npx cypress run --spec "${browserSpec}" --env allure=true`
      : `npx cypress run --browser ${browser} --spec "${browserSpec}" --env allure=true`

  console.log(`\n${'='.repeat(60)}`)
  console.log(`  Browser: ${browser.toUpperCase()}`)
  console.log(`${'='.repeat(60)}`)

  try {
    execSync(cmd, {
      stdio: 'inherit',
      env: { ...process.env, ALLURE_RESULTS_DIR: resultsDir },
    })
    totalPassed++
    console.log(`\n  ${browser} PASSED`)
  } catch {
    totalFailed++
    console.error(`\n  ${browser} FAILED`)
  }

  mergeResults(resultsDir)
}

console.log(`\n${'='.repeat(60)}`)
console.log(`  DONE: ${totalPassed} browsers passed, ${totalFailed} failed`)
console.log(`  Merged results: ${mergedDir}/`)
console.log(`${'='.repeat(60)}\n`)
