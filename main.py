import os
import re
import matplotlib.pyplot as plt
import sqlite3
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.request import HTTPXRequest
from db import init_db, guardar_gasto
from io import BytesIO
from datetime import datetime



# Cargar token del bot desde archivo .env
load_dotenv()
init_db()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# --- FUNCIONES ---

def extraer_datos(texto):
    texto = texto.strip()

    # Buscar el primer número como monto
    match = re.search(r"(\d+(?:[.,]\d{1,2})?)", texto)
    if not match:
        return None, None

    monto = match.group(1).replace(",", ".")

    # El nombre será todo el texto antes del número
    partes = texto[:match.start()].strip()
    supermercado = partes.lower() if partes else "Desconocido"

    return supermercado, monto


# --- HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "👋 ¡Hola! Soy tu asistente para registrar y analizar tus gastos en supermercados.\n\n"
            "📌 ¿Cómo usarme?\n"
            "Simplemente enviame un mensaje con el formato:\n"
            "`NombreSupermercado Monto`\n"
            "Ejemplo:\n"
            "`coto 15879.50`\n\n"
            "📊 Comandos disponibles:\n"
            "/start - Mostrar este mensaje de bienvenida\n"
            "/resumen - Ver un gráfico de tus gastos acumulados\n\n"
            "💡 Consejo: Siempre usá el nombre del comercio seguido del monto separado por un espacio.\n"
            "¡Podés ingresar cualquier tipo de local o comercio!",
            parse_mode="Markdown"
        )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text or not message.from_user:
        return  # Ignoramos si no hay mensaje, texto o usuario

    texto = message.text.strip()
    supermercado, monto = extraer_datos(texto)

    if not supermercado or not monto:
        await message.reply_text(
            "❌ No pude interpretar el mensaje. Usá el formato:\n`NombreSupermercado Monto`",
            parse_mode="Markdown"
        )
        return

    try:
        guardar_gasto(str(message.from_user.id), supermercado, float(monto))
    except Exception as e:
        await message.reply_text(f"⚠️ Ocurrió un error al guardar el gasto:\n`{e}`", parse_mode="Markdown")
        return

    await message.reply_text(
    f"🧾 Gasto registrado:\nSupermercado: {supermercado.capitalize()}\nMonto: ${monto}"
    )

async def grafico_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.from_user:
        return

    user_id = str(message.from_user.id)

    # Consultar los gastos del usuario
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT supermercado, COUNT(*), SUM(monto)
        FROM gastos
        WHERE usuario_id = ?
        GROUP BY supermercado
    """, (user_id,))
    datos = cursor.fetchall()
    conn.close()

    if not datos:
        await message.reply_text("ℹ️ Aún no registraste gastos.")
        return

    supermercados = [row[0] for row in datos]
    visitas = [row[1] for row in datos]
    montos = [row[2] for row in datos]

    # Crear gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(supermercados, montos, color='skyblue')

    # Ajustar el límite superior del eje Y para que no se corte el texto
    max_monto = max(montos)
    ax.set_ylim(top=max_monto * 1.25)  # 25% más alto que el valor máximo

    # Agregar etiquetas con monto y visitas arriba de cada barra
    for bar, monto, visita in zip(bars, montos, visitas):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max_monto * 0.02,  # pequeño margen arriba
            f"${monto:,.2f}\nVisitas: {visita}",
            ha='center', va='bottom', fontsize=10, fontweight='bold'
        )

    ax.set_ylabel("Total gastado ($)")
    ax.set_xlabel("Supermercado")
    ax.set_title("Resumen de gastos por supermercado")
    plt.xticks(rotation=0)
    fig.tight_layout()

    # Enviar imagen al usuario
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    await message.reply_photo(photo=buffer, caption="📊 Tu resumen de gastos.")


# --- MAIN ---

def main():
    request = HTTPXRequest(connect_timeout=15.0, read_timeout=15.0)
    app = ApplicationBuilder().token(TOKEN).request(request).build()  # type: ignore

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CommandHandler("resumen", grafico_handler))


    print("Bot corriendo...")
    app.run_polling()

if __name__ == "__main__":
    main()
