from telegram import ParseMode
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import Filters

from django.contrib.auth.models import User

from webpanel.models.order import Order as OrderModel
from webpanel.models.profile import Profile

from telegram_bot.decorator import save_query
from .menu import menu_kb

class Order(object):
    """Формирование заказа
    """
    def __init__(self, updater: Updater) -> None:
        self.updater = updater
        dp = updater.dispatcher

        # Регистрируем команды
        dp.add_handler(CommandHandler('order', self._order))
        dp.add_handler(MessageHandler(
            Filters.regex(r'^🛒 Корзина$'),
            self._order))

        dp.add_handler(MessageHandler(
            Filters.regex(r'^Отправить заявку на исполнение$'),
            self._execute_order))
        dp.add_handler(MessageHandler(
            Filters.regex(r'^✉ Отправить заявку$'),
            self._execute_order))

        dp.add_handler(MessageHandler(
            Filters.regex(r'^Удалить заявку полностью$'),
            self._delete_order))
        dp.add_handler(MessageHandler(
            Filters.regex(r'^🗑 Удалить заявку$'),
            self._delete_order))

        dp.add_handler(MessageHandler(
            Filters.regex(r'^Список заявок в исполнении$'),
            self._order_list))
        dp.add_handler(MessageHandler(
            Filters.regex(r'^📄 Заявки в исполнении$'),
            self._order_list))

        # Изменение объёма позиции
        dp.add_handler(CallbackQueryHandler(
            callback=self._change_product_1,
            pattern=r'^chpk_1_[0-9]*$'))
        dp.add_handler(CallbackQueryHandler(
            callback=self._change_product_2,
            pattern=r'^chpk_2_[0-9]*$'))
        dp.add_handler(CallbackQueryHandler(
            callback=self._change_product_3,
            pattern=r'^chpk_3_[0-9]*$'))
        dp.add_handler(CallbackQueryHandler(
            callback=self._change_product_4,
            pattern=r'^chpk_4_[0-9]*$'))
        dp.add_handler(CallbackQueryHandler(
            callback=self._change_product_5,
            pattern=r'^chpk_5_[0-9]*$'))
        dp.add_handler(CallbackQueryHandler(
            callback=self._change_product_6,
            pattern=r'^chpk_6_[0-9]*$'))

        # Удаление позиции
        dp.add_handler(CallbackQueryHandler(
            callback=self._delete_product,
            pattern=r'^delete_product_[0-9]*$'))


    @save_query
    def _order(self, update, context) -> None:
        """Данные по заказу
        """
        user = Profile.objects.get(telegram_id=update.message.chat.id)
        user = User.objects.get(id=user.id)

        order_count = OrderModel.objects.filter(user=user).filter(status=0).count()

        if order_count == 0:
            # Нет заказов
            message = 'Вы пока не добавили товары в заявку. Выберите что-нибудь с помощью поиска: /search Или посмотрите список заявок в исполнении.'
            
            update.message.reply_text(message,
                reply_markup=ReplyKeyboardMarkup(menu_kb()))
        else:
            # Товары есть, выводим их:
            order = OrderModel.objects.filter(user=user).filter(status=0)
            message = '*Ваша заявка*'
            message += f'\nВсего позиций: {order_count}'
            update.message.reply_text(
                message,
                parse_mode=ParseMode.MARKDOWN)

            for item in order:
                message = f'\n\n📦 <b>{item.product.title}</b>'
                message += f'\nЦена: {item.product.price} ₸ за {item.product.unit.short}'
                message += f'\nОбъём товара: {int(item.product_count)} {item.product.unit.short}'
                #message += f'\nИзменить объём товара: /change_product_count_{item.id}'
                message += f'\n\nВоспользуйтесь кнопками ниже, чтобы изменить объём товара (увеличить или уменьшить):'
                keyboard = [
                    [
                        InlineKeyboardButton('+1', callback_data=f'chpk_1_{item.id}'),
                        InlineKeyboardButton('+10', callback_data=f'chpk_2_{item.id}'),
                        InlineKeyboardButton('+100', callback_data=f'chpk_3_{item.id}')
                    ],
                    [
                        InlineKeyboardButton('-1', callback_data=f'chpk_4_{item.id}'),
                        InlineKeyboardButton('-10', callback_data=f'chpk_5_{item.id}'),
                        InlineKeyboardButton('-100', callback_data=f'chpk_6_{item.id}')
                    ],
                    [InlineKeyboardButton('Удалить', callback_data=f'delete_product_{item.id}')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                update.message.reply_text(
                    message,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup)

            reply_keyboard = menu_kb()
            message = 'После проверки заказа не забудьте его отправить на исполнение!'
            update.message.reply_text(
                message,
                reply_markup=ReplyKeyboardMarkup(reply_keyboard))

    @save_query
    def _execute_order(self, update, context) -> None:
        """Отправить заявку на исполнение
        """
        user = Profile.objects.get(telegram_id=update.message.chat.id)
        user = User.objects.get(id=user.id)
        order_count = OrderModel.objects.filter(user=user).filter(status=0).count()

        if order_count > 0:
            # Заявка не пуста, отправляем её продавцу (или продавцам)
            OrderModel.objects.filter(user=user).filter(status=0).update(status=1)

            # Список товаров в заявке:
            message = 'Заявка упешно отправлена на исполнение.'
            message += '\n\nСписок заказанных товаров:'
            total_sum = 0
            for item in OrderModel.objects.filter(user=user).filter(status=1):
                message += f'\n📦 *{item.product.title}*'
                message += f'\nЦена: {item.product.price} ₸'
                message += f'\nКоличество: {item.product_count} за {item.product.unit.short}'
                product_sum = round(item.product.price * item.product_count, 2)
                total_sum += product_sum
                message += f'\nСумма: {product_sum} ₸'
                message += f'\n\n'
            message += '----'
            message += f'\n*Общая сумма: {total_sum} ₸*'
            update.message.reply_text(
                message,
                reply_markup=ReplyKeyboardMarkup(menu_kb()),
                parse_mode=ParseMode.MARKDOWN)
        else:
            update.message.reply_text('Ваша заявка пуста. Нечего отправлять.',
                reply_markup=ReplyKeyboardMarkup(menu_kb()))

    @save_query
    def _delete_order(self, update, context) -> None:
        """Удалить заявку полностью
        """
        user = Profile.objects.get(telegram_id=update.message.chat.id)
        user = User.objects.get(id=user.id)
        order_count = OrderModel.objects.filter(user=user).filter(status=0).count()

        if order_count > 0:
            # Удаляем
            OrderModel.objects.filter(user=user).filter(status=0).update(status=5)
            update.message.reply_text(
                'Заявка удалена.',
                reply_markup=ReplyKeyboardMarkup(menu_kb()))
        else:
            update.message.reply_text('Ваша заявка пуста. Нечего удалять.',
                reply_markup=ReplyKeyboardMarkup(menu_kb()))

    @save_query
    def _order_list(self, update, context) -> None:
        """Список заявок в исполнении
        """
        user = Profile.objects.get(telegram_id=update.message.chat.id)
        user = User.objects.get(id=user.id)
        order_count_1 = OrderModel.objects.filter(user=user).filter(status=1).count()
        order_count_2 = OrderModel.objects.filter(user=user).filter(status=2).count()
        order_count_3 = OrderModel.objects.filter(user=user).filter(status=3).count()
        message = '*Статус ваших заявок*'
        message += (
            f'\nКоличество товаров, ожидающих выставление счёта: {order_count_1}'
            f'\nКоличество товаров, принятых в работу: {order_count_2}'
            f'\nКоличество товаров, ожидающих доставки: {order_count_3}')


        update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ReplyKeyboardMarkup(menu_kb()))

    def _delete_product(self, update, context) -> None:
        """Удалить: delete_product_{item.id}
        """
        query = update.callback_query
        order_id = int(query.data.split('_')[-1])
        order = OrderModel.objects.get(id=order_id)
        order.status = 5
        order.save()
        query.edit_message_text('Товар удалён')

    def _change_product_1(self, update, context) -> None:
        """Увеличить объём товара на 1

        chpk_1_{item.id}
        """
        query = update.callback_query
        order_id = int(query.data.split('_')[-1])
        order = OrderModel.objects.get(id=order_id)
        order.product_count = order.product_count + 1
        order.save()

        message = f'\n\n📦 <b>{order.product.title}</b>'
        message += f'\nЦена: {order.product.price} ₸ за {order.product.unit.short}'
        message += f'\nОбъём товара: <b>{int(order.product_count)}</b> {order.product.unit.short}'
        message += f'\n\nВоспользуйтесь кнопками ниже, чтобы изменить объём товара (увеличить или уменьшить):'
        keyboard = [
            [
                InlineKeyboardButton('+1', callback_data=f'chpk_1_{order.id}'),
                InlineKeyboardButton('+10', callback_data=f'chpk_2_{order.id}'),
                InlineKeyboardButton('+100', callback_data=f'chpk_3_{order.id}')
            ],
            [
                InlineKeyboardButton('-1', callback_data=f'chpk_4_{order.id}'),
                InlineKeyboardButton('-10', callback_data=f'chpk_5_{order.id}'),
                InlineKeyboardButton('-100', callback_data=f'chpk_6_{order.id}')
            ],
            [InlineKeyboardButton('Удалить', callback_data=f'delete_product_{order.id}')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup)
    
    def _change_product_2(self, update, context) -> None:
        """Увеличить объём товара на 10

        chpk_1_{item.id}
        """
        query = update.callback_query
        order_id = int(query.data.split('_')[-1])
        order = OrderModel.objects.get(id=order_id)
        order.product_count = order.product_count + 10
        order.save()

        message = f'\n\n📦 <b>{order.product.title}</b>'
        message += f'\nЦена: {order.product.price} ₸ за {order.product.unit.short}'
        message += f'\nОбъём товара: <b>{int(order.product_count)}</b> {order.product.unit.short}'
        message += f'\n\nВоспользуйтесь кнопками ниже, чтобы изменить объём товара (увеличить или уменьшить):'
        keyboard = [
            [
                InlineKeyboardButton('+1', callback_data=f'chpk_1_{order.id}'),
                InlineKeyboardButton('+10', callback_data=f'chpk_2_{order.id}'),
                InlineKeyboardButton('+100', callback_data=f'chpk_3_{order.id}')
            ],
            [
                InlineKeyboardButton('-1', callback_data=f'chpk_4_{order.id}'),
                InlineKeyboardButton('-10', callback_data=f'chpk_5_{order.id}'),
                InlineKeyboardButton('-100', callback_data=f'chpk_6_{order.id}')
            ],
            [InlineKeyboardButton('Удалить', callback_data=f'delete_product_{order.id}')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup)

    def _change_product_3(self, update, context) -> None:
        """Увеличить объём товара на 100

        chpk_1_{item.id}
        """
        query = update.callback_query
        order_id = int(query.data.split('_')[-1])
        order = OrderModel.objects.get(id=order_id)
        order.product_count = order.product_count + 100
        order.save()

        message = f'\n\n📦 <b>{order.product.title}</b>'
        message += f'\nЦена: {order.product.price} ₸ за {order.product.unit.short}'
        message += f'\nОбъём товара: <b>{int(order.product_count)}</b> {order.product.unit.short}'
        message += f'\n\nВоспользуйтесь кнопками ниже, чтобы изменить объём товара (увеличить или уменьшить):'
        keyboard = [
            [
                InlineKeyboardButton('+1', callback_data=f'chpk_1_{order.id}'),
                InlineKeyboardButton('+10', callback_data=f'chpk_2_{order.id}'),
                InlineKeyboardButton('+100', callback_data=f'chpk_3_{order.id}')
            ],
            [
                InlineKeyboardButton('-1', callback_data=f'chpk_4_{order.id}'),
                InlineKeyboardButton('-10', callback_data=f'chpk_5_{order.id}'),
                InlineKeyboardButton('-100', callback_data=f'chpk_6_{order.id}')
            ],
            [InlineKeyboardButton('Удалить', callback_data=f'delete_product_{order.id}')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup)

    def _change_product_4(self, update, context) -> None:
        """Уменьшить объём товара на 1

        chpk_1_{item.id}
        """
        query = update.callback_query
        order_id = int(query.data.split('_')[-1])
        order = OrderModel.objects.get(id=order_id)
        order.product_count = order.product_count - 1
        if order.product_count < 0:
            order.product_count = 0
        order.save()

        message = f'\n\n📦 <b>{order.product.title}</b>'
        message += f'\nЦена: {order.product.price} ₸ за {order.product.unit.short}'
        message += f'\nОбъём товара: <b>{int(order.product_count)}</b> {order.product.unit.short}'
        message += f'\n\nВоспользуйтесь кнопками ниже, чтобы изменить объём товара (увеличить или уменьшить):'
        keyboard = [
            [
                InlineKeyboardButton('+1', callback_data=f'chpk_1_{order.id}'),
                InlineKeyboardButton('+10', callback_data=f'chpk_2_{order.id}'),
                InlineKeyboardButton('+100', callback_data=f'chpk_3_{order.id}')
            ],
            [
                InlineKeyboardButton('-1', callback_data=f'chpk_4_{order.id}'),
                InlineKeyboardButton('-10', callback_data=f'chpk_5_{order.id}'),
                InlineKeyboardButton('-100', callback_data=f'chpk_6_{order.id}')
            ],
            [InlineKeyboardButton('Удалить', callback_data=f'delete_product_{order.id}')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup)

    def _change_product_5(self, update, context) -> None:
        """Уменьшить объём товара на 1

        chpk_1_{item.id}
        """
        query = update.callback_query
        order_id = int(query.data.split('_')[-1])
        order = OrderModel.objects.get(id=order_id)
        order.product_count = order.product_count - 10
        if order.product_count < 0:
            order.product_count = 0
        order.save()

        message = f'\n\n📦 <b>{order.product.title}</b>'
        message += f'\nЦена: {order.product.price} ₸ за {order.product.unit.short}'
        message += f'\nОбъём товара: <b>{int(order.product_count)}</b> {order.product.unit.short}'
        message += f'\n\nВоспользуйтесь кнопками ниже, чтобы изменить объём товара (увеличить или уменьшить):'
        keyboard = [
            [
                InlineKeyboardButton('+1', callback_data=f'chpk_1_{order.id}'),
                InlineKeyboardButton('+10', callback_data=f'chpk_2_{order.id}'),
                InlineKeyboardButton('+100', callback_data=f'chpk_3_{order.id}')
            ],
            [
                InlineKeyboardButton('-1', callback_data=f'chpk_4_{order.id}'),
                InlineKeyboardButton('-10', callback_data=f'chpk_5_{order.id}'),
                InlineKeyboardButton('-100', callback_data=f'chpk_6_{order.id}')
            ],
            [InlineKeyboardButton('Удалить', callback_data=f'delete_product_{order.id}')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup)

    def _change_product_6(self, update, context) -> None:
        """Уменьшить объём товара на 100

        chpk_1_{item.id}
        """
        query = update.callback_query
        order_id = int(query.data.split('_')[-1])
        order = OrderModel.objects.get(id=order_id)
        order.product_count = order.product_count - 100
        if order.product_count < 0:
            order.product_count = 0
        order.save()

        message = f'\n\n📦 <b>{order.product.title}</b>'
        message += f'\nЦена: {order.product.price} ₸ за {order.product.unit.short}'
        message += f'\nОбъём товара: <b>{int(order.product_count)}</b> {order.product.unit.short}'
        message += f'\n\nВоспользуйтесь кнопками ниже, чтобы изменить объём товара (увеличить или уменьшить):'
        keyboard = [
            [
                InlineKeyboardButton('+1', callback_data=f'chpk_1_{order.id}'),
                InlineKeyboardButton('+10', callback_data=f'chpk_2_{order.id}'),
                InlineKeyboardButton('+100', callback_data=f'chpk_3_{order.id}')
            ],
            [
                InlineKeyboardButton('-1', callback_data=f'chpk_4_{order.id}'),
                InlineKeyboardButton('-10', callback_data=f'chpk_5_{order.id}'),
                InlineKeyboardButton('-100', callback_data=f'chpk_6_{order.id}')
            ],
            [InlineKeyboardButton('Удалить', callback_data=f'delete_product_{order.id}')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(
            message,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup)