def _truncate(text: str, max_len: int = 18) -> str:
    return text[:max_len] + "\u2026" if len(text) > max_len else text


def _build_diagram(
    title: str,
    box1_line1: str,
    box1_line2: str,
    box2_subtitle: str,
    arrow1_method: str,
    arrow1_status: str,
    arrow2_label: str,
    box4_subtitle: str,
    pid: str
) -> str:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="200">
  <defs>
    <linearGradient id="{pid}bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#F8FAFC;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#F1F5F9;stop-opacity:1"/>
    </linearGradient>
    <linearGradient id="{pid}yellow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FCD34D;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#F59E0B;stop-opacity:1"/>
    </linearGradient>
    <linearGradient id="{pid}blue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#60A5FA;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#3B82F6;stop-opacity:1"/>
    </linearGradient>
    <linearGradient id="{pid}green" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#34D399;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#10B981;stop-opacity:1"/>
    </linearGradient>
    <linearGradient id="{pid}purple" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#A78BFA;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#8B5CF6;stop-opacity:1"/>
    </linearGradient>
    <marker id="{pid}arrow" markerWidth="8" markerHeight="6" refX="7" refY="3"
            orient="auto" markerUnits="userSpaceOnUse">
      <polygon points="0 0, 8 3, 0 6" fill="#94A3B8"/>
    </marker>
  </defs>

  <!-- Background -->
  <rect width="800" height="200" fill="url(#{pid}bg)" rx="12"/>
  <rect width="800" height="200" fill="none" stroke="#E2E8F0" stroke-width="1.5" rx="12"/>

  <!-- Title -->
  <text x="400" y="30" text-anchor="middle" font-family="Arial, sans-serif"
        font-size="14" font-weight="bold" fill="#1E293B">{title}</text>

  <!-- Box 1 shadow -->
  <rect x="17" y="57" width="155" height="80" rx="10" fill="#000000" fill-opacity="0.08"/>
  <!-- Box 1: Test Data (yellow) -->
  <rect x="15" y="54" width="155" height="80" rx="10" fill="url(#{pid}yellow)" stroke="#D97706" stroke-width="1.5"/>
  <text x="92" y="77" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" fill="white">&#128203;</text>
  <text x="92" y="92" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="white">Test Data</text>
  <text x="92" y="106" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="rgba(255,255,255,0.95)">{box1_line1}</text>
  <text x="92" y="119" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="rgba(255,255,255,0.85)">{box1_line2}</text>

  <!-- Arrow 1 -->
  <line x1="172" y1="94" x2="215" y2="94" stroke="#94A3B8" stroke-width="2"
        stroke-dasharray="6,4" marker-end="url(#{pid}arrow)">
    <animate attributeName="stroke-dashoffset" from="10" to="0" dur="0.7s" repeatCount="indefinite"/>
  </line>
  <text x="194" y="87" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" font-weight="bold" fill="#475569">{arrow1_method}</text>
  <text x="194" y="108" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#10B981">{arrow1_status}</text>

  <!-- Box 2 shadow -->
  <rect x="222" y="57" width="155" height="80" rx="10" fill="#000000" fill-opacity="0.08"/>
  <!-- Box 2: Todo API (blue) -->
  <rect x="220" y="54" width="155" height="80" rx="10" fill="url(#{pid}blue)" stroke="#2563EB" stroke-width="1.5"/>
  <text x="297" y="81" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" fill="white">&#127760;</text>
  <text x="297" y="100" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="white">Todo API</text>
  <text x="297" y="116" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="rgba(255,255,255,0.9)">{box2_subtitle}</text>

  <!-- Arrow 2 -->
  <line x1="377" y1="94" x2="420" y2="94" stroke="#94A3B8" stroke-width="2"
        stroke-dasharray="6,4" marker-end="url(#{pid}arrow)">
    <animate attributeName="stroke-dashoffset" from="10" to="0" dur="0.7s" begin="0.25s" repeatCount="indefinite"/>
  </line>
  <text x="399" y="87" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" font-weight="bold" fill="#475569">{arrow2_label}</text>

  <!-- Box 3 shadow -->
  <rect x="427" y="57" width="155" height="80" rx="10" fill="#000000" fill-opacity="0.08"/>
  <!-- Box 3: PostgreSQL (green) -->
  <rect x="425" y="54" width="155" height="80" rx="10" fill="url(#{pid}green)" stroke="#059669" stroke-width="1.5"/>
  <text x="502" y="81" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" fill="white">&#128452;</text>
  <text x="502" y="100" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="white">PostgreSQL</text>
  <text x="502" y="116" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="rgba(255,255,255,0.9)">todos tabel</text>

  <!-- Arrow 3 -->
  <line x1="582" y1="94" x2="625" y2="94" stroke="#94A3B8" stroke-width="2"
        stroke-dasharray="6,4" marker-end="url(#{pid}arrow)">
    <animate attributeName="stroke-dashoffset" from="10" to="0" dur="0.7s" begin="0.5s" repeatCount="indefinite"/>
  </line>
  <text x="604" y="87" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" font-weight="bold" fill="#475569">Query</text>

  <!-- Box 4 shadow -->
  <rect x="632" y="57" width="153" height="80" rx="10" fill="#000000" fill-opacity="0.08"/>
  <!-- Box 4: Verifikation (purple) -->
  <rect x="630" y="54" width="153" height="80" rx="10" fill="url(#{pid}purple)" stroke="#7C3AED" stroke-width="1.5"/>
  <text x="706" y="81" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" fill="white">&#9989;</text>
  <text x="706" y="100" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="white">Verifikation</text>
  <text x="706" y="116" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="rgba(255,255,255,0.9)">{box4_subtitle}</text>

  <!-- Step labels -->
  <text x="92" y="156" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#94A3B8">&#9312; Test data</text>
  <text x="297" y="156" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#94A3B8">&#9313; API kald</text>
  <text x="502" y="156" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#94A3B8">&#9314; Persistering</text>
  <text x="706" y="156" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#94A3B8">&#9315; DB assertion</text>
