# LANCAST Meeting Intelligence 🏗️

**Agent 3** del stack LANCAST — convierte reuniones de construcción en reportes ejecutivos accionables con acuerdos, responsables, impacto financiero y draft de email de seguimiento.

## Uso rápido

```bash
# Audio desde iPhone Voice Memos
python run_meeting.py --audio reunion_pmr.m4a

# Nota rápida post-reunión (3-5 min después de salir)
python run_meeting.py --note "Reunión PMR: acordamos reducir jardín 4 a 4000m², excluir electricidad..."

# Archivo de texto con notas
python run_meeting.py --text notas_reunion.txt

# Caso de prueba PMR
python run_meeting.py --test
```

## Outputs

Cada reunión genera:
- ✅ Minuta ejecutiva con resumen
- ✅ Acuerdos con responsable, fecha límite y prioridad
- ✅ Acciones LANCAST y acciones del cliente
- ✅ Puntos abiertos con urgencia
- ✅ Impacto financiero si hay cambios de scope
- ✅ Draft de email de seguimiento al cliente
- ✅ Email HTML a gerencia@lancast.biz

## Flujo iPhone → Reporte

```
Reunión termina
    ↓
Graba con Voice Memos (iPhone)
    ↓
Comparte el .m4a por email/WhatsApp
    ↓
Sube a PythonAnywhere:
  scp reunion.m4a LANCASTHND@ssh.pythonanywhere.com:~/lancast-meeting-agent/
    ↓
python run_meeting.py --audio reunion.m4a
    ↓
Email llega a gerencia@lancast.biz en ~60 segundos
```

## Variables de entorno (.env)

```
ANTHROPIC_API_KEY=sk-ant-...
SENDGRID_API_KEY=SG....
GMAIL_ADDRESS=licitaciones@lancast.biz
ALERT_EMAIL=gerencia@lancast.biz
```

## Stack LANCAST

- ✅ **Agent 1**: Monitor HonduCompras → alerta email diaria
- ✅ **Agent 2**: Estimador de presupuesto automático
- ✅ **Agent 3**: Meeting Intelligence (este agente)
- 📋 **Agent 4**: Monitor de ejecución PMR (post-adjudicación)

---
LANCAST | Constructora Lanza Castillo S. de R.L. | Honduras
