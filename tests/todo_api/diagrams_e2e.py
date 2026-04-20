def _auth_svg() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" width="680" height="310">
  <defs>
    <linearGradient id="ea_bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#F8FAFC"/><stop offset="100%" style="stop-color:#F1F5F9"/>
    </linearGradient>
    <linearGradient id="ea_green" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#34D399"/><stop offset="100%" style="stop-color:#10B981"/>
    </linearGradient>
    <linearGradient id="ea_red" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#F87171"/><stop offset="100%" style="stop-color:#EF4444"/>
    </linearGradient>
    <linearGradient id="ea_blue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#60A5FA"/><stop offset="100%" style="stop-color:#3B82F6"/>
    </linearGradient>
    <linearGradient id="ea_amber" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FCD34D"/><stop offset="100%" style="stop-color:#F59E0B"/>
    </linearGradient>
    <marker id="ea_arr" markerWidth="8" markerHeight="6" refX="7" refY="3"
            orient="auto" markerUnits="userSpaceOnUse">
      <polygon points="0 0, 8 3, 0 6" fill="#94A3B8"/>
    </marker>
  </defs>
  <rect width="680" height="310" fill="url(#ea_bg)" rx="10"/>
  <rect width="680" height="310" fill="none" stroke="#E2E8F0" stroke-width="1.5" rx="10"/>

  <!-- 1: Åbn app -->
  <rect x="10" y="22" width="80" height="26" rx="6" fill="url(#ea_blue)" stroke="#2563EB" stroke-width="1"/>
  <text x="50" y="39" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Åbn app</text>

  <!-- 1→2 -->
  <line x1="90" y1="35" x2="108" y2="35" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ea_arr)"/>

  <!-- 2: Logget ind? diamond (cx=153,cy=35,hw=43,hh=18) -->
  <polygon points="153,17 196,35 153,53 110,35" fill="url(#ea_amber)" stroke="#D97706" stroke-width="1"/>
  <text x="153" y="32" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="white">Logget</text>
  <text x="153" y="43" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="white">ind?</text>

  <!-- 2→3 Ja -->
  <line x1="196" y1="35" x2="220" y2="35" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ea_arr)"/>
  <text x="208" y="30" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="#10B981" font-weight="bold">Ja</text>

  <!-- 3: Todo App green -->
  <rect x="220" y="22" width="85" height="26" rx="6" fill="url(#ea_green)" stroke="#059669" stroke-width="1"/>
  <text x="262" y="39" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Todo App ✓</text>

  <!-- 2→4 Nej -->
  <line x1="153" y1="53" x2="153" y2="80" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ea_arr)"/>
  <text x="163" y="69" text-anchor="start" font-family="Arial,sans-serif" font-size="9" fill="#EF4444" font-weight="bold">Nej</text>

  <!-- 4: Login side -->
  <rect x="113" y="80" width="80" height="26" rx="6" fill="url(#ea_blue)" stroke="#2563EB" stroke-width="1"/>
  <text x="153" y="97" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Login side</text>

  <!-- 4→5 -->
  <line x1="193" y1="93" x2="222" y2="93" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ea_arr)"/>

  <!-- 5: Har konto? diamond (cx=265,cy=93,hw=43,hh=18) -->
  <polygon points="265,75 308,93 265,111 222,93" fill="url(#ea_amber)" stroke="#D97706" stroke-width="1"/>
  <text x="265" y="90" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="white">Har</text>
  <text x="265" y="101" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="white">konto?</text>

  <!-- 5→6 Ja -->
  <line x1="308" y1="93" x2="331" y2="93" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ea_arr)"/>
  <text x="319" y="88" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="#10B981" font-weight="bold">Ja</text>

  <!-- 6: Indtast login -->
  <rect x="331" y="80" width="95" height="26" rx="6" fill="url(#ea_blue)" stroke="#2563EB" stroke-width="1"/>
  <text x="378" y="97" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Indtast login</text>

  <!-- 6→7 -->
  <line x1="426" y1="93" x2="445" y2="93" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ea_arr)"/>

  <!-- 7: Korrekte? diamond (cx=490,cy=93,hw=45,hh=18) -->
  <polygon points="490,75 535,93 490,111 445,93" fill="url(#ea_amber)" stroke="#D97706" stroke-width="1"/>
  <text x="490" y="97" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="white">Korrekte?</text>

  <!-- 7→8 Ja -->
  <line x1="535" y1="93" x2="558" y2="93" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ea_arr)"/>
  <text x="546" y="88" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="#10B981" font-weight="bold">Ja</text>

  <!-- 8: Token gemt green -->
  <rect x="558" y="80" width="95" height="26" rx="6" fill="url(#ea_green)" stroke="#059669" stroke-width="1"/>
  <text x="605" y="97" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" font-weight="bold" fill="white">Token gemt ✓</text>

  <!-- 7→9 Nej -->
  <line x1="490" y1="111" x2="490" y2="135" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ea_arr)"/>
  <text x="500" y="126" text-anchor="start" font-family="Arial,sans-serif" font-size="9" fill="#EF4444" font-weight="bold">Nej</text>

  <!-- 9: Fejlbesked red -->
  <rect x="445" y="135" width="90" height="26" rx="6" fill="url(#ea_red)" stroke="#DC2626" stroke-width="1"/>
  <text x="490" y="152" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Fejlbesked ✗</text>

  <!-- 5→10 Nej -->
  <line x1="265" y1="111" x2="265" y2="180" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ea_arr)"/>
  <text x="275" y="148" text-anchor="start" font-family="Arial,sans-serif" font-size="9" fill="#EF4444" font-weight="bold">Nej</text>

  <!-- 10: Registrering -->
  <rect x="222" y="180" width="86" height="26" rx="6" fill="url(#ea_blue)" stroke="#2563EB" stroke-width="1"/>
  <text x="265" y="197" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Registrering</text>

  <!-- 10→11 -->
  <line x1="308" y1="193" x2="328" y2="193" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ea_arr)"/>

  <!-- 11: Gyldigt CVR? diamond (cx=380,cy=193,hw=52,hh=18) -->
  <polygon points="380,175 432,193 380,211 328,193" fill="url(#ea_amber)" stroke="#D97706" stroke-width="1"/>
  <text x="380" y="190" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="white">Gyldigt</text>
  <text x="380" y="201" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="white">CVR?</text>

  <!-- 11→12 Ja -->
  <line x1="432" y1="193" x2="454" y2="193" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ea_arr)"/>
  <text x="443" y="188" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="#10B981" font-weight="bold">Ja</text>

  <!-- 12: Firma vises green -->
  <rect x="454" y="180" width="95" height="26" rx="6" fill="url(#ea_green)" stroke="#059669" stroke-width="1"/>
  <text x="501" y="197" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Firma vises</text>

  <!-- 12→13 -->
  <line x1="501" y1="206" x2="501" y2="223" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ea_arr)"/>

  <!-- 13: Konto oprettet green -->
  <rect x="449" y="223" width="106" height="26" rx="6" fill="url(#ea_green)" stroke="#059669" stroke-width="1"/>
  <text x="502" y="240" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" font-weight="bold" fill="white">Konto oprettet</text>

  <!-- 13→14 -->
  <line x1="502" y1="249" x2="502" y2="266" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ea_arr)"/>

  <!-- 14: Auto-login green -->
  <rect x="457" y="266" width="90" height="26" rx="6" fill="url(#ea_green)" stroke="#059669" stroke-width="1"/>
  <text x="502" y="283" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Auto-login ✓</text>

  <!-- 11→15 Nej -->
  <line x1="380" y1="211" x2="380" y2="253" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ea_arr)"/>
  <text x="390" y="235" text-anchor="start" font-family="Arial,sans-serif" font-size="9" fill="#EF4444" font-weight="bold">Nej</text>

  <!-- 15: CVR fejl red -->
  <rect x="338" y="253" width="84" height="26" rx="6" fill="url(#ea_red)" stroke="#DC2626" stroke-width="1"/>
  <text x="380" y="270" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">CVR fejl ✗</text>
