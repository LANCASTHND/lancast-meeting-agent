"""
meeting_agent.py — LANCAST Agent 3: Meeting Intelligence
Procesa audio o texto de reuniones y genera:
  1. Minuta ejecutiva estructurada
  2. Acuerdos con responsables y fechas
  3. Impacto financiero en presupuesto
  4. Draft de email de seguimiento al cliente
  5. Alertas para Agent 2 si hay cambios de scope

Inputs soportados:
  - Audio (.m4a, .mp3, .wav, .ogg) — iPhone Voice Memos o cualquier grabadora
  - Texto — notas post-reunión, transcripción manual
  - Voice note rápido (3-5 min resumen post-reunión)
"""

import os
import json
import anthropic
from datetime import datetime
from dotenv import load_dotenv
from typing import Optional

load_dotenv(override=True)

# ── Project context LANCAST ───────────────────────────────────────────────────
LANCAST_CONTEXT = """
LANCAST (Constructora Lanza Castillo S. de R.L.) es una empresa constructora hondureña.
Proyectos activos principales:
- PMR (Parque Memorial La Resurrección): Proyecto de urbanización ~L 20M en etapa de modificación de alcance
- LPuNBS-MCH-001-2026 (Choloma): Suministro concreto hidráulico L 9.7M — en proceso de licitación

Vocabulario técnico hondureño de construcción:
- Pliego: términos de referencia / especificaciones técnicas
- Estimación: factura de avance de obra
- Acta de inicio: documento oficial que inicia el contrato
- Fianza: garantía de cumplimiento
- Planos: diseños estructurales o arquitectónicos
- Ítems: actividades del cuadro de cantidades
- Lempiras (L): moneda nacional
- FHIS, AMDC, PNUD, OIM: clientes institucionales típicos
- Colonia / Col.: barrio o urbanización

Personas clave en reuniones LANCAST:
- Gerencia LANCAST: tomador de decisiones principal
- Cliente PMR: contraparte que solicita modificaciones al proyecto
- Supervisión: representante técnico del cliente en sitio
"""

SYSTEM_PROMPT = f"""Eres el agente de inteligencia de reuniones de LANCAST.

Tu tarea es analizar el contenido de una reunión de construcción y generar 
outputs estructurados y accionables.

{LANCAST_CONTEXT}

INSTRUCCIONES:
1. Si el input es una transcripción o notas, analiza directamente
2. Detecta automáticamente el tipo de reunión (PMR, licitación, obra, cliente, interna)
3. Extrae SOLO lo que se dijo explícitamente — no inventes ni asumas
4. Marca con ❓ los puntos ambiguos o que requieren confirmación
5. Si se mencionan montos, extractalos con precisión
6. Detecta cambios de scope que impacten el presupuesto

FORMATO DE RESPUESTA: JSON válido únicamente.

{{
  "tipo_reunion": "PMR|Licitacion|Ejecucion|Cliente|Interna|Otro",
  "fecha": "string o null",
  "duracion_estimada": "string o null",
  "presentes": ["nombres detectados o roles"],
  "proyecto": "nombre del proyecto",
  "resumen_ejecutivo": "2-3 oraciones del resultado más importante",
  "acuerdos": [
    {{
      "descripcion": "string",
      "responsable": "LANCAST|Cliente|Ambos|Pendiente",
      "fecha_limite": "string o null",
      "prioridad": "Alta|Media|Baja"
    }}
  ],
  "puntos_abiertos": [
    {{
      "descripcion": "string",
      "requiere_decision_de": "LANCAST|Cliente|Ambos",
      "urgencia": "Alta|Media|Baja"
    }}
  ],
  "impacto_financiero": {{
    "hay_cambios": true,
    "descripcion": "string",
    "monto_estimado": "number o null",
    "tipo": "Aumento|Reduccion|Sin cambio|Por definir"
  }},
  "acciones_lancast": [
    {{
      "accion": "string",
      "responsable": "string",
      "fecha_limite": "string o null"
    }}
  ],
  "acciones_cliente": [
    {{
      "accion": "string",
      "fecha_limite": "string o null"
    }}
  ],
  "alertas": ["string"],
  "proxima_reunion": "fecha/descripcion o null",
  "draft_seguimiento": {{
    "para": "string",
    "asunto": "string",
    "cuerpo": "string"
  }}
}}"""


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe audio using Claude's vision/audio capabilities.
    Supports: .m4a (iPhone Voice Memos), .mp3, .wav, .ogg
    """
    import base64
    import mimetypes

    print(f"[Agent 3] Transcribiendo audio: {audio_path}")

    # Detect mime type
    mime_type, _ = mimetypes.guess_type(audio_path)
    if not mime_type:
        ext = os.path.splitext(audio_path)[1].lower()
        mime_map = {
            '.m4a': 'audio/mp4',
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.ogg': 'audio/ogg',
            '.mp4': 'audio/mp4',
        }
        mime_type = mime_map.get(ext, 'audio/mpeg')

    with open(audio_path, 'rb') as f:
        audio_data = base64.standard_b64encode(f.read()).decode('utf-8')

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": mime_type,
                        "data": audio_data,
                    }
                },
                {
                    "type": "text",
                    "text": """Transcribe este audio de una reunión de construcción en Honduras.
