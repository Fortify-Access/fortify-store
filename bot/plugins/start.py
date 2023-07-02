from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from bot import models
from bot import functions

@Client.on_message(filters.private & filters.regex("^/start"))
async def start(client: Client, message: Message):
    bot = await models.BotConfiguration.objects.get(bot_token=client.bot_token)
    user, created = await models.BotUser.objects.get_or_create(telegram_user_id=message.from_user.id, bot=bot)
    message.delete()

    with translation.override(user.preferred_language):
        if created:
            if len((message_args := message.text.split(' '))) == 2:
                referral = message_args[-1].split('_')[-1]
                referral_user = await models.BotUser.objects.get(referral)

                await models.BotNotification.objects.create(
                    bot_user=referral_user, type=models.BotNotification.Type.OTHER, message=models.BotNotification.Message.SUBSET)

            panel_concept = {
                'chat_id': user.telegram_user_id,
                'photo': 'goh',
                'text': 'Choose your language',
                'reply_markup': InlineKeyboardMarkup([
                    [InlineKeyboardButton("English", callback_data="set_language_english"),
                    InlineKeyboardButton("فارسی", callback_data="set_language_farsi")]
                ])
            }
            await functions.update_panel(client, user, panel_concept)

            return True

        panel_concept = {
            'chat_id': user.telegram_user_id,
            'photo': 'goh',
            'text': _('Your panel'),
            'reply_markup': InlineKeyboardMarkup([[InlineKeyboardButton("kossher", callback_data="kos")]])
        }
        await functions.update_panel(client, user, panel_concept)


@Client.on_callback_query(filters.regex("^set_language_(.*)$"))
async def set_language(client: Client, callback_query: CallbackQuery):
    language = callback_query.data.split('_')[-1]
    user = await models.BotUser.objects.get(telegram_user_id=callback_query.from_user.id)
    user.preferred_language = language[:2]
    await user.save(update_fields=('language',))

    await callback_query.answer(_(f"Your language has been set to {language}"), user.preferred_language)
    await start(client, callback_query.message)
