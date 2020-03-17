from telegram import ParseMode
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import KeyboardButton
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import DictPersistence

from validate_email import validate_email

from django.contrib.auth.models import User
from webpanel.models.profile import Profile

from telegram_bot.decorator import save_query

class Commands(object):
    """обработка стандартных команд

    /start — начинает общение с пользователем
    /help — отображает сообщение с помощью
    /settings — (по возможности) возвращает список возможных настроек и команды для их изменения.
    """
    def __init__(self, updater: Updater) -> None:
        
        
        self.updater = updater
        dp = updater.dispatcher

        # Регистрируем команды
        dp.add_handler(CommandHandler('start', self._start))
        dp.add_handler(CommandHandler('help', self._help))
        dp.add_handler(CommandHandler('settings', self._settings))
        
        self.STEP_B, self.STEP_C = range(2)
        registration_handler = ConversationHandler(
            entry_points=[CommandHandler('register', self._register_step_a)],
            states={
                self.STEP_B: [MessageHandler(Filters.all, self._register_step_b)],
                self.STEP_C: [MessageHandler(Filters.all, self._register_step_c)]
            },
            fallbacks=[CommandHandler('cancel', self._cancel)],
            name='registration',
            persistent=True
        )

        self.ADDRESS_B = range(1)
        address_handler = ConversationHandler(
            entry_points=[CommandHandler('address', self._address)],
            states={
                self.ADDRESS_B: [MessageHandler(Filters.text, self._address_step_b)]
            },
            fallbacks=[CommandHandler('cancel', self._cancel_address)],
            name='set_address',
            persistent=True
        )

        dp.add_handler(registration_handler)
        dp.add_handler(address_handler)


    @save_query
    def _start(self, update, context) -> None:
        """Стартовое приветствие бота
        """
        message = 'Привет!'
        message += '\n\n'
        message += 'С помощью этого бота вы можете выбрать себе товары по минимальным ценам.'
        message += '\n\n'
        message += 'Для того, чтобы заказать товары, '
        message += 'вам необходимо будет пройти авторизацию, открыв доступ к своему номеру телефона. '
        message += 'Пройдите авторизацию прямо сейчас: /register'
        update.message.reply_text(message)

    @save_query
    def _help(self, update, context) -> None:
        """Помощь по боту
        """
        message = 'Основные команды бота:'
        message += '\n\n'
        message += '/settings — Настройки вашего аккаунта.'
        message += '\n'
        message += '/order — Ваш заказ.'
        message += '\n'
        message += '/catalog — Каталог товаров.'
        message += '\n'
        message += '/address — Ваш адрес для доставки.'
        message += '\n'
        message += '/help — помощь.'
        
        update.message.reply_text(message)

    @save_query
    def _settings(self, update, context) -> None:
        """Профиль пользователя
        """
        # Попробуем найти пользователя, если он зарегистрирован
        c = Profile.objects.filter(telegram_id=update.message.chat.id).count()
        if c == 0:
            # Пользователь не создан
            message = 'Кажется, вы ещё не зарегистрировались в системе. Нажмите /register для продолжения.'
        else:
            user = Profile.objects.get(telegram_id=update.message.chat.id)
            user = User.objects.get(id=user.id)
            message = 'Ваши данные:'
        
            message += f'\nТелефон: {user.profile.phone}'
            message += f'\nПочта: {user.email}'
            #message += f'\nИмя: {user.first_name}'
            #message += f'\nФамилия: {user.last_name}'
            message += f'\nЛогин: {user.username}'
            message += f'\nАдрес доставки: {user.profile.address}'
            message += f'\nТип аккаунта: {user.profile.type}'

        update.message.reply_text(message)

    @save_query
    def _address(self, update, context):
        """Арес пользователя
        """
        c = Profile.objects.filter(telegram_id=update.message.chat.id).count()
        if c == 0:
            # Пользователь не создан
            message = 'Кажется, вы ещё не зарегистрировались в системе. Нажмите /register для продолжения.'
        else:
            user = Profile.objects.get(telegram_id=update.message.chat.id)
            user = User.objects.get(id=user.id)

            message = 'Ваш текущий адрес, указанный в системе:'
            message += '\n\n'
            message += f'----\n{user.profile.address}\n----'
            message += '\n\n'
            message += 'Если данный адрес некорректный, введите новый. Если всё верно, введите команду /cancel'
            update.message.reply_text(message)
            return self.ADDRESS_B

    @save_query
    def _address_step_b(self, update, context):
        address = update.message.text.lower().strip()
        if '/cancel' == address:
            message = 'Адрес не изменён.'
            update.message.reply_text(message)
            return ConversationHandler.END
        else:
            c = Profile.objects.filter(telegram_id=update.message.chat.id).count()
            if c == 0:
                # Пользователь не создан
                message = 'Кажется, вы ещё не зарегистрировались в системе. Нажмите /register для продолжения.'
                return ConversationHandler.END
            else:
                user = Profile.objects.get(telegram_id=update.message.chat.id)
                user = User.objects.get(id=user.id)
                user.profile.address = address
                user.save()
                message = 'Изменения сохранены!'
                update.message.reply_text(message)
                return ConversationHandler.END

    @save_query
    def _register_step_a(self, update, context):
        """Регистрация нового бесплатного покупателя:
        Шаг 1: Поле для телефона
        """
        c = Profile.objects.filter(telegram_id=update.message.chat.id).count()
        if c > 0:
            message = 'Вы уже зарегистрированы. Начните искать товары, просто набрав нужное название!'
            reply_markup=ReplyKeyboardRemove()
        else:
            message = '*Регистрация*'
            message += '\nДля регистрации вам нужно будет указать телефон и электронную почту. '
            message += 'После регистрации вы получите пароль.'
            message += '\n\nНажмите на кнопку ниже, чтобы предоставить свой номер телефона.'
            btn = KeyboardButton(text='Показать номер телефона', request_contact=True)
            reply_markup=ReplyKeyboardMarkup([[btn]], one_time_keyboard=True)

        update.message.reply_text(
            message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN)
        return self.STEP_B

    @save_query
    def _register_step_b(self, update, context):
        """Регистрация нового бесплатного покупателя:
        Шаг 2: Поле для электропочты
        """
        phone_number = update.message.contact.phone_number
        if phone_number is not None:
            if Profile.objects.filter(phone=phone_number):
                # Данный номер уже существует в системе
                message = 'Данный номер телефона уже зарегистрирован в системе.'
                update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
                return ConversationHandler.END
            else:
                # Телефон не найден, продолжаем регистрацию
                context.user_data['phone_number'] = phone_number
                message = 'Укажите адрес вашей электронной почты:'
                update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
                return self.STEP_C
        else:
            message = 'Не удалось получить номер телефона. Пожалуйста, начните регистрацию с команды /register'
            update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

    @save_query
    def _register_step_c(self, update, context):
        """Регистрация нового бесплатного покупателя:
        Шаг 3: Сохранение результата, выдаётся пароль
        """
        text = update.message.text.lower().strip()

        if validate_email(text):
            #'Валидация почты успешна'
            if User.objects.filter(email=text):
                message = 'Такой адрес электронной почты уже зарегистрирован в системе. Попробуйте заново с другой почтой: /register'
            else:
                # Все проверки закончены, регистрируем нового пользователя
                # if User.objects.filter(username=update.message.chat.username):
                #     username = context.user_data['phone_number']
                # else:
                # if len(update.message.chat.username) > 3:
                #     username = update.message.chat.username
                # else:
                #     username = context.user_data['phone_number']

                # if update.message.chat.username:
                #     #
                username = context.user_data['phone_number']

                new_user = User(username=username, email=text)
                password = User.objects.make_random_password()
                new_user.set_password(password)
                new_user.last_name = update.message.chat.last_name or ''
                new_user.first_name = update.message.chat.first_name or ''
                new_user.save()

                new_user.profile.type = 1
                new_user.profile.phone = context.user_data['phone_number']
                new_user.profile.telegram_id = update.message.chat.id
                new_user.save()
                message = 'Поздравляем! Вы успешно зарегистрировались в системе.'
                message += ' Теперь вы можете осуществлять поиск по товарам и заказывать то, что вам нужно.'
                message += '\n\nВаши учётные данные:'
                message += f'\nЛогин: {username}'
                message += f'\nПароль: {password}'

                message += 'Вы также можете указать свой адрес для доставки товаров.'
                message += 'Для этого воспользуйтесь командой /address'

        else:
            message = 'Введён некорректный адрес почты. Попробуйте заново: /register'

        update.message.reply_text(message)
        return ConversationHandler.END

    @save_query
    def _cancel(self, update, context):
        """Отмена последовательного диалога
        """
        update.message.reply_text('Отмена', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    @save_query
    def _cancel_address(self, update, context):
        """Отмена последовательного диалога
        """
        update.message.reply_text('Отмена', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END