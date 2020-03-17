from django.contrib.auth.models import User
from webpanel.models.profile import Profile

from .models import Logger


def save_query(func):
    """Декоратор: сохраняет в БД пользовательский запрос
    """
    def wrapper(inner, update, context):
        u = update
        c = Profile.objects.filter(telegram_id=u.message.chat.id).count()
        if c > 0:
            user = Profile.objects.get(telegram_id=u.message.chat.id)
            user = User.objects.get(id=user.id)
            Logger(
                user=user,
                chat_id=u.message.chat.id,
                message=u.message.text
            ).save()
        func(inner, update, context)
    return wrapper