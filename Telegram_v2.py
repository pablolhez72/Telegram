# Telegram + ChatGPT Integration Bot    

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from ChatGpt import ConsultandoChatGPT  # Importa la función de consulta a ChatGPT desde tu archivo ChatGpt.py

#pip install python-telegram-bot --upgrade
#pip install --upgrade pip  

#cada vez que se hace un cambio hay que reiniciar el bot, 
# para evitar esto se puede instalar la liberia Hupper que monitorea los cambios en la aplicación
#pip install hupper 
#hupper -m Telegram_v2.py        EJECUTAR DESDE LA TERMINAL
#hupper -m Telegram_v2.py --reload  EJECUTAR DESDE LA TERMINAL

#Variables de entorno
#pip install python-dotenv      
import os
from dotenv import load_dotenv
load_dotenv() #carga variable entorno desde el archivo .env
token_chatgpt = os.getenv("OPENAI_API_KEY")
token_telegram = os.getenv("TELEGRAM_API_KEY")
#print(f"Clave API de OpenAI: {token_chatgpt}")
#print(f"Clave API de Telegram: {token_telegram}")



##########################################
async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello World!")

async def start(update: Update, context):
    """Envía un mensaje de bienvenida y el menú principal."""
    keyboard = [
        [InlineKeyboardButton("Pedir información", callback_data='pedir_informacion')],
        [InlineKeyboardButton("Hacer consulta", callback_data='hacer_consulta')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "¡Hola! Soy tu asistente de Telegram. ¿En qué puedo ayudarte hoy?",
        reply_markup=reply_markup
    )

async def menu_principal(update: Update, context):
    """Muestra el menú principal."""
    keyboard = [
        [InlineKeyboardButton("Pedir información", callback_data='pedir_informacion')],
        [InlineKeyboardButton("Hacer consulta", callback_data='hacer_consulta')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        "Aquí tienes el menú principal de nuevo:",
        reply_markup=reply_markup
    )

async def pedir_informacion_menu(update: Update, context):
    """Muestra el submenú para pedir información."""
    keyboard = [
        [InlineKeyboardButton("Horarios de atención", callback_data='info_horarios')],
        [InlineKeyboardButton("Productos y servicios", callback_data='info_productos')],
        [InlineKeyboardButton("Estado de mi pedido", callback_data='info_pedido')],
        [InlineKeyboardButton("Volver al menú principal", callback_data='menu_principal')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text(
        "¡Excelente! ¿Sobre qué tema te gustaría pedir información?",
        reply_markup=reply_markup
    )

async def hacer_consulta_menu(update: Update, context):
    """Indica al usuario que ingrese su consulta."""
    await update.callback_query.message.edit_text(
        "¿Qué tipo de consulta quieres hacer? Describe tu pregunta o el problema que tienes."
        "\n\n*Puedes escribir tu consulta directamente.*"
        "\n\nPara volver al menú principal, escribe /start" # Se añade una instrucción para volver
    )
    # Establecer un "estado" para saber que estamos esperando una consulta
    context.user_data['estado'] = 'esperando_consulta'


async def manejar_mensajes(update: Update, context):
    """Maneja los mensajes de texto del usuario, especialmente si está haciendo una consulta."""
    if 'estado' in context.user_data and context.user_data['estado'] == 'esperando_consulta':
        user_text = update.message.text
        # Aquí es donde integrarías tu lógica para procesar la consulta del usuario
        # Por simplicidad, aquí solo la repetimos.
        await update.message.reply_text(f"Recibí tu consulta: '{user_text}'. Un momento, por favor, estoy procesándola...")
        await update.message.reply_text("stamos consultando...")
        await update.message.reply_text("https://platform.openai.com/settings/organization/usage")


        Respuesta_GPT=ConsultandoChatGPT(user_text)
        await update.message.reply_text(f"Respuesta: '{Respuesta_GPT}'.")
      

        # Limpiar el estado después de manejar la consulta
        del context.user_data['estado']

        # Opcional: mostrar el menú principal de nuevo después de la consulta
        keyboard = [
            [InlineKeyboardButton("Pedir información", callback_data='pedir_informacion')],
            [InlineKeyboardButton("Hacer consulta", callback_data='hacer_consulta')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "¿Hay algo más en lo que pueda ayudarte?",
            reply_markup=reply_markup
        )
    else:
        # Mensaje por defecto si no se reconoce el comando o la intención
        await update.message.reply_text("Lo siento, no entendí tu respuesta. Por favor, elige una opción del menú o usa /start para ver el menú principal.")


# --- Funciones de información específica ---

async def mostrar_info(update: Update, context, info_type):
    """Envía la información específica según el tipo solicitado."""
    query = update.callback_query
    await query.answer() # Importante para que el botón deje de girar

    messages = {
        'info_horarios': "Nuestros horarios de atención son de Lunes a Viernes de 9:00 a 18:00 hs.",
        'info_productos': "Ofrecemos una amplia gama de productos y servicios, incluyendo internet de alta velocidad, telefonía y televisión digital.",
        'info_pedido': "Para consultar el estado de tu pedido, por favor, proporciona tu número de orden o DNI."
    }
    await query.message.edit_text(messages.get(info_type, "Información no disponible."))

    # Volver al menú de pedir información después de mostrar la info
    keyboard = [
        [InlineKeyboardButton("Horarios de atención", callback_data='info_horarios')],
        [InlineKeyboardButton("Productos y servicios", callback_data='info_productos')],
        [InlineKeyboardButton("Estado de mi pedido", callback_data='info_pedido')],
        [InlineKeyboardButton("Volver al menú principal", callback_data='menu_principal')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "¿Hay algo más sobre lo que quieras información?",
        reply_markup=reply_markup
    )
##########################################

application = ApplicationBuilder().token(token_telegram).build()

# Handlers para comandos
application.add_handler(CommandHandler("start", start))

# Handlers para botones (CallbackQueryHandler)
application.add_handler(CallbackQueryHandler(pedir_informacion_menu, pattern='^pedir_informacion$'))
application.add_handler(CallbackQueryHandler(hacer_consulta_menu, pattern='^hacer_consulta$'))
application.add_handler(CallbackQueryHandler(menu_principal, pattern='^menu_principal$'))

application.add_handler(CallbackQueryHandler(lambda update, context: mostrar_info(update, context, 'info_horarios'), pattern='^info_horarios$'))
application.add_handler(CallbackQueryHandler(lambda update, context: mostrar_info(update, context, 'info_productos'), pattern='^info_productos$'))
application.add_handler(CallbackQueryHandler(lambda update, context: mostrar_info(update, context, 'info_pedido'), pattern='^info_pedido$'))

# Handler para mensajes de texto (cuando esperamos una consulta)
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensajes))

# Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
application.run_polling(allowed_updates=Update.ALL_TYPES)