</svg>"""


def _crud_svg() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" width="680" height="185">
  <defs>
    <linearGradient id="ec_bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#F8FAFC"/><stop offset="100%" style="stop-color:#F1F5F9"/>
    </linearGradient>
    <linearGradient id="ec_green" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#34D399"/><stop offset="100%" style="stop-color:#10B981"/>
    </linearGradient>
    <linearGradient id="ec_red" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#F87171"/><stop offset="100%" style="stop-color:#EF4444"/>
    </linearGradient>
    <linearGradient id="ec_blue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#60A5FA"/><stop offset="100%" style="stop-color:#3B82F6"/>
    </linearGradient>
    <linearGradient id="ec_amber" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FCD34D"/><stop offset="100%" style="stop-color:#F59E0B"/>
    </linearGradient>
    <marker id="ec_arr" markerWidth="8" markerHeight="6" refX="7" refY="3"
            orient="auto" markerUnits="userSpaceOnUse">
      <polygon points="0 0, 8 3, 0 6" fill="#94A3B8"/>
    </marker>
  </defs>
  <rect width="680" height="185" fill="url(#ec_bg)" rx="10"/>
  <rect width="680" height="185" fill="none" stroke="#E2E8F0" stroke-width="1.5" rx="10"/>

  <!-- 1: Indtast titel -->
  <rect x="15" y="22" width="90" height="26" rx="6" fill="url(#ec_blue)" stroke="#2563EB" stroke-width="1"/>
  <text x="60" y="39" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Indtast titel</text>

  <!-- 1→2 -->
  <line x1="105" y1="35" x2="131" y2="35" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ec_arr)"/>

  <!-- 2: Tom titel? diamond (cx=177,cy=35,hw=46,hh=18) -->
  <polygon points="177,17 223,35 177,53 131,35" fill="url(#ec_amber)" stroke="#D97706" stroke-width="1"/>
  <text x="177" y="32" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="white">Tom</text>
  <text x="177" y="43" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="white">titel?</text>

  <!-- 2→3 Ja -->
  <line x1="223" y1="35" x2="250" y2="35" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ec_arr)"/>
  <text x="236" y="30" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="#10B981" font-weight="bold">Ja</text>

  <!-- 3: Blokeret red -->
  <rect x="250" y="22" width="85" height="26" rx="6" fill="url(#ec_red)" stroke="#DC2626" stroke-width="1"/>
  <text x="292" y="39" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Blokeret ✗</text>

  <!-- 2→4 Nej -->
  <line x1="177" y1="53" x2="177" y2="92" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ec_arr)"/>
  <text x="187" y="75" text-anchor="start" font-family="Arial,sans-serif" font-size="9" fill="#EF4444" font-weight="bold">Nej</text>

  <!-- 4: Todo oprettet green -->
  <rect x="130" y="92" width="95" height="26" rx="6" fill="url(#ec_green)" stroke="#059669" stroke-width="1"/>
  <text x="177" y="109" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" font-weight="bold" fill="white">Todo oprettet</text>

  <!-- 4→5 -->
  <line x1="225" y1="105" x2="260" y2="105" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ec_arr)"/>

  <!-- 5: Handling? diamond (cx=310,cy=105,hw=50,hh=18) -->
  <polygon points="310,87 360,105 310,123 260,105" fill="url(#ec_amber)" stroke="#D97706" stroke-width="1"/>
  <text x="310" y="109" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" font-weight="bold" fill="white">Handling?</text>

  <!-- Fan-out trunk: vertical line at x=360 from y=70 to y=140 -->
  <line x1="360" y1="70" x2="360" y2="140" stroke="#94A3B8" stroke-width="1.5"/>

  <!-- 5→6 Marker -->
  <line x1="360" y1="70" x2="430" y2="70" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ec_arr)"/>
  <text x="395" y="65" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="#475569" font-weight="bold">Marker</text>

  <!-- 5→7 Rediger -->
  <line x1="360" y1="105" x2="430" y2="105" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ec_arr)"/>
  <text x="395" y="100" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="#475569" font-weight="bold">Rediger</text>

  <!-- 5→8 Slet -->
  <line x1="360" y1="140" x2="430" y2="140" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#ec_arr)"/>
  <text x="395" y="153" text-anchor="middle" font-family="Arial,sans-serif" font-size="9" fill="#475569" font-weight="bold">Slet</text>

  <!-- 6: Completed green -->
  <rect x="430" y="57" width="90" height="26" rx="6" fill="url(#ec_green)" stroke="#059669" stroke-width="1"/>
  <text x="475" y="74" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Completed ✓</text>

  <!-- 7: Titel opdateret green -->
  <rect x="430" y="92" width="110" height="26" rx="6" fill="url(#ec_green)" stroke="#059669" stroke-width="1"/>
  <text x="485" y="109" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" font-weight="bold" fill="white">Titel opdateret ✓</text>

  <!-- 8: Fjernet green -->
  <rect x="430" y="127" width="80" height="26" rx="6" fill="url(#ec_green)" stroke="#059669" stroke-width="1"/>
  <text x="470" y="144" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Fjernet ✓</text>
</svg>"""


