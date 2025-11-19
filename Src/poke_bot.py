from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler

from handlers.start import start
from handlers.gasto import (
    gasto,
    recibir_descripcion,
    recibir_monto,
    cancelar
)
from config import TOKEN

# --- PRESUPUESTO MENSUAL ---
PRESUPUESTO = 3500

# --- ESTADOS ---
DESCRIPCION, MONTO = range(2)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("gasto", gasto)],
        states={
            DESCRIPCION: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_descripcion)],
            MONTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_monto)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)]
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("start", start))


    print("Bot corriendo…")
    app.run_polling()

if __name__ == "__main__":
    main()
