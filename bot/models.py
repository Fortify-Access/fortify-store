from django.db import models

# Create your models here.
class BotConfiguration(models.Model):
    title = models.CharField(max_length=64)
    api_id = models.PositiveIntegerField()
    api_hash = models.CharField(max_length=128)
    bot_token = models.CharField(max_length=364)
    user_agent = models.OneToOneField('config.User', models.CASCADE, related_name='store_bot')
    is_active = models.BooleanField(default=True)
    broadcast_channel = models.CharField(max_length=64, help_text='Broadcast telegram channel username without @')


class BotUser(models.Model):
    class Language(models.TextChoices):
        EN = 'en', 'English'
        FA = 'fa', 'Persian'

    bot = models.ForeignKey(BotConfiguration, models.CASCADE, 'users')
    telegram_user_id = models.PositiveIntegerField()
    balance = models.PositiveIntegerField(default=0)
    referral = models.ForeignKey('BotUser', models.CASCADE, 'subsets')
    panel_message_id = models.IntegerField(null=True, blank=True)
    preferred_language = models.CharField(max_length=2, choices=Language.choices, default=Language.EN)


class BotNotification(models.Model):
    class Type(models.IntegerChoices):
        BILLING = 0, 'Billing'
        TECHNICAL = 1, 'Technical'
        SUPPORT = 2, 'Support'
        OTHER = 3, 'Other'

    class Message(models.IntegerChoices):
        PAYMENT = 0, 'You have a new payment! check it out.'
        SUPPORT = 1, 'You have a new message from support team!'
        SUBSET = 2, 'Congracts! a new user clicked on your referral link!'

    bot_user = models.ForeignKey(BotUser, models.CASCADE, 'notifications')
    type = models.PositiveSmallIntegerField(choices=Type.choices)
    message = models.PositiveSmallIntegerField(choices=Message.choices)
    datetime = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
