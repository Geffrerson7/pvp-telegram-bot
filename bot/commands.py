import asyncio
from bot.service import (
    generate_pvp_pokemon_messages,
    generate_all_pvp_pokemon_messages,
)
from telegram import Update
from telegram.ext import ContextTypes
from settings.config import (
    CHAT_ID,
    SUPPORT,
    ADMIN,
    USER_1,
    USER_2,
    USER_3,
    PERIOD,
    MESSAGE_THREAD_ID,
)
import telegram
from typing import List

# ID del grupo al que se enviarán las coordenadas
GRUPO_COORDENADAS_ID = int(CHAT_ID)
TEMA_ID = int(MESSAGE_THREAD_ID)
# Lista de usuarios permitidos para activar los comandos
USUARIOS_PERMITIDOS = [int(SUPPORT), int(ADMIN), int(USER_1), int(USER_2), int(USER_3)]

PERIOD = int(PERIOD)


async def send_coordinates(
    context: ContextTypes.DEFAULT_TYPE, total_text: List[str], max_cp: int
):
    if total_text:
        messages_number = len(total_text)
        message_delay = 3 if len(total_text) > 18 else 2
        plural_letter = "" if messages_number == 1 else "s"
        if max_cp == 9999:
            max_cp = "Master League"
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text=f"Enviando {messages_number} coordenada{plural_letter} PVP {max_cp}...",
        )
        for text in total_text:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text=text,
                parse_mode="MarkdownV2",
            )
            await asyncio.sleep(message_delay)
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text=f"Se terminó de enviar la{plural_letter} coordenada{plural_letter} PVP {max_cp}. Dentro de {PERIOD} minutos se enviarán más.",
        )
    else:
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text=f"No se encontraron coordenadas. Dentro de {PERIOD} minutos buscaré más.",
        )


async def send_all_coordinates(
    context: ContextTypes.DEFAULT_TYPE, total_text: List[str]
):
    if total_text:
        messages_number = len(total_text)
        message_delay = 3 if len(total_text) > 18 else 2
        plural_letter = "" if messages_number == 1 else "s"

        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text=f"Enviando {messages_number} coordenada{plural_letter} PVP...",
        )
        for text in total_text:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text=text,
                parse_mode="MarkdownV2",
            )
            await asyncio.sleep(message_delay)
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text=f"Se terminó de enviar la{plural_letter} coordenada{plural_letter} PVP. Dentro de {PERIOD} minutos se enviarán más.",
        )
    else:
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text=f"No se encontraron coordenadas. Dentro de {PERIOD} minutos buscaré más.",
        )


async def callback_coordinate_start_pvp_1500(context: ContextTypes.DEFAULT_TYPE):
    try:
        total_text = generate_pvp_pokemon_messages(1500)
        await send_coordinates(context, total_text, 1500)
    except telegram.error.RetryAfter as e:
        await asyncio.sleep(e.retry_after)
        message = (
            f"Se pausó temporalmente el envío de coordenadas debido a un límite de velocidad. "
            f"Se reanudará automáticamente en {e.retry_after} segundos."
        )
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text=message,
        )
        print(f"Error de RetryAfter en callback_coordinate: {e}")
        total_text_retry = generate_pvp_pokemon_messages(1500)
        await send_coordinates(context, total_text_retry, 1500)
    except Exception as e:
        print(f"Error en callback_coordinate_start_pvp_1500: {e}")
        message = "Lo siento, ha ocurrido un error al generar los mensajes del bot. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible."
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text=message,
        )


async def callback_coordinate_start_pvp_2500(context: ContextTypes.DEFAULT_TYPE):
    try:
        total_text = generate_pvp_pokemon_messages(2500)
        await send_coordinates(context, total_text, 2500)
    except telegram.error.RetryAfter as e:
        await asyncio.sleep(e.retry_after)
        message = (
            f"Se pausó temporalmente el envío de coordenadas debido a un límite de velocidad. "
            f"Se reanudará automáticamente en {e.retry_after} segundos."
        )
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text=message,
        )
        print(f"Error de RetryAfter en callback_coordinate: {e}")
        total_text_retry = generate_pvp_pokemon_messages(2500)
        await send_coordinates(context, total_text_retry, 2500)
    except Exception as e:
        print(f"Error en callback_coordinate_start_pvp_2500: {e}")
        message = "Lo siento, ha ocurrido un error al generar los mensajes del bot. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible."
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text=message,
        )


