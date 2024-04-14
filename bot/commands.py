import asyncio
from bot.service import (
    generate_pvp_1500_pokemon_messages,
    fetch_pvp_1500_pokemon_data,
    coordinates_waiting_time
)
from telegram import Update
from telegram.ext import ContextTypes
from settings import config
import telegram
from typing import List

# ID del grupo al que se enviarán las coordenadas
GRUPO_COORDENADAS_ID = int(config.CHAT_ID)

# Lista de usuarios permitidos para activar los comandos
USUARIOS_PERMITIDOS = [int(config.SUPPORT), int(config.ADMIN)]

PERIOD = int(config.PERIOD)


async def send_coordinates(
    context: ContextTypes.DEFAULT_TYPE, total_text: List[str]):
    if total_text:
        messages_number = len(total_text)
        message_delay = 3 if len(total_text) > 18 else 2
        plural_letter = "" if messages_number == 1 else "s"
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            text=f"Enviando {messages_number} coordenada{plural_letter} PVP...",
        )
        for text in total_text:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID, text=text, parse_mode="MarkdownV2"
            )
            await asyncio.sleep(message_delay)
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            text=f"Se terminó de enviar la{plural_letter} coordenada{plural_letter} PVP. Dentro de {PERIOD} minutos se enviarán más.",
        )
    else:
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            text=f"No se encontraron coordenadas. Dentro de {PERIOD} minutos buscaré más.",
        )


async def callback_coordinate_start_pvp_1500(context: ContextTypes.DEFAULT_TYPE):
    try:
        total_text = generate_pvp_1500_pokemon_messages()
        await send_coordinates(context, total_text)
    except telegram.error.RetryAfter as e:
        await asyncio.sleep(e.retry_after)
        message = (
            f"Se pausó temporalmente el envío de coordenadas debido a un límite de velocidad. "
            f"Se reanudará automáticamente en {e.retry_after} segundos."
        )
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            text=message,
        )
        print(f"Error de RetryAfter en callback_coordinate: {e}")
        total_text_retry = generate_pvp_1500_pokemon_messages()
        await send_coordinates(context, total_text_retry)
    except Exception as e:
        print(f"Error en callback_coordinate_pvp: {e}")
        message = "Lo siento, ha ocurrido un error al generar los mensajes del bot. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible."
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            text=message,
        )

async def start_pvp_1500(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Verificar si el usuario está permitido para activar los comandos
        if update.effective_user.id not in USUARIOS_PERMITIDOS:
            await update.message.reply_text(
                "No tienes permiso para activar los comandos."
            )
            return

        # Verificar si el mensaje proviene del grupo de coordenadas
        if update.effective_chat.id != GRUPO_COORDENADAS_ID:
            await update.message.reply_text(
                "Los comandos solo pueden ser activados en el grupo de @top100galaxy1"
            )
            return

        job_start_pvp_1500 = context.chat_data.get("callback_coordinate_start_pvp_1500")

        if job_start_pvp_1500:
            await update.message.reply_text(
                "Las coordenadas de PVP se están enviando. Si desea detner el envío digite /stop"
            )
            return
        else:
            coordinates_lista_size = len(fetch_pvp_1500_pokemon_data())
            waiting_time = 1 + coordinates_waiting_time(coordinates_lista_size)
            await update.message.reply_text(
                f"En {waiting_time:.2f} segundos se enviarán las coordenadas..."
            )
            job_start_pvp_1500 = context.job_queue.run_repeating(
                callback_coordinate_start_pvp_1500, interval=PERIOD * 60, first=1
            )
            context.chat_data["callback_coordinate_start_pvp_1500"] = job_start_pvp_1500

    except telegram.error.TelegramError as e:
        print(f"Error de Telegram: {e}")
        await update.message.reply_text(
            "Se ha producido un error al ejecutar el comando /pvp1500. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible."
        )

    except Exception as e:
        print(f"Error en start_pvp_1500(): {e}")
        await update.message.reply_text(
            "Lo siento, ha ocurrido un error con el bot. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible."
        )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Verificar si el usuario está permitido para usar el comando
        if update.effective_user.id not in USUARIOS_PERMITIDOS:
            await update.message.reply_text(
                "No tienes permiso para detener el envío de coordenadas."
            )
            return

        # Verificar si el mensaje proviene del grupo de coordenadas
        if update.effective_chat.id != GRUPO_COORDENADAS_ID:
            await update.message.reply_text(
                "Los comandos solo pueden ser activados en el grupo de @top100galaxy1"
            )
            return

        job_start_pvp_1500 = context.chat_data.get("callback_coordinate_start_pvp_1500")

        if job_start_pvp_1500:
            job_start_pvp_1500.schedule_removal()
            del context.chat_data["callback_coordinate_start_pvp_1500"]
            await update.message.reply_text(
                "El envío de coordenadas PVP ha sido detenido."
            )
        else:
            await update.message.reply_text(
                "No se encontró ningún envío de coordenadas activo."
            )

    except telegram.error.TelegramError as e:
        print(f"Error de Telegram: {e}")
        await update.message.reply_text(
            "Se ha producido un error al ejecutar el comando /stop. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible."
        )

    except Exception as e:
        print(f"Error en stop: {e}")
        await update.message.reply_text(
            "Lo siento, ha ocurrido un error con el bot. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible."
        )