</svg>"""
    return f'<html><body style="margin:0;padding:20px;background:#fff;">{svg}</body></html>'


def post_diagram(title: str, completed: bool) -> str:
    label = _truncate(title)
    return _build_diagram(
        title="POST /todos \u2014 Opret Todo Flow",
        box1_line1=f'"{label}"',
        box1_line2=f"completed: {completed}",
        box2_subtitle="POST /todos",
        arrow1_method="POST",
        arrow1_status="HTTP 201 \u2713",
        arrow2_label="INSERT",
        box4_subtitle="7 assertions",
        pid="p_"
    )


def put_diagram(title: str, completed) -> str:
    label = _truncate(title)
    return _build_diagram(
        title="PUT /todos/{{id}} \u2014 Opdater Todo Flow",
        box1_line1=f'"{label}"',
        box1_line2=f"completed: {completed}",
        box2_subtitle="PUT /todos/{{id}}",
        arrow1_method="PUT",
        arrow1_status="HTTP 200 \u2713",
        arrow2_label="UPDATE",
        box4_subtitle="7 assertions",
        pid="pu_"
    )


def delete_diagram(todo_id: int) -> str:
    return _build_diagram(
        title="DELETE /todos/{{id}} \u2014 Slet Todo Flow",
        box1_line1=f"id: {todo_id}",
        box1_line2="",
        box2_subtitle="DELETE /todos/{{id}}",
        arrow1_method="DELETE",
        arrow1_status="HTTP 200 \u2713",
        arrow2_label="DELETE",
        box4_subtitle="is None, count=0",
        pid="d_"
    )


def _build_negative_diagram(
    title: str,
    box1_line1: str,
    box2_subtitle: str,
    arrow1_method: str,
    http_error: str,
    error_subtitle: str,
    pid: str
) -> str:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="200">
  <defs>
    <linearGradient id="{pid}bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#FEF2F2;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#FEE2E2;stop-opacity:1"/>
    </linearGradient>
    <linearGradient id="{pid}orange" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FB923C;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#F97316;stop-opacity:1"/>
    </linearGradient>
    <linearGradient id="{pid}gray" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#9CA3AF;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#6B7280;stop-opacity:1"/>
    </linearGradient>
    <linearGradient id="{pid}red" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#F87171;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#EF4444;stop-opacity:1"/>
    </linearGradient>
    <marker id="{pid}arrow" markerWidth="8" markerHeight="6" refX="7" refY="3"
            orient="auto" markerUnits="userSpaceOnUse">
      <polygon points="0 0, 8 3, 0 6" fill="#94A3B8"/>
    </marker>
    <marker id="{pid}redarrow" markerWidth="8" markerHeight="6" refX="7" refY="3"
            orient="auto" markerUnits="userSpaceOnUse">
      <polygon points="0 0, 8 3, 0 6" fill="#EF4444"/>
    </marker>
  </defs>

  <!-- Background (reddish tint) -->
  <rect width="800" height="200" fill="url(#{pid}bg)" rx="12"/>
  <rect width="800" height="200" fill="none" stroke="#FECACA" stroke-width="1.5" rx="12"/>

  <!-- NEGATIV TEST badge -->
  <rect x="296" y="7" width="208" height="22" rx="5" fill="#EF4444" fill-opacity="0.12" stroke="#EF4444" stroke-width="1.5"/>
  <text x="400" y="22" text-anchor="middle" font-family="Arial, sans-serif"
        font-size="10" font-weight="bold" fill="#DC2626">&#9888; NEGATIV TEST &#9888;</text>

  <!-- Title -->
  <text x="400" y="46" text-anchor="middle" font-family="Arial, sans-serif"
        font-size="13" font-weight="bold" fill="#1E293B">{title}</text>

  <!-- Box 1 shadow -->
  <rect x="82" y="62" width="170" height="80" rx="10" fill="#000000" fill-opacity="0.08"/>
  <!-- Box 1: Test Data (orange) -->
  <rect x="80" y="59" width="170" height="80" rx="10" fill="url(#{pid}orange)" stroke="#EA580C" stroke-width="1.5"/>
  <text x="165" y="82" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" fill="white">&#128203;</text>
  <text x="165" y="97" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="white">Test Data</text>
  <text x="165" y="112" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="rgba(255,255,255,0.95)">{box1_line1}</text>

  <!-- Arrow 1 (gray) -->
  <line x1="252" y1="99" x2="295" y2="99" stroke="#94A3B8" stroke-width="2"
        stroke-dasharray="6,4" marker-end="url(#{pid}arrow)">
    <animate attributeName="stroke-dashoffset" from="10" to="0" dur="0.7s" repeatCount="indefinite"/>
  </line>
  <text x="274" y="92" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" font-weight="bold" fill="#475569">{arrow1_method}</text>

  <!-- Box 2 shadow -->
  <rect x="302" y="62" width="170" height="80" rx="10" fill="#000000" fill-opacity="0.08"/>
  <!-- Box 2: Todo API (gray) -->
  <rect x="300" y="59" width="170" height="80" rx="10" fill="url(#{pid}gray)" stroke="#4B5563" stroke-width="1.5"/>
  <text x="385" y="82" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" fill="white">&#127760;</text>
  <text x="385" y="100" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="white">Todo API</text>
  <text x="385" y="116" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="rgba(255,255,255,0.9)">{box2_subtitle}</text>

  <!-- Arrow 2 (red — fejlsti) -->
  <line x1="472" y1="99" x2="515" y2="99" stroke="#EF4444" stroke-width="2"
        stroke-dasharray="6,4" marker-end="url(#{pid}redarrow)">
    <animate attributeName="stroke-dashoffset" from="10" to="0" dur="0.7s" begin="0.25s" repeatCount="indefinite"/>
  </line>
  <text x="494" y="92" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" font-weight="bold" fill="#DC2626">{http_error}</text>

  <!-- Box 3 shadow -->
  <rect x="522" y="62" width="170" height="80" rx="10" fill="#000000" fill-opacity="0.08"/>
  <!-- Box 3: HTTP Error (red) -->
  <rect x="520" y="59" width="170" height="80" rx="10" fill="url(#{pid}red)" stroke="#DC2626" stroke-width="2"/>
  <text x="605" y="82" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" fill="white">&#10060;</text>
  <text x="605" y="100" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="white">{http_error}</text>
  <text x="605" y="116" text-anchor="middle" font-family="Arial, sans-serif" font-size="10" fill="rgba(255,255,255,0.9)">{error_subtitle}</text>

  <!-- Step labels -->
  <text x="165" y="161" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#94A3B8">&#9312; Test data</text>
  <text x="385" y="161" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#94A3B8">&#9313; API kald</text>
  <text x="605" y="161" text-anchor="middle" font-family="Arial, sans-serif" font-size="9" fill="#94A3B8">&#9314; Fejl respons</text>
</svg>"""
    return f'<html><body style="margin:0;padding:20px;background:#fff;">{svg}</body></html>'