El audio puede estar en español hondureño con términos técnicos de construcción.
Transcribe TODO lo que se dice, indicando [INAUDIBLE] donde no se entienda.
Si hay múltiples hablantes, indica [HABLANTE 1], [HABLANTE 2], etc.
No interpretes — solo transcribe."""
                }
            ]
        }]
    )
    return response.content[0].text


def analyze_meeting(content: str, meeting_type: str = "auto") -> dict:
    """
    Analyze meeting content (text or transcription) and generate structured output.
    content: transcription or meeting notes
    meeting_type: "PMR", "Choloma", "auto", etc.
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    context_hint = f"\nTIPO DE REUNIÓN ESPERADO: {meeting_type}" if meeting_type != "auto" else ""

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4000,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"""Analiza esta reunión de LANCAST y genera el reporte estructurado.
{context_hint}

CONTENIDO DE LA REUNIÓN:
{content}

Genera el JSON completo con todos los campos requeridos."""
        }]
    )

    raw = response.content[0].text.strip()
    raw = raw.replace('```json', '').replace('```', '').strip()
    return json.loads(raw)


def process_meeting(
    input_path: Optional[str] = None,
    text_content: Optional[str] = None,
    meeting_type: str = "auto",
    send_email: bool = True
) -> dict:
    """
    Main function: process audio or text and generate full meeting report.
    """
    print(f"\n{'='*60}")
    print(f"[Agent 3] LANCAST Meeting Intelligence")
    print(f"{'='*60}")

    # Step 1: Get content
    if input_path:
        ext = os.path.splitext(input_path)[1].lower()
        if ext in ['.m4a', '.mp3', '.wav', '.ogg', '.mp4']:
            content = transcribe_audio(input_path)
            print(f"[Agent 3] Audio transcrito: {len(content)} caracteres")
        else:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"[Agent 3] Texto cargado: {len(content)} caracteres")
    elif text_content:
        content = text_content
        print(f"[Agent 3] Procesando texto: {len(content)} caracteres")
    else:
        raise ValueError("Necesitas proporcionar input_path o text_content")

    # Step 2: Analyze
    print(f"[Agent 3] Analizando con Claude...")
    report = analyze_meeting(content, meeting_type)

    # Step 3: Print summary
    print(f"\n[Agent 3] REPORTE:")
    print(f"  Tipo: {report.get('tipo_reunion', '')}")
    print(f"  Proyecto: {report.get('proyecto', '')}")
    print(f"  Resumen: {report.get('resumen_ejecutivo', '')}")
    print(f"  Acuerdos: {len(report.get('acuerdos', []))}")
    print(f"  Acciones LANCAST: {len(report.get('acciones_lancast', []))}")
    print(f"  Puntos abiertos: {len(report.get('puntos_abiertos', []))}")

    fin = report.get('impacto_financiero', {})
    if fin.get('hay_cambios'):
        monto = fin.get('monto_estimado')
        tipo = fin.get('tipo', '')
        print(f"  💰 Impacto financiero: {tipo} {f'L {monto:,.2f}' if monto else 'monto por definir'}")

    # Step 4: Send email
    if send_email:
        _send_report_email(report)

    # Step 5: Save JSON
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    output_file = f"reunion_{timestamp}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n[Agent 3] Reporte guardado: {output_file}")
    print(f"[Agent 3] ✅ Completado.")

    return report


