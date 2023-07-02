from pyrogram import Client
from pyrogram.types import InputMediaPhoto
from bot import models


async def make_input_media_photo(caption: str, photo: str=None):
    return InputMediaPhoto(photo=photo if photo else 'banners', caption=caption)

async def update_panel(client: Client, user: models.BotUser, panel_concept: dict):
    try:
        panel_message = await client.get_messages(panel_concept['chat_id'], user.panel_message_id)

        await panel_message.edit_media(
            media=await make_input_media_photo(panel_concept['text'], photo=panel_concept['photo']),
            reply_markup=panel_concept['reply_markup']
        )
        return True

    except:
        user.panel_message_id = await client.send_photo(**panel_concept).id
        await user.save(update_fields=('panel_message_id',))
