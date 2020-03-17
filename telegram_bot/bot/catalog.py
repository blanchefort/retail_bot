from telegram import ParseMode
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import Filters

from django.contrib.auth.models import User
from django.core.paginator import Paginator

from webpanel.models.profile import Profile
from webpanel.models.product import Product
from webpanel.models.product_category import ProductCategory

from telegram_bot.decorator import save_query

class Catalog(object):
    """Просмотр каталога товаров
    """
    def __init__(self, updater: Updater) -> None:
        self.updater = updater
        dp = updater.dispatcher

        # Старт каталога
        dp.add_handler(CommandHandler('catalog', self._catalog))

        # Выбор категории каталога, страница 1
        # catalog_category_CATEGORY_PAGE
        dp.add_handler(CallbackQueryHandler(
            callback=self._catalog_category,
            pattern=r'^catalog_category_[0-9]*_[0-9]*$'))


    @save_query
    def _catalog(self, update, context):
        """Старт просмотра каталога
        """
        message = '<b>📂 Каталог доступных товаров</b>'
        keyboard = []

        for c in ProductCategory.objects.all():
            button = [InlineKeyboardButton(c.name, callback_data=f'catalog_category_{c.id}_1')]
            keyboard.append(button)
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup)

    def _catalog_category(self, update, context):
        """Просмотр товаров в выбранной категории
        """
        query = update.callback_query
        category_id = int(query.data.split('_')[-2])
        page_no = int(query.data.split('_')[-1])

        if ProductCategory.objects.filter(id=category_id):
            category = ProductCategory.objects.get(id=category_id)
            products = Product.objects.filter(is_active=True).filter(category=category).order_by('title')
            paginator = Paginator(products, 5)
            page = paginator.get_page(page_no)
            keyboard = []

            message = f'📂 *{category.name}*'
            message += f'\nВ категории позиций: *{products.count()}*'
            message += '\n\n*Товары:*'
            for item in page:
                message += f'\n\n📦 *{item.title}*'
                message += f'\nЦена: {item.price} ₸ за {item.unit.short}'
                message += f'\nДобавить в заказ: /product{item.id}'


            # Previous
            if page.has_previous():
                button = InlineKeyboardButton(
                    '1',
                    callback_data=f'catalog_category_{category_id}_1')
                keyboard.append(button)
                button = InlineKeyboardButton(
                    '⬅️',
                    callback_data=f'catalog_category_{category_id}_{page.previous_page_number()}')
                keyboard.append(button)
            # Current
            button = InlineKeyboardButton(
                    f'• {page.number} из {page.paginator.num_pages} •',
                    callback_data=f'catalog_category_{category_id}_{page.number}')
            keyboard.append(button)
            # Next
            if page.has_next():
                button = InlineKeyboardButton(
                    '➡️',
                    callback_data=f'catalog_category_{category_id}_{page.next_page_number()}')
                keyboard.append(button)
                button = InlineKeyboardButton(
                    f'{page.paginator.num_pages}',
                    callback_data=f'catalog_category_{category_id}_{page.paginator.num_pages}')
                keyboard.append(button)



            #button = [InlineKeyboardButton('Пагинация', callback_data=f'catalog_category_{category_id}_1')]
            #keyboard.append(button)

            reply_markup = InlineKeyboardMarkup([keyboard])


            query.edit_message_text(
                message,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup)