from datetime import datetime
import gspread
from telegram import Update
from telegram.ext import ContextTypes
from sheets import init_gsheet

PRESUPUESTO_MENSUAL = 3500  # puedes cambiarlo

async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Conexión a Google Sheets
        # gc = gspread.service_account(filename="Credenciales/tu_archivo.json")
        # sh = gc.open("GastosProyecto")
        # ws = sh.sheet1  # o la pestaña donde guardas los datos
        ws = init_gsheet()

        # Obtener todos los registros
        registros = ws.get_all_records()

        # Fecha actual en tu zona horaria
        mes_actual = datetime.now().month
        año_actual = datetime.now().year

        # Filtrar registros del mes y año actuales
        gastos_mes = [
            r for r in registros
            if datetime.strptime(r["fecha"], "%Y-%m-%d").month == mes_actual
            and datetime.strptime(r["fecha"], "%Y-%m-%d").year == año_actual
        ]

        # Sumar gastos
        total_mes = sum(float(r["monto"].replace("$", "").replace(",", "")) for r in gastos_mes)

        # Calcular saldo
        saldo = PRESUPUESTO_MENSUAL - total_mes

        if saldo > 0:
            mensaje = f"💰 *Presupuesto del mes*\n\nHas gastado: *${total_mes:,.2f}*\nTe queda: *${saldo:,.2f}* del presupuesto."
        else:
            mensaje = f"⚠️ *Presupuesto excedido*\n\nHas gastado: *${total_mes:,.2f}*\nTe pasaste por: *${abs(saldo):,.2f}*"

        await update.message.reply_text(mensaje, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"❌ Error al calcular el saldo: {e}")
