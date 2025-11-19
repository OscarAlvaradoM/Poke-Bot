
from telegram import Update
from datetime import datetime
from telegram.ext import ConversationHandler, ContextTypes
from sheets import init_gsheet

# --- PRESUPUESTO MENSUAL ---
PRESUPUESTO = 3500

# --- ESTADOS ---
DESCRIPCION, MONTO = range(2)

async def gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 ¿Cuál es la descripción del gasto?")
    return DESCRIPCION

async def recibir_descripcion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["descripcion"] = update.message.text
    await update.message.reply_text("💰 ¿Cuánto costó?")
    return MONTO

async def recibir_monto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    try:
        context.user_data["monto"] = float(update.message.text.replace("$", "").replace(",", ""))
    except ValueError:
        await update.message.reply_text("❌ Por favor escribe un número válido.")
        return MONTO

    sheet = init_gsheet()

    # Registrar en Sheets
    fecha = datetime.now().strftime("%Y-%m-%d")
    usuario = update.effective_user.first_name
    descripcion = context.user_data["descripcion"]
    row = [fecha, usuario, descripcion, context.user_data["monto"]]
    sheet.append_row(row)

    # Calcular total gastado en el mes
    registros = sheet.get_all_records()
    mes_actual = datetime.now().strftime("%Y-%m")

    print(registros)
    total_mes = sum(
        float(r["monto"].replace("$", "").replace(",", "")) for r in registros
        if r["fecha"].startswith(mes_actual)
    )

    restante = PRESUPUESTO - total_mes

    await update.message.reply_text(
        f"✅ Gasto registrado:\n"
        f"- {descripcion}\n"
        f"- ${context.user_data['monto']:.2f}\n\n"
        f"📊 **Este mes llevan gastado:** ${total_mes:.2f}\n"
        f"💵 **Presupuesto restante:** ${restante:.2f} de ${PRESUPUESTO:.2f}"
    )

    return ConversationHandler.END

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operación cancelada.")
    return ConversationHandler.END