def negative_post_diagram(missing_field: str) -> str:
    return _build_negative_diagram(
        title="POST /todos \u2014 Manglende p\u00e5kr\u00e6vet felt",
        box1_line1=f"mangler: {missing_field}",
        box2_subtitle="validerer input",
        arrow1_method="POST",
        http_error="HTTP 422 \u2717",
        error_subtitle="Unprocessable Entity",
        pid="np_"
    )


def negative_put_diagram(todo_id: int) -> str:
    return _build_negative_diagram(
        title="PUT /todos/{{id}} \u2014 Todo ikke fundet",
        box1_line1=f"id: {todo_id}",
        box2_subtitle="finder ikke todo",
        arrow1_method="PUT",
        http_error="HTTP 404 \u2717",
        error_subtitle="Not Found",
        pid="npu_"
    )


def negative_delete_diagram(todo_id: int) -> str:
    return _build_negative_diagram(
        title="DELETE /todos/{{id}} \u2014 Todo ikke fundet",
        box1_line1=f"id: {todo_id}",
        box2_subtitle="finder ikke todo",
        arrow1_method="DELETE",
        http_error="HTTP 404 \u2717",
        error_subtitle="Not Found",
        pid="nd_"
    )


def get_all_diagram() -> str:
    return _build_diagram(
        title="GET /todos \u2014 Hent Alle Todos Flow",
        box1_line1="ingen filtre",
        box1_line2="",
        box2_subtitle="GET /todos",
        arrow1_method="GET",
        arrow1_status="HTTP 200 \u2713",
        arrow2_label="SELECT ALL",
        box4_subtitle="liste > 0",
        pid="ga_"
    )


