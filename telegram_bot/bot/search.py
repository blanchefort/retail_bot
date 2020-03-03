from telegram import ParseMode
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from django.contrib.auth.models import User

from webpanel.models.product import Product
from webpanel.models.order import Order
from webpanel.models.profile import Profile

class Search(object):
    """Поиск по товарам
    """
    def __init__(self, updater: Updater) -> None:
        self.updater = updater
        dp = updater.dispatcher

        # Регистрируем команды
        dp.add_handler(CommandHandler('search', self._search))
        dp.add_handler(MessageHandler(
            Filters.regex('/product[0-9]*$'),
            self._add_to_order))

        # Любой текст, введённый без команды считается поиском товара
        dp.add_handler(MessageHandler(Filters.all, self._results))


    def _search(self, update, context) -> None:
        """Поиск
        """
        update.message.reply_text('Напишите название товара, и мы выведем вам результат поиска.')

    def _results(self, update, context) -> None:
        """Результаты поиска для бесплатного покупателя
        """
        search_query = update.message.text
        # В PostgreSQL можно делать более совершенный поиск
        # https://docs.djangoproject.com/en/3.0/topics/db/search/
        search_result = Product.objects.filter(title__icontains=search_query).filter(is_active=1)

        if len(search_result) == 0:
            message = 'По вашему запросу ничего не найдено.'
        else:
            result_count = len(search_result)
            message = '*Результаты поиска*'
            message += f'\nНайдено {result_count} товаров'
            message += '\nТовары:'

            for item in search_result:
                message += f'\n\n📦 *{item.title}*'
                message += f'\nЦена: {item.price} ₸ за {item.unit.short}'
                message += f'\nДобавить в заказ: /product{item.id}'

        update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN)

    def _add_to_order(self, update, context) -> None:
        """Добавление товара в заказ
        """
        product_id = int(update.message.text.split('t')[-1])
        product = Product.objects.get(id=product_id)
        user = Profile.objects.get(telegram_id=update.message.chat.id)
        user = User.objects.get(id=user.id)

        if product.is_active == True:
            # проверим, не нажимал ли пользователь уже на этот товар
            check_count = Order.objects.filter(product=product
                                ).filter(user=user
                                ).filter(status=0
                                ).count()

            if check_count == 0:
                # новая строчка заказа
                order = Order(product=product, user=user)
                order.status = 0
                order.save()

            message = 'Товар добавлен к заказу:'
            message += (
                f'\nНазвание: *{product.title}*'
                f'\nЦена: *{product.price}* ₸'
                f'\n\nКоличество товара вы сможете указать при отправке заказа: /order')
        else:
            message = 'К сожалению, данной товарной позиции уже нет в списке доступных товаров.'

        update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN)