#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.


from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message

import config 
from config import BANNED_USERS
from strings import get_command, get_string, helpers
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils import help_pannel
from YukkiMusic.utils.database import get_lang, is_commanddelete_on, is_on_off
from YukkiMusic.utils.decorators.language import (LanguageStart,
                                                  languageCB)
from YukkiMusic.utils.inline.help import (help_back_markup,
                                          private_help_panel)

### Command
HELP_COMMAND = get_command("HELP_COMMAND")


@app.on_message(
    filters.command(HELP_COMMAND)
    & filters.private
    & ~filters.edited
    & ~BANNED_USERS
)
@app.on_callback_query(
    filters.regex("settings_back_helper") & ~BANNED_USERS
)
async def helper_private(
    client: app, update: Union[types.Message, types.CallbackQuery]
):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_, True)
        if update.message.photo:
            await update.message.delete()
            await update.message.reply_photo(
                photo="https://telegra.ph/file/803ffb6adaeb83215a8d0.jpg",
                #caption=_["help_1"],
                reply_markup=keyboard
            )
            if await is_on_off(config.LOG):
                sender_id = update.from_user.id
                sender_name = update.from_user.first_name
                log_message = (
                    f"{update.from_user.mention} has just started bot to check <code>HELP INFORMATION</code>\n\n**USER ID:** {sender_id}\n**USER NAME:** {sender_name}"
                )
                await app.send_message(config.LOG_GROUP_ID, log_message)
            
        else:
            await update.edit_message_text(
                #_["help_1"],
                reply_markup=keyboard
            )
    else:
        chat_id = update.chat.id
        if await is_commanddelete_on(update.chat.id):
            try:
                await update.delete()
            except:
                pass
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_)
        await update.reply_photo(
            photo="https://telegra.ph/file/803ffb6adaeb83215a8d0.jpg",
            #caption=_["help_1"], 
            reply_markup=keyboard
        )
        if await is_on_off(config.LOG):
            sender_id = update.from_user.id
            sender_name = update.from_user.first_name
            log_message = (
                f"{update.from_user.mention} has just started bot to check <code>HELP INFORMATION</code>\n\n**USER ID:** {sender_id}\n**USER NAME:** {sender_name}"
            )
            await app.send_message(config.LOG_GROUP_ID, log_message)
        
@app.on_message(
    filters.command(HELP_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(
        _["help_2"], reply_markup=InlineKeyboardMarkup(keyboard)
    )


@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_back_markup(_)    
    if cb == "hb1":
        await CallbackQuery.edit_message_text(
            helpers.HELP_1, reply_markup=keyboard
        )
    elif cb == "hb2":
        await CallbackQuery.edit_message_text(
            helpers.HELP_2, reply_markup=keyboard
        )
    elif cb == "hb3":
        await CallbackQuery.edit_message_text(
            helpers.HELP_3, reply_markup=keyboard
        )
    elif cb == "hb4":
        await CallbackQuery.edit_message_text(
            helpers.HELP_4, reply_markup=keyboard
        )