async def callback_coordinate_start_pvp_master_league(
    context: ContextTypes.DEFAULT_TYPE,
):
    try:
        total_text = generate_pvp_pokemon_messages(9999)
        await send_coordinates(context, total_text, 9999)
    except telegram.error.RetryAfter as e:
        await asyncio.sleep(e.retry_after)
        message = (
            f"Se pausó temporalmente el envío de coordenadas debido a un límite de velocidad. "
            f"Se reanudará automáticamente en {e.retry_after} segundos."
        )
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text=message,
        )
        print(f"Error de RetryAfter en callback_coordinate: {e}")
        total_text_retry = generate_pvp_pokemon_messages(9999)
        await send_coordinates(context, total_text_retry, 9999)
    except Exception as e:
        print(f"Error en callback_coordinate_start_pvp_master_league: {e}")
        message = "Lo siento, ha ocurrido un error al generar los mensajes del bot. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible."
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text=message,
        )


async def callback_coordinate_start_pvp(context: ContextTypes.DEFAULT_TYPE):
    try:
        total_text = generate_all_pvp_pokemon_messages()
        await send_all_coordinates(context, total_text)
    except telegram.error.RetryAfter as e:
        await asyncio.sleep(e.retry_after)
        message = (
            f"Se pausó temporalmente el envío de coordenadas debido a un límite de velocidad. "
            f"Se reanudará automáticamente en {e.retry_after} segundos."
        )
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text=message,
        )
        print(f"Error de RetryAfter en callback_coordinate: {e}")
        total_text_retry = generate_all_pvp_pokemon_messages()
        await send_all_coordinates(context, total_text_retry)
    except Exception as e:
        print(f"Error en callback_coordinate_start_pvp_master_league: {e}")
        message = "Lo siento, ha ocurrido un error al generar los mensajes del bot. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible."
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text=message,
        )


async def start_pvp_1500(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Verificar si el usuario está permitido para activar los comandos
        if update.effective_user.id not in USUARIOS_PERMITIDOS:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="No tienes permiso para activar los comandos.",
            )
            return
        # Verificar si el mensaje proviene del grupo de coordenadas
        if update.effective_chat.id != GRUPO_COORDENADAS_ID:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Los comandos solo pueden ser activados en el grupo de @top100galaxy1",
            )
            return

        job_start_pvp_1500 = context.chat_data.get("callback_coordinate_start_pvp_1500")
        job_start_pvp_2500 = context.chat_data.get("callback_coordinate_start_pvp_2500")
        job_start_pvp_master_league = context.chat_data.get(
            "callback_coordinate_start_pvp_master_league"
        )
        job_start_pvp = context.chat_data.get("callback_coordinate_start_pvp")

        if job_start_pvp_2500:
            job_start_pvp_2500.schedule_removal()
            del context.chat_data["callback_coordinate_start_pvp_2500"]
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Las coordenadas PVP 1500 se están enviando. Si desea enviar PVP 2500, digite /stoppvp y luego /pvp2500.",
            )
            return
        elif job_start_pvp_master_league:
            job_start_pvp_master_league.schedule_removal()
            del context.chat_data["callback_coordinate_start_pvp_master_league"]
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Las coordenadas PVP 1500 se están enviando. Si desea enviar PVP Master Ball League, digite /stoppvp y luego /pvpmaster.",
            )
            return
        elif job_start_pvp:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Las coordenadas de PVP 1500 se están enviando. Si desea enviar PVP, digite /stoppvp y luego /pvp.",
            )
            return
        elif job_start_pvp_1500:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Las coordenadas de ya PVP 1500 se están enviando. Si desea detener el envío digite /stoppvp",
            )
        else:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Buscando coordenadas...",
            )
            job_start_pvp_1500 = context.job_queue.run_repeating(
                callback_coordinate_start_pvp_1500, interval=PERIOD * 60, first=1
            )
            context.chat_data["callback_coordinate_start_pvp_1500"] = job_start_pvp_1500

    except telegram.error.TelegramError as e:
        print(f"Error de Telegram: {e}")
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text="Se ha producido un error al ejecutar el comando /pvp1500. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible.",
        )

    except Exception as e:
        print(f"Error en start_pvp_1500(): {e}")
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text="Lo siento, ha ocurrido un error con el bot. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible.",
        )


