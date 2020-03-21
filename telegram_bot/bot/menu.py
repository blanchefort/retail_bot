"""Главная клавиатура (меню)

Диспетчер:
dp.add_handler(MessageHandler(
            Filters.regex(r'^📂 Каталог$'),
            self._catalog))

Добавить клавиатуру в ответе:
reply_markup=ReplyKeyboardMarkup(menu_kb())
"""
from telegram_bot.decorator import save_query


#@save_query
def menu_kb():
    return [
        ['📂 Каталог',  '📄 Заявки в исполнении',],
        ['🛠 Настройки', '✉ Отправить заявку',],
        ['🛒 Корзина', '🗑 Удалить заявку']]