def _send_report_email(report: dict) -> bool:
    """Send meeting report via SendGrid."""
    import urllib.request
    import urllib.error

    key = os.environ.get("SENDGRID_API_KEY")
    from_email = os.environ.get("GMAIL_ADDRESS")
    to_email = os.environ.get("ALERT_EMAIL", "gerencia@lancast.biz")

    if not key:
        print("[Agent 3] No SendGrid key — skip email")
        return False

    html = _build_report_html(report)
    text = _build_report_text(report)

    tipo = report.get('tipo_reunion', '')
    proyecto = report.get('proyecto', '')
    n_acuerdos = len(report.get('acuerdos', []))
    fecha = datetime.now().strftime('%d/%m/%Y')
    subject = f"🏗️ LANCAST — Reunión {tipo} {proyecto} | {n_acuerdos} acuerdos | {fecha}"

    payload = json.dumps({
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": from_email, "name": "LANCAST Meeting Intel"},
        "subject": subject,
        "content": [
            {"type": "text/plain", "value": text},
            {"type": "text/html", "value": html}
        ]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.sendgrid.com/v3/mail/send",
        data=payload,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            print(f"[Agent 3] ✅ Email enviado a {to_email} — HTTP {resp.status}")
            return True
    except urllib.error.HTTPError as e:
        print(f"[Agent 3] ❌ Error email: {e.code} — {e.read().decode()}")
        return False


def _build_report_html(report: dict) -> str:
    tipo = report.get('tipo_reunion', '')
    proyecto = report.get('proyecto', '')
    fecha = report.get('fecha') or datetime.now().strftime('%d/%m/%Y')
    resumen = report.get('resumen_ejecutivo', '')
    acuerdos = report.get('acuerdos', [])
    puntos = report.get('puntos_abiertos', [])
    acc_lancast = report.get('acciones_lancast', [])
    acc_cliente = report.get('acciones_cliente', [])
    fin = report.get('impacto_financiero', {})
    alertas = report.get('alertas', [])
    proxima = report.get('proxima_reunion')
    draft = report.get('draft_seguimiento', {})

    # Priority colors
    prio_color = {'Alta': '#ef4444', 'Media': '#f59e0b', 'Baja': '#22c55e'}
    urg_color = {'Alta': '#ef4444', 'Media': '#f59e0b', 'Baja': '#22c55e'}

    # Acuerdos rows
    acuerdos_html = ''
    for a in acuerdos:
        color = prio_color.get(a.get('prioridad', ''), '#999')
        acuerdos_html += f"""
        <tr>
          <td style="padding:8px;border:1px solid #ddd;font-size:12px;">{a.get('descripcion','')}</td>
          <td style="padding:8px;border:1px solid #ddd;font-size:12px;text-align:center;">{a.get('responsable','')}</td>
          <td style="padding:8px;border:1px solid #ddd;font-size:12px;text-align:center;">{a.get('fecha_limite','—')}</td>
          <td style="padding:8px;border:1px solid #ddd;font-size:12px;text-align:center;">
            <span style="background:{color};color:white;padding:2px 6px;border-radius:10px;font-size:10px;">{a.get('prioridad','')}</span>
          </td>
        </tr>"""

    # Acciones LANCAST
    acc_html = ''
    for a in acc_lancast:
        acc_html += f"<li style='font-size:12px;margin-bottom:4px;'><strong>{a.get('responsable','LANCAST')}</strong> — {a.get('accion','')} <span style='color:#666;'>→ {a.get('fecha_limite','Sin fecha')}</span></li>"

    # Acciones cliente
    acc_cliente_html = ''
    for a in acc_cliente:
        acc_cliente_html += f"<li style='font-size:12px;margin-bottom:4px;'>{a.get('accion','')} <span style='color:#666;'>→ {a.get('fecha_limite','Sin fecha')}</span></li>"

    # Puntos abiertos
    puntos_html = ''
    for p in puntos:
        color = urg_color.get(p.get('urgencia', ''), '#999')
        puntos_html += f"<li style='font-size:12px;margin-bottom:4px;'>❓ {p.get('descripcion','')} <span style='color:{color};font-size:11px;'>[Urgencia {p.get('urgencia','')}]</span></li>"

    # Impacto financiero
    fin_html = ''
    if fin.get('hay_cambios'):
        monto = fin.get('monto_estimado')
        tipo_fin = fin.get('tipo', '')
        color_fin = '#22c55e' if tipo_fin == 'Aumento' else '#ef4444' if tipo_fin == 'Reduccion' else '#f59e0b'
        monto_str = f"L {float(monto):,.2f}" if monto else "Monto por definir"
        fin_html = f"""
        <div style="background:#fff8e1;padding:12px;border-radius:6px;border-left:4px solid {color_fin};margin-bottom:16px;">
          <strong style="color:#1a5c2a;">💰 Impacto Financiero: {tipo_fin}</strong><br>
          <span style="font-size:13px;">{fin.get('descripcion','')}</span><br>
          <span style="font-size:15px;font-weight:bold;color:{color_fin};">{monto_str}</span>
        </div>"""

    # Alertas
    alertas_html = ''
    if alertas:
        alertas_html = '<div style="background:#fff3cd;padding:12px;border-radius:6px;border-left:4px solid #f59e0b;margin-bottom:16px;"><strong>⚠️ Alertas</strong><ul style="margin:6px 0 0 0;padding-left:18px;">'
        for a in alertas:
            alertas_html += f'<li style="font-size:12px;">{a}</li>'
        alertas_html += '</ul></div>'

    # Draft email
    draft_html = ''
    if draft.get('cuerpo'):
        draft_html = f"""
        <div style="background:#f0f4f8;padding:14px;border-radius:6px;border-left:4px solid #1a5c2a;margin-bottom:16px;">
          <strong style="color:#1a5c2a;">📧 Draft Email de Seguimiento</strong><br>
          <p style="margin:6px 0 2px 0;font-size:12px;color:#666;"><strong>Para:</strong> {draft.get('para','')}</p>
          <p style="margin:0 0 8px 0;font-size:12px;color:#666;"><strong>Asunto:</strong> {draft.get('asunto','')}</p>
          <div style="background:white;padding:10px;border-radius:4px;font-size:12px;white-space:pre-wrap;">{draft.get('cuerpo','')}</div>
        </div>"""

    presentes = ', '.join(report.get('presentes', []))

    return f"""<html>
<body style="font-family:Arial,sans-serif;max-width:750px;margin:0 auto;color:#333;">

<div style="background:#1a5c2a;padding:20px;border-radius:8px 8px 0 0;">
  <h2 style="color:white;margin:0;">🏗️ LANCAST — Reporte de Reunión</h2>
  <p style="color:#a7d7b0;margin:4px 0 0 0;font-size:13px;">{fecha} | {tipo} | {proyecto}</p>
</div>

<div style="padding:20px;background:#fafafa;border:1px solid #e0e0e0;border-radius:0 0 8px 8px;">

  <div style="background:#e8f5e9;padding:12px;border-radius:6px;margin-bottom:16px;">
    <strong style="color:#1a5c2a;">Resumen Ejecutivo</strong>
    <p style="margin:6px 0 0 0;font-size:13px;">{resumen}</p>
    {f'<p style="margin:4px 0 0 0;font-size:12px;color:#666;">Presentes: {presentes}</p>' if presentes else ''}
    {f'<p style="margin:4px 0 0 0;font-size:12px;color:#1a5c2a;"><strong>Próxima reunión: {proxima}</strong></p>' if proxima else ''}
  </div>

  {fin_html}
  {alertas_html}

  <h4 style="color:#1a5c2a;border-bottom:2px solid #8dc641;padding-bottom:4px;">✅ Acuerdos ({len(acuerdos)})</h4>
  {f'''<table style="width:100%;border-collapse:collapse;margin-bottom:16px;">
    <thead><tr style="background:#1a5c2a;color:white;">
      <th style="padding:8px;font-size:12px;text-align:left;">Acuerdo</th>
      <th style="padding:8px;font-size:12px;">Responsable</th>
      <th style="padding:8px;font-size:12px;">Fecha límite</th>
      <th style="padding:8px;font-size:12px;">Prioridad</th>
    </tr></thead>
    <tbody>{acuerdos_html}</tbody>
  </table>''' if acuerdos else '<p style="color:#999;font-size:12px;">No se registraron acuerdos formales.</p>'}

  <h4 style="color:#1a5c2a;border-bottom:2px solid #8dc641;padding-bottom:4px;">📋 Acciones LANCAST</h4>
  {f'<ul style="margin:0 0 16px 0;padding-left:20px;">{acc_html}</ul>' if acc_html else '<p style="color:#999;font-size:12px;">Sin acciones pendientes.</p>'}

  {f'<h4 style="color:#1a5c2a;border-bottom:2px solid #8dc641;padding-bottom:4px;">📋 Acciones del Cliente</h4><ul style="margin:0 0 16px 0;padding-left:20px;">{acc_cliente_html}</ul>' if acc_cliente_html else ''}

  {f'<h4 style="color:#1a5c2a;border-bottom:2px solid #8dc641;padding-bottom:4px;">❓ Puntos Abiertos ({len(puntos)})</h4><ul style="margin:0 0 16px 0;padding-left:20px;">{puntos_html}</ul>' if puntos_html else ''}

  {draft_html}

  <p style="color:#999;font-size:11px;border-top:1px solid #eee;padding-top:10px;margin:0;">
    LANCAST Agent 3 Meeting Intelligence | Powered by Claude AI<br>
    Reporte generado automáticamente — verificar acuerdos con los presentes.
  </p>
</div>
</body></html>"""


def _build_report_text(report: dict) -> str:
    lines = [
        f"LANCAST — REPORTE DE REUNIÓN",
        f"{'='*50}",
        f"Tipo: {report.get('tipo_reunion','')} | Proyecto: {report.get('proyecto','')}",
        f"Fecha: {report.get('fecha') or datetime.now().strftime('%d/%m/%Y')}",
        f"Presentes: {', '.join(report.get('presentes',[]))}",
        f"",
        f"RESUMEN: {report.get('resumen_ejecutivo','')}",
        f"",
    ]
    if report.get('acuerdos'):
        lines.append("ACUERDOS:")
        for a in report['acuerdos']:
            lines.append(f"  ✅ {a.get('descripcion','')} → {a.get('responsable','')} | {a.get('fecha_limite','Sin fecha')} | {a.get('prioridad','')}")
    if report.get('acciones_lancast'):
        lines.append("\nACCIONES LANCAST:")
        for a in report['acciones_lancast']:
            lines.append(f"  • {a.get('accion','')} → {a.get('fecha_limite','Sin fecha')}")
    if report.get('puntos_abiertos'):
        lines.append("\nPUNTOS ABIERTOS:")
        for p in report['puntos_abiertos']:
            lines.append(f"  ❓ {p.get('descripcion','')} [{p.get('urgencia','')}]")
    fin = report.get('impacto_financiero', {})
    if fin.get('hay_cambios'):
        monto = fin.get('monto_estimado')
        lines.append(f"\nIMPACTO FINANCIERO: {fin.get('tipo','')} — {f'L {float(monto):,.2f}' if monto else 'Por definir'}")
    if report.get('alertas'):
        lines.append("\nALERTAS:")
        for a in report['alertas']:
            lines.append(f"  ⚠️  {a}")
    if report.get('proxima_reunion'):
        lines.append(f"\nPRÓXIMA REUNIÓN: {report['proxima_reunion']}")
    return '\n'.join(lines)