def _logout_svg() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" width="680" height="80">
  <defs>
    <linearGradient id="el_bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#F8FAFC"/><stop offset="100%" style="stop-color:#F1F5F9"/>
    </linearGradient>
    <linearGradient id="el_green" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#34D399"/><stop offset="100%" style="stop-color:#10B981"/>
    </linearGradient>
    <linearGradient id="el_blue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#60A5FA"/><stop offset="100%" style="stop-color:#3B82F6"/>
    </linearGradient>
    <marker id="el_arr" markerWidth="8" markerHeight="6" refX="7" refY="3"
            orient="auto" markerUnits="userSpaceOnUse">
      <polygon points="0 0, 8 3, 0 6" fill="#94A3B8"/>
    </marker>
  </defs>
  <rect width="680" height="80" fill="url(#el_bg)" rx="10"/>
  <rect width="680" height="80" fill="none" stroke="#E2E8F0" stroke-width="1.5" rx="10"/>

  <!-- 1: Klik Log ud -->
  <rect x="22" y="22" width="95" height="26" rx="6" fill="url(#el_blue)" stroke="#2563EB" stroke-width="1"/>
  <text x="69" y="39" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Klik Log ud</text>

  <!-- 1→2 -->
  <line x1="117" y1="35" x2="167" y2="35" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#el_arr)"/>

  <!-- 2: Token fjernet green -->
  <rect x="167" y="22" width="105" height="26" rx="6" fill="url(#el_green)" stroke="#059669" stroke-width="1"/>
  <text x="219" y="39" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" font-weight="bold" fill="white">Token fjernet</text>

  <!-- 2→3 -->
  <line x1="272" y1="35" x2="332" y2="35" stroke="#94A3B8" stroke-width="1.5" marker-end="url(#el_arr)"/>

  <!-- 3: Redirect login green -->
  <rect x="332" y="22" width="110" height="26" rx="6" fill="url(#el_green)" stroke="#059669" stroke-width="1"/>
  <text x="387" y="39" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" font-weight="bold" fill="white">Redirect login ✓</text>
