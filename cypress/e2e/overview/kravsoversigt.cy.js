import { epic, feature, story, attachment, parentSuite, suite } from 'allure-cypress'

const thStyle = 'padding: 8px; text-align: left; border: 1px solid #dee2e6;'
const tdStyle = 'padding: 8px; text-align: left; border: 1px solid #dee2e6;'
const tableStyle = 'border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; font-size: 13px;'
const headerStyle = 'background-color: #f2f2f2;'
const titleStyle = 'font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; color: #1E293B; margin: 0 0 8px 0;'
const noteStyle =
  'font-family: Arial, sans-serif; font-size: 13px; color: #1E293B; ' +
  'background: #fffbe6; border: 1px solid #ffe58f; border-radius: 4px; ' +
  'padding: 8px 12px; margin: 0 0 12px 0;'

const funktionelle = [
  ['REQ-001', 'App redirecter til login når ikke autentificeret', 'Funktionel', 'Høj', 'TC-AUTH-002'],
  ['REQ-002', 'App viser Todo App når allerede logget ind', 'Funktionel', 'Høj', 'TC-AUTH-001'],
  ['REQ-003', 'Login med gyldige credentials → token gemt og redirect til app', 'Funktionel', 'Høj', 'TC-AUTH-003'],
  ['REQ-004', 'Login med forkerte credentials → fejlbesked vises', 'Funktionel', 'Høj', 'TC-AUTH-004'],
  ['REQ-005', 'CVR opslag returnerer firmanavn og adresse', 'Funktionel', 'Høj', 'TC-AUTH-005'],
  ['REQ-006', 'Registrering med gyldige data → konto oprettet og auto-login', 'Funktionel', 'Høj', 'TC-AUTH-006'],
  ['REQ-007', 'Ugyldigt CVR → fejlbesked vises', 'Funktionel', 'Høj', 'TC-AUTH-007'],
  ['REQ-008', 'Log ud → token fjernet og redirect til login', 'Funktionel', 'Høj', 'TC-AUTH-008'],
  ['REQ-009', 'Opret todo med gyldig titel → vises i listen', 'Funktionel', 'Høj', 'TC-TODO-001'],
  ['REQ-010', 'Tom titel blokerer oprettelse af todo', 'Funktionel', 'Høj', 'TC-TODO-002'],
  ['REQ-011', 'Marker todo som completed → strikethrough vises', 'Funktionel', 'Medium', 'TC-TODO-003'],
  ['REQ-012', 'Rediger todo titel → opdateret titel vises', 'Funktionel', 'Medium', 'TC-TODO-004'],
  ['REQ-013', 'Slet todo → fjernes fra listen', 'Funktionel', 'Høj', 'TC-TODO-005'],
]

const nonFunktionelle = [
  ['REQ-014', "API svarer inden 2 sekunder", 'Non-funktionel', 'Medium', 'TC-NFR-001'],
  ['REQ-015', "Alle API kald anvender HTTPS", 'Non-funktionel', 'Høj', 'TC-NFR-002'],
  ['REQ-016', "JWT token gemmes sikkert i localStorage efter login", 'Non-funktionel', 'Høj', 'TC-NFR-003'],
  ['REQ-017', "Applikationen understøtter Chrome, Edge, Firefox og Electron", 'Non-funktionel', 'Høj', 'TC-NFR-005'],
  ['REQ-018', "Systemet fungerer korrekt i aktuel browser", 'Non-funktionel', 'Høj', 'TC-NFR-005'],
  ['REQ-019', "CVR opslag viser firmanavn inden 3 sekunder", 'Non-funktionel', 'Medium', 'TC-NFR-004'],
  ['REQ-020', "CVR opslag returnerer feedback inden 3 sekunder", 'Non-funktionel', 'Medium', 'TC-NFR-004'],
]

function buildRows(krav, bgStyle) {
  return krav
    .map(
      ([id, beskrivelse, type, prioritet, tests]) =>
        `<tr${bgStyle}>` +
        `<td style="${tdStyle}">${id}</td>` +
        `<td style="${tdStyle}">${beskrivelse}</td>` +
        `<td style="${tdStyle}">${type}</td>` +
        `<td style="${tdStyle}">${prioritet}</td>` +
        `<td style="${tdStyle}">✅</td>` +
        `<td style="${tdStyle}">${tests}</td>` +
        `</tr>`
    )
    .join('')
}

const tabel =
  `<h3 style="${titleStyle}">Kravsoversigt — Todo App E2E</h3>` +
  `<p style="${noteStyle}">💡 Find testcases i Behaviors fanen under <strong>001_Tests → 001A_Chrome / 001B_Edge / 001C_Firefox / 001D_Electron</strong></p>` +
  `<table border="1" style="${tableStyle}">` +
  `<tr style="${headerStyle}">` +
  `<th style="${thStyle}">Krav ID</th>` +
  `<th style="${thStyle}">Beskrivelse</th>` +
  `<th style="${thStyle}">Type</th>` +
  `<th style="${thStyle}">Prioritet</th>` +
  `<th style="${thStyle}">Status</th>` +
  `<th style="${thStyle}">Testcase</th>` +
  `</tr>` +
  buildRows(funktionelle, '') +
  buildRows(nonFunktionelle, ' style="background-color: #f8f9fa;"') +
  `</table>`

const htmlContent = `<html><body style="margin:0;padding:20px;background:#fff;">${tabel}</body></html>`

describe('000_Dokumentation', () => {
  beforeEach(() => {
    parentSuite('000_Dokumentation')
    suite('Oversigt')
    epic('000_Dokumentation')
    feature('000A_Kravsoversigt')
    story('000A_Kravsoversigt')
  })

  it('Kravsoversigt — Todo App E2E', () => {
    attachment('Kravsoversigt', htmlContent, 'text/html')
  })
})
