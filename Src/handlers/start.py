# handlers/start.py
from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Usa /gasto para registrar un gasto. Usa /saldo para ver tu saldo mensual."
    )
