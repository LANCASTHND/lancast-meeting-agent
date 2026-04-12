"""
run_meeting.py — LANCAST Agent 3 Runner

Uso:
  python run_meeting.py --audio reunion.m4a
  python run_meeting.py --text notas.txt
  python run_meeting.py --note "Reunión PMR: acordamos reducir jardín 4..."
  python run_meeting.py --test
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from meeting_agent import process_meeting

load_dotenv(override=True)

# ── Caso de prueba PMR ────────────────────────────────────────────────────────
PMR_TEST_NOTES = """
Reunión PMR — Revisión de Alcance
Fecha: Lunes 14 de abril 2026
Lugar: Oficinas LANCAST, Tegucigalpa
Presentes: Gerencia LANCAST, Representante Cliente PMR, Ing. Supervisión

Puntos discutidos:

1. JARDÍN 4 — El cliente solicita reducir las cantidades de Jardín 4 
   de 8,465 m² a aproximadamente 4,000 m² para ajustarse al presupuesto disponible.
   LANCAST confirma que técnicamente es viable si se mantiene mínimo 4,000 m².
   Acordado: reducir a 4,000 m².

2. INSTALACIONES ELÉCTRICAS — El cliente solicita excluir completamente 
   las instalaciones eléctricas de esta etapa. Presupuesto aproximado de 
   instalaciones eléctricas era L 227,184.
   Acordado: excluir instalaciones eléctricas de la etapa actual.
   El cliente solicitará cotización separada posteriormente.

3. CRONOGRAMA — El cliente necesita que LANCAST presente la propuesta 
   ajustada antes del viernes 18 de abril para que pueda ser aprobada 
   por la junta directiva el lunes 21.
   Acordado: LANCAST entrega propuesta revisada el jueves 17 de abril.

4. PRECIO — LANCAST indicó que el ajuste de Jardín 4 reduce el precio 
   aproximadamente en L 850,000 a L 900,000. El nuevo precio estimado 
   estaría entre L 18,200,000 y L 18,400,000 más ISV.
   Punto abierto: precio exacto pendiente de cálculo final por LANCAST.

5. PLAZO DE EJECUCIÓN — Se discutió plazo de 90 días calendario desde 
   acta de inicio. El cliente necesita confirmar si pueden dar inicio 
   antes del 1 de mayo.
   Punto abierto: fecha de inicio pendiente aprobación presupuestaria del cliente.

6. FIANZA — El cliente requiere fianza de cumplimiento del 10% del monto 
   del contrato. LANCAST confirma que puede obtenerla.

Próxima reunión: Lunes 21 de abril para revisión de propuesta ajustada 
y posible firma de contrato.
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LANCAST Agent 3 — Meeting Intelligence')
    parser.add_argument('--audio', help='Archivo de audio (.m4a, .mp3, .wav)')
    parser.add_argument('--text', help='Archivo de texto con notas o transcripción')
    parser.add_argument('--note', help='Nota rápida post-reunión (texto directo)')
    parser.add_argument('--type', default='auto', help='Tipo: PMR, Choloma, auto')
    parser.add_argument('--no-email', action='store_true', help='No enviar email')
    parser.add_argument('--test', action='store_true', help='Correr caso de prueba PMR')
    args = parser.parse_args()

    if args.test:
        print("[Agent 3] Corriendo caso de prueba PMR...")
        report = process_meeting(
            text_content=PMR_TEST_NOTES,
            meeting_type="PMR",
            send_email=not args.no_email
        )
    elif args.audio:
        report = process_meeting(
            input_path=args.audio,
            meeting_type=args.type,
            send_email=not args.no_email
        )
    elif args.text:
        report = process_meeting(
            input_path=args.text,
            meeting_type=args.type,
            send_email=not args.no_email
        )
    elif args.note:
        report = process_meeting(
            text_content=args.note,
            meeting_type=args.type,
            send_email=not args.no_email
        )
    else:
        print("ERROR: Especifica --audio, --text, --note o --test")
        print("Ejemplo: python run_meeting.py --test")
        sys.exit(1)
