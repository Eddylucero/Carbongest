import logging
import os
import django
import re

# ¡Importa sync_to_async!
from asgiref.sync import sync_to_async

# Configura Django para poder acceder a tus modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarbonGest.settings') # Asegúrate que 'CarbonGest' sea el nombre de tu proyecto Django
django.setup()

from django.conf import settings
from Aplicaciones.Proveedores.models import Proveedor # Asegúrate que 'Aplicaciones.Proveedores' sea la ruta correcta a tu app

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja el comando /start y pide el número de teléfono."""
    user = update.effective_user
    await update.message.reply_html(
        f"¡Hola {user.full_name}! 👋 Soy tu bot de pedidos de CarbonGest.\n"
        "Para que pueda enviarte pedidos, por favor, **envíame tu número de teléfono**.\n"
        "Puedes compartirlo directamente desde Telegram (icono del clip -> Contacto), o escribirlo (ej: +593981234567)."
    )
    logger.info(f"Comando /start recibido de {user.full_name} ({user.id})")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja los mensajes de texto y contactos para vincular el chat_id."""
    chat_id = update.effective_chat.id
    phone_number = None

    if update.message.contact and update.message.contact.user_id == update.effective_user.id:
        phone_number = update.message.contact.phone_number
        logger.info(f"Contacto compartido: {phone_number} por {update.effective_user.full_name}")
    elif update.message.text:
        match = re.search(r'^\+?\d{9,15}$', update.message.text.strip())
        if match:
            phone_number = match.group(0)
            logger.info(f"Número de teléfono en texto: {phone_number} por {update.effective_user.full_name}")
        
    if not phone_number:
        await update.message.reply_text(
            "Por favor, comparte tu número de teléfono para vincular tu cuenta. "
            "Asegúrate de incluir el código de país (ej: +593...) o usar la opción 'Compartir Contacto'."
        )
        return

    cleaned_phone_number = re.sub(r'[^0-9]', '', phone_number)

    try:
        # ¡IMPORTANTE! Envuelve la consulta al ORM con sync_to_async
        proveedor = await sync_to_async(
            Proveedor.objects.filter(telefono__endswith=cleaned_phone_number[-9:]).first
        )()

        if proveedor:
            proveedor.telegram_chat_id = str(chat_id)
            # ¡También envuelve el guardado con sync_to_async!
            await sync_to_async(proveedor.save)()
            await update.message.reply_text(
                f"¡Gracias {proveedor.nombre}! Hemos vinculado tu cuenta de Telegram.\n"
                "Ahora recibirás los pedidos por aquí. 🎉"
            )
            logger.info(f"Proveedor {proveedor.nombre} vinculado con chat_id: {chat_id}")
        else:
            await update.message.reply_text(
                "Lo siento, no pude encontrar un proveedor asociado a este número. "
                "Asegúrate de que tu número esté registrado correctamente en nuestro sistema y vuelve a intentarlo."
            )
            logger.warning(f"Número no encontrado: {phone_number} (chat_id: {chat_id})")
    except Exception as e:
        logger.error(f"Error al vincular el proveedor con chat_id {chat_id}: {e}", exc_info=True)
        await update.message.reply_text("Ocurrió un error al vincular tu cuenta. Por favor, inténtalo de nuevo más tarde.")

def main() -> None:
    """Inicia el bot."""
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND | filters.CONTACT, handle_message))

    logger.info("Bot de Telegram iniciado. Escuchando actualizaciones...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()