async def start_pvp_2500(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Verificar si el usuario está permitido para activar los comandos
        if update.effective_user.id not in USUARIOS_PERMITIDOS:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="No tienes permiso para activar los comandos.",
            )
            return
        # Verificar si el mensaje proviene del grupo de coordenadas
        if update.effective_chat.id != GRUPO_COORDENADAS_ID:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Los comandos solo pueden ser activados en el grupo de @top100galaxy1",
            )
            return

        job_start_pvp_1500 = context.chat_data.get("callback_coordinate_start_pvp_1500")
        job_start_pvp_2500 = context.chat_data.get("callback_coordinate_start_pvp_2500")
        job_start_pvp_master_league = context.chat_data.get(
            "callback_coordinate_start_pvp_master_league"
        )
        job_start_pvp = context.chat_data.get("callback_coordinate_start_pvp")

        if job_start_pvp_1500:
            job_start_pvp_1500.schedule_removal()
            del context.chat_data["callback_coordinate_start_pvp_1500"]
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Las coordenadas PVP 2500 se están enviando. Si desea enviar PVP 1500, digite /stoppvp y luego /pvp1500.",
            )
            return
        elif job_start_pvp_master_league:
            job_start_pvp_master_league.schedule_removal()
            del context.chat_data["callback_coordinate_start_pvp_master_league"]
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Las coordenadas PVP 2500 se están enviando. Si desea enviar PVP Master Ball League, digite /stoppvp y luego /pvpmaster.",
            )
            return
        elif job_start_pvp:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Las coordenadas de PVP 2500 se están enviando. Si desea enviar PVP, digite /stoppvp y luego /pvp.",
            )
            return
        elif job_start_pvp_2500:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Las coordenadas de PVP 2500 ya se están enviando. Si desea detener el envío digite /stoppvp",
            )
        else:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Buscando coordenadas...",
            )
            job_start_pvp_2500 = context.job_queue.run_repeating(
                callback_coordinate_start_pvp_2500, interval=PERIOD * 60, first=1
            )
            context.chat_data["callback_coordinate_start_pvp_2500"] = job_start_pvp_2500

    except telegram.error.TelegramError as e:
        print(f"Error de Telegram: {e}")
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text="Se ha producido un error al ejecutar el comando /pvp2500. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible.",
        )

    except Exception as e:
        print(f"Error en start_pvp_2500(): {e}")
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text="Lo siento, ha ocurrido un error con el bot. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible.",
        )


async def start_pvp_master_league(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    try:
        # Verificar si el usuario está permitido para activar los comandos
        if update.effective_user.id not in USUARIOS_PERMITIDOS:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="No tienes permiso para activar los comandos.",
            )
            return
        # Verificar si el mensaje proviene del grupo de coordenadas
        if update.effective_chat.id != GRUPO_COORDENADAS_ID:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Los comandos solo pueden ser activados en el grupo de @top100galaxy1",
            )
            return

        job_start_pvp_1500 = context.chat_data.get("callback_coordinate_start_pvp_1500")
        job_start_pvp_2500 = context.chat_data.get("callback_coordinate_start_pvp_2500")
        job_start_pvp_master_league = context.chat_data.get(
            "callback_coordinate_start_pvp_master_league"
        )
        job_start_pvp = context.chat_data.get("callback_coordinate_start_pvp")

        if job_start_pvp_1500:
            job_start_pvp_1500.schedule_removal()
            del context.chat_data["callback_coordinate_start_pvp_1500"]
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Las coordenadas PVP Master Ball League se están enviando. Si desea enviar PVP 1500, digite /stoppvp y luego /pvp1500.",
            )
            return
        elif job_start_pvp_2500:
            job_start_pvp_2500.schedule_removal()
            del context.chat_data["callback_coordinate_start_pvp_2500"]
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Las coordenadas PVP Master Ball League se están enviando. Si desea enviar PVP 2500, digite /stoppvp y luego /pvp2500.",
            )
            return
        elif job_start_pvp:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Las coordenadas de PVP Master Ball League se están enviando. Si desea enviar PVP, digite /stoppvp y luego /pvp.",
            )
            return
        elif job_start_pvp_master_league:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Las coordenadas de PVP Master Ball League se están enviando. Si desea detener el envío digite /stoppvp",
            )
        else:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Buscando coordenadas...",
            )
            job_start_pvp_master_league = context.job_queue.run_repeating(
                callback_coordinate_start_pvp_master_league,
                interval=PERIOD * 60,
                first=1,
            )
            context.chat_data["callback_coordinate_start_pvp_master_league"] = (
                job_start_pvp_master_league
            )

    except telegram.error.TelegramError as e:
        print(f"Error de Telegram: {e}")
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text="Se ha producido un error al ejecutar el comando /pvpmaster. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible.",
        )

    except Exception as e:
        print(f"Error en start_pvp_master_league(): {e}")
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text="Lo siento, ha ocurrido un error con el bot. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible.",
        )