def get_single_diagram(todo_id: int) -> str:
    return _build_diagram(
        title="GET /todos/{{id}} \u2014 Hent Enkelt Todo Flow",
        box1_line1=f"id: {todo_id}",
        box1_line2="",
        box2_subtitle="GET /todos/{{id}}",
        arrow1_method="GET",
        arrow1_status="HTTP 200 \u2713",
        arrow2_label="SELECT",
        box4_subtitle="id matcher",
        pid="gs_"
    )


def get_validate_fields_diagram(todo_id: int) -> str:
    return _build_diagram(
        title="GET /todos/{{id}} \u2014 Feltvalidering Flow",
        box1_line1=f"id: {todo_id}",
        box1_line2="",
        box2_subtitle="GET /todos/{{id}}",
        arrow1_method="GET",
        arrow1_status="HTTP 200 \u2713",
        arrow2_label="SELECT",
        box4_subtitle="id,title,completed",
        pid="gv_"
    )


def negative_get_diagram(todo_id, expected_status: int) -> str:
    box2_subtitle = "validerer input" if expected_status == 422 else "finder ikke todo"
    error_subtitle = "Unprocessable Entity" if expected_status == 422 else "Not Found"
    return _build_negative_diagram(
        title="GET /todos/{{id}} \u2014 Negativ Test",
        box1_line1=f"id: {todo_id}",
        box2_subtitle=box2_subtitle,
        arrow1_method="GET",
        http_error=f"HTTP {expected_status} \u2717",
        error_subtitle=error_subtitle,
        pid="ng_"
    )