</svg>"""


def e2e_diagram() -> str:
    legend = (
        '<div style="display:flex;gap:16px;margin-bottom:10px;font-family:Arial,sans-serif;font-size:11px;color:#475569;">'
        '<span><span style="display:inline-block;width:12px;height:12px;background:#10B981;border-radius:2px;margin-right:4px;vertical-align:middle;"></span>Success</span>'
        '<span><span style="display:inline-block;width:12px;height:12px;background:#EF4444;border-radius:2px;margin-right:4px;vertical-align:middle;"></span>Fejl</span>'
        '<span><span style="display:inline-block;width:12px;height:12px;background:#F59E0B;transform:rotate(45deg);margin-right:6px;vertical-align:middle;"></span>Beslutning</span>'
        '</div>'
    )
    return (
        '<div style="margin:0;padding:20px;background:#fff;font-family:Arial,sans-serif;">'
        '<h3 style="color:#1E293B;margin:0 0 8px;font-size:15px;">E2E Beslutningsflows \u2014 Todo App</h3>'
        + legend
        + '<h4 style="color:#475569;margin:0 0 6px;font-size:12px;">1. Autentificering</h4>'
        + _auth_svg()
        + '<h4 style="color:#475569;margin:14px 0 6px;font-size:12px;">2. Todo CRUD</h4>'
        + _crud_svg()
        + '<h4 style="color:#475569;margin:14px 0 6px;font-size:12px;">3. Logout</h4>'
        + _logout_svg()
        + '</div>'
    )