async def start_pvp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Verificar si el usuario está permitido para activar los comandos
        if update.effective_user.id not in USUARIOS_PERMITIDOS:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="No tienes permiso para activar los comandos.",
            )
            return
        # Verificar si el mensaje proviene del grupo de coordenadas
        if update.effective_chat.id != GRUPO_COORDENADAS_ID:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Los comandos solo pueden ser activados en el grupo de @top100galaxy1",
            )
            return

        job_start_pvp_1500 = context.chat_data.get("callback_coordinate_start_pvp_1500")
        job_start_pvp_2500 = context.chat_data.get("callback_coordinate_start_pvp_2500")
        job_start_pvp_master_league = context.chat_data.get(
            "callback_coordinate_start_pvp_master_league"
        )
        job_start_pvp = context.chat_data.get("callback_coordinate_start_pvp")

        if job_start_pvp_1500:
            job_start_pvp_1500.schedule_removal()
            del context.chat_data["callback_coordinate_start_pvp_1500"]
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Las coordenadas PVP se están enviando. Si desea enviar PVP 1500, digite /stoppvp y luego /pvp1500.",
            )
            return
        elif job_start_pvp_2500:
            job_start_pvp_2500.schedule_removal()
            del context.chat_data["callback_coordinate_start_pvp_2500"]
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Las coordenadas PVP se están enviando. Si desea enviar PVP 2500, digite /stoppvp y luego /pvp2500.",
            )
            return
        elif job_start_pvp_master_league:
            job_start_pvp_master_league.schedule_removal()
            del context.chat_data["callback_coordinate_start_pvp_master_league"]
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Las coordenadas PVP se están enviando. Si desea enviar PVP Master Ball League, digite /stoppvp y luego /pvpmaster.",
            )
            return
        elif job_start_pvp:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Las coordenadas de PVP ya se están enviando.",
            )
        else:
            await update.message.reply_text("Buscando coordenadas...")
            job_start_pvp = context.job_queue.run_repeating(
                callback_coordinate_start_pvp, interval=PERIOD * 60, first=1
            )
            context.chat_data["callback_coordinate_start_pvp"] = job_start_pvp

    except telegram.error.TelegramError as e:
        print(f"Error de Telegram: {e}")
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text="Se ha producido un error al ejecutar el comando /pvp. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible.",
        )

    except Exception as e:
        print(f"Error en start_pvp(): {e}")
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text="Lo siento, ha ocurrido un error con el bot. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible.",
        )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Verificar si el usuario está permitido para activar los comandos
        if update.effective_user.id not in USUARIOS_PERMITIDOS:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="No tienes permiso para activar los comandos.",
            )
            return
        # Verificar si el mensaje proviene del grupo de coordenadas
        if update.effective_chat.id != GRUPO_COORDENADAS_ID:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="Los comandos solo pueden ser activados en el grupo de @top100galaxy1",
            )
            return

        job_start_pvp_1500 = context.chat_data.get("callback_coordinate_start_pvp_1500")
        job_start_pvp_2500 = context.chat_data.get("callback_coordinate_start_pvp_2500")
        job_start_pvp_master_league = context.chat_data.get(
            "callback_coordinate_start_pvp_master_league"
        )
        job_start_pvp = context.chat_data.get("callback_coordinate_start_pvp")

        if job_start_pvp_1500:
            job_start_pvp_1500.schedule_removal()
            del context.chat_data["callback_coordinate_start_pvp_1500"]
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="El envío de coordenadas PVP 1500 ha sido detenido.",
            )
        elif job_start_pvp_2500:
            job_start_pvp_2500.schedule_removal()
            del context.chat_data["callback_coordinate_start_pvp_2500"]
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="El envío de coordenadas PVP 2500 ha sido detenido.",
            )
        elif job_start_pvp_master_league:
            job_start_pvp_master_league.schedule_removal()
            del context.chat_data["callback_coordinate_start_pvp_master_league"]
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="El envío de coordenadas PVP Master League ha sido detenido.",
            )
        elif job_start_pvp:
            job_start_pvp.schedule_removal()
            del context.chat_data["callback_coordinate_start_pvp"]
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="El envío de coordenadas PVP ha sido detenido.",
            )
        else:
            await context.bot.send_message(
                chat_id=GRUPO_COORDENADAS_ID,
                message_thread_id=TEMA_ID,
                text="No se encontró ningún envío de coordenadas activo.",
            )
    except telegram.error.TelegramError as e:
        print(f"Error de Telegram: {e}")
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text="Se ha producido un error al ejecutar el comando /stop. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible.",
        )

    except Exception as e:
        print(f"Error en stop(): {e}")
        await context.bot.send_message(
            chat_id=GRUPO_COORDENADAS_ID,
            message_thread_id=TEMA_ID,
            text="Lo siento, ha ocurrido un error con el bot. Por favor, comunica este error al administrador del bot para que pueda solucionarlo lo antes posible.",
        )
