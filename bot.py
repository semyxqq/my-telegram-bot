import telebot
from telebot import types

# ===== НАСТРОЙКИ =====
BOT_TOKEN = "import telebot
from telebot import types

# ===== НАСТРОЙКИ =====
BOT_TOKEN = "import telebot
from telebot import types

# ===== НАСТРОЙКИ =====
BOT_TOKEN = "import telebot
from telebot import types

# ===== НАСТРОЙКИ =====
BOT_TOKEN = "8986216792:AAFk9vAO8ToUoGVngmcKtVh1oHgPx5sVFI"   # Получить у @BotFather
ADMIN_ID = 1078750702                    # Твой Telegram ID (узнать у @userinfobot)
CHANNEL_LINK = "https://t.me/slavreviews"  # Ссылка на твой канал
CHANNEL_NAME = "Репка"              # Название канала

bot = telebot.TeleBot(BOT_TOKEN)

# Хранилище состояний (кто в режиме написания сообщения)
user_states = {}


# ===== ГЛАВНОЕ МЕНЮ =====
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_channel = types.KeyboardButton("📢 Ссылка на канал")
    btn_write = types.KeyboardButton("✉️ Написать мне")
    markup.add(btn_channel, btn_write)
    return markup


# ===== /start =====
@bot.message_handler(commands=['start'])
def start(message):
    text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Я бот для связи. Здесь ты можешь:\n"
        "• Получить ссылку на мой канал\n"
        "• Написать мне личное сообщение\n\n"
        "Выбери действие ниже 👇"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())


# ===== /help =====
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(
        message.chat.id,
        "Доступные команды:\n"
        "/start — главное меню\n"
        "/channel — ссылка на канал\n"
        "/write — написать сообщение\n"
        "/cancel — отменить написание",
        reply_markup=main_menu()
    )


# ===== Ссылка на канал =====
@bot.message_handler(commands=['channel'])
@bot.message_handler(func=lambda m: m.text == "📢 Ссылка на канал")
def send_channel(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"➡️ {CHANNEL_NAME}", url=CHANNEL_LINK))
    bot.send_message(
        message.chat.id,
        f"Вот ссылка на мой канал:\n{CHANNEL_LINK}",
        reply_markup=markup
    )


# ===== Написать мне =====
@bot.message_handler(commands=['write'])
@bot.message_handler(func=lambda m: m.text == "✉️ Написать мне")
def ask_message(message):
    user_states[message.chat.id] = "writing"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❌ Отмена"))
    bot.send_message(
        message.chat.id,
        "✍️ Напиши своё сообщение, и я передам его владельцу.\n\n"
        "Можно отправить текст, фото, видео или документ.",
        reply_markup=markup
    )


# ===== Отмена =====
@bot.message_handler(commands=['cancel'])
@bot.message_handler(func=lambda m: m.text == "❌ Отмена")
def cancel(message):
    user_states.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "Отменено.", reply_markup=main_menu())


# ===== Приём сообщений (текст) =====
@bot.message_handler(
    func=lambda m: user_states.get(m.chat.id) == "writing",
    content_types=['text']
)
def forward_text(message):
    user = message.from_user
    header = (
        f"📩 Новое сообщение\n"
        f"От: {user.first_name or ''} {user.last_name or ''}\n"
        f"Username: @{user.username if user.username else 'нет'}\n"
        f"ID: {user.id}\n"
        f"—————————————"
    )

    try:
        bot.send_message(ADMIN_ID, header)
        bot.send_message(ADMIN_ID, message.text)

        # Кнопка "Ответить"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "↩️ Ответить",
            callback_data=f"reply_{user.id}"
        ))
        bot.send_message(ADMIN_ID, "Ответить пользователю:", reply_markup=markup)

        bot.send_message(message.chat.id, "✅ Сообщение отправлено!", reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка отправки: {e}", reply_markup=main_menu())

    user_states.pop(message.chat.id, None)


# ===== Приём сообщений (медиа) =====
@bot.message_handler(
    func=lambda m: user_states.get(m.chat.id) == "writing",
    content_types=['photo', 'video', 'document', 'audio', 'voice', 'sticker']
)
def forward_media(message):
    user = message.from_user
    header = (
        f"📩 Новое сообщение (медиа)\n"
        f"От: {user.first_name or ''} {user.last_name or ''}\n"
        f"Username: @{user.username if user.username else 'нет'}\n"
        f"ID: {user.id}"
    )
    try:
        bot.send_message(ADMIN_ID, header)
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "↩️ Ответить",
            callback_data=f"reply_{user.id}"
        ))
        bot.send_message(ADMIN_ID, "Ответить пользователю:", reply_markup=markup)

        bot.send_message(message.chat.id, "✅ Сообщение отправлено!", reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}", reply_markup=main_menu())

    user_states.pop(message.chat.id, None)


# ===== Ответ от админа =====
@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def reply_to_user(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Недоступно")
        return

    target_id = int(call.data.split("_")[1])
    user_states[ADMIN_ID] = f"reply_to_{target_id}"

    bot.send_message(
        ADMIN_ID,
        f"✍️ Напиши ответ пользователю (ID: {target_id}):\n/cancel — отмена"
    )
    bot.answer_callback_query(call.id)


# ===== Отправка ответа пользователю =====
@bot.message_handler(
    func=lambda m: m.from_user.id == ADMIN_ID
    and isinstance(user_states.get(ADMIN_ID), str)
    and user_states.get(ADMIN_ID).startswith("reply_to_")
)
def send_reply(message):
    state = user_states.get(ADMIN_ID)
    target_id = int(state.replace("reply_to_", ""))

    try:
        bot.copy_message(target_id, ADMIN_ID, message.message_id)
        bot.send_message(ADMIN_ID, "✅ Ответ отправлен.")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ Ошибка: {e}")

    user_states.pop(ADMIN_ID, None)


# ===== Всё остальное =====
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(
        message.chat.id,
        "Используй кнопки меню 👇",
        reply_markup=main_menu()
    )


# ===== Запуск =====
if __name__ == "__main__":
    print("🤖 Бот запущен...")
    bot.infinity_polling()"   # Получить у @BotFather
ADMIN_ID = 123456789                    # Твой Telegram ID (узнать у @userinfobot)
CHANNEL_LINK = "https://t.me/your_channel"  # Ссылка на твой канал
CHANNEL_NAME = "Мой канал"              # Название канала

bot = telebot.TeleBot(BOT_TOKEN)

# Хранилище состояний (кто в режиме написания сообщения)
user_states = {}


# ===== ГЛАВНОЕ МЕНЮ =====
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_channel = types.KeyboardButton("📢 Ссылка на канал")
    btn_write = types.KeyboardButton("✉️ Написать мне")
    markup.add(btn_channel, btn_write)
    return markup


# ===== /start =====
@bot.message_handler(commands=['start'])
def start(message):
    text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Я бот для связи. Здесь ты можешь:\n"
        "• Получить ссылку на мой канал\n"
        "• Написать мне личное сообщение\n\n"
        "Выбери действие ниже 👇"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())


# ===== /help =====
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(
        message.chat.id,
        "Доступные команды:\n"
        "/start — главное меню\n"
        "/channel — ссылка на канал\n"
        "/write — написать сообщение\n"
        "/cancel — отменить написание",
        reply_markup=main_menu()
    )


# ===== Ссылка на канал =====
@bot.message_handler(commands=['channel'])
@bot.message_handler(func=lambda m: m.text == "📢 Ссылка на канал")
def send_channel(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"➡️ {CHANNEL_NAME}", url=CHANNEL_LINK))
    bot.send_message(
        message.chat.id,
        f"Вот ссылка на мой канал:\n{CHANNEL_LINK}",
        reply_markup=markup
    )


# ===== Написать мне =====
@bot.message_handler(commands=['write'])
@bot.message_handler(func=lambda m: m.text == "✉️ Написать мне")
def ask_message(message):
    user_states[message.chat.id] = "writing"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❌ Отмена"))
    bot.send_message(
        message.chat.id,
        "✍️ Напиши своё сообщение, и я передам его владельцу.\n\n"
        "Можно отправить текст, фото, видео или документ.",
        reply_markup=markup
    )


# ===== Отмена =====
@bot.message_handler(commands=['cancel'])
@bot.message_handler(func=lambda m: m.text == "❌ Отмена")
def cancel(message):
    user_states.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "Отменено.", reply_markup=main_menu())


# ===== Приём сообщений (текст) =====
@bot.message_handler(
    func=lambda m: user_states.get(m.chat.id) == "writing",
    content_types=['text']
)
def forward_text(message):
    user = message.from_user
    header = (
        f"📩 Новое сообщение\n"
        f"От: {user.first_name or ''} {user.last_name or ''}\n"
        f"Username: @{user.username if user.username else 'нет'}\n"
        f"ID: {user.id}\n"
        f"—————————————"
    )

    try:
        bot.send_message(ADMIN_ID, header)
        bot.send_message(ADMIN_ID, message.text)

        # Кнопка "Ответить"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "↩️ Ответить",
            callback_data=f"reply_{user.id}"
        ))
        bot.send_message(ADMIN_ID, "Ответить пользователю:", reply_markup=markup)

        bot.send_message(message.chat.id, "✅ Сообщение отправлено!", reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка отправки: {e}", reply_markup=main_menu())

    user_states.pop(message.chat.id, None)


# ===== Приём сообщений (медиа) =====
@bot.message_handler(
    func=lambda m: user_states.get(m.chat.id) == "writing",
    content_types=['photo', 'video', 'document', 'audio', 'voice', 'sticker']
)
def forward_media(message):
    user = message.from_user
    header = (
        f"📩 Новое сообщение (медиа)\n"
        f"От: {user.first_name or ''} {user.last_name or ''}\n"
        f"Username: @{user.username if user.username else 'нет'}\n"
        f"ID: {user.id}"
    )
    try:
        bot.send_message(ADMIN_ID, header)
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "↩️ Ответить",
            callback_data=f"reply_{user.id}"
        ))
        bot.send_message(ADMIN_ID, "Ответить пользователю:", reply_markup=markup)

        bot.send_message(message.chat.id, "✅ Сообщение отправлено!", reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}", reply_markup=main_menu())

    user_states.pop(message.chat.id, None)


# ===== Ответ от админа =====
@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def reply_to_user(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Недоступно")
        return

    target_id = int(call.data.split("_")[1])
    user_states[ADMIN_ID] = f"reply_to_{target_id}"

    bot.send_message(
        ADMIN_ID,
        f"✍️ Напиши ответ пользователю (ID: {target_id}):\n/cancel — отмена"
    )
    bot.answer_callback_query(call.id)


# ===== Отправка ответа пользователю =====
@bot.message_handler(
    func=lambda m: m.from_user.id == ADMIN_ID
    and isinstance(user_states.get(ADMIN_ID), str)
    and user_states.get(ADMIN_ID).startswith("reply_to_")
)
def send_reply(message):
    state = user_states.get(ADMIN_ID)
    target_id = int(state.replace("reply_to_", ""))

    try:
        bot.copy_message(target_id, ADMIN_ID, message.message_id)
        bot.send_message(ADMIN_ID, "✅ Ответ отправлен.")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ Ошибка: {e}")

    user_states.pop(ADMIN_ID, None)


# ===== Всё остальное =====
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(
        message.chat.id,
        "Используй кнопки меню 👇",
        reply_markup=main_menu()
    )


# ===== Запуск =====
if __name__ == "__main__":
    print("🤖 Бот запущен...")
    bot.infinity_polling()"   # Получить у @BotFather
ADMIN_ID = 123456789                    # Твой Telegram ID (узнать у @userinfobot)
CHANNEL_LINK = "https://t.me/your_channel"  # Ссылка на твой канал
CHANNEL_NAME = "Мой канал"              # Название канала

bot = telebot.TeleBot(BOT_TOKEN)

# Хранилище состояний (кто в режиме написания сообщения)
user_states = {}


# ===== ГЛАВНОЕ МЕНЮ =====
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_channel = types.KeyboardButton("📢 Ссылка на канал")
    btn_write = types.KeyboardButton("✉️ Написать мне")
    markup.add(btn_channel, btn_write)
    return markup


# ===== /start =====
@bot.message_handler(commands=['start'])
def start(message):
    text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Я бот для связи. Здесь ты можешь:\n"
        "• Получить ссылку на мой канал\n"
        "• Написать мне личное сообщение\n\n"
        "Выбери действие ниже 👇"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())


# ===== /help =====
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(
        message.chat.id,
        "Доступные команды:\n"
        "/start — главное меню\n"
        "/channel — ссылка на канал\n"
        "/write — написать сообщение\n"
        "/cancel — отменить написание",
        reply_markup=main_menu()
    )


# ===== Ссылка на канал =====
@bot.message_handler(commands=['channel'])
@bot.message_handler(func=lambda m: m.text == "📢 Ссылка на канал")
def send_channel(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"➡️ {CHANNEL_NAME}", url=CHANNEL_LINK))
    bot.send_message(
        message.chat.id,
        f"Вот ссылка на мой канал:\n{CHANNEL_LINK}",
        reply_markup=markup
    )


# ===== Написать мне =====
@bot.message_handler(commands=['write'])
@bot.message_handler(func=lambda m: m.text == "✉️ Написать мне")
def ask_message(message):
    user_states[message.chat.id] = "writing"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❌ Отмена"))
    bot.send_message(
        message.chat.id,
        "✍️ Напиши своё сообщение, и я передам его владельцу.\n\n"
        "Можно отправить текст, фото, видео или документ.",
        reply_markup=markup
    )


# ===== Отмена =====
@bot.message_handler(commands=['cancel'])
@bot.message_handler(func=lambda m: m.text == "❌ Отмена")
def cancel(message):
    user_states.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "Отменено.", reply_markup=main_menu())


# ===== Приём сообщений (текст) =====
@bot.message_handler(
    func=lambda m: user_states.get(m.chat.id) == "writing",
    content_types=['text']
)
def forward_text(message):
    user = message.from_user
    header = (
        f"📩 Новое сообщение\n"
        f"От: {user.first_name or ''} {user.last_name or ''}\n"
        f"Username: @{user.username if user.username else 'нет'}\n"
        f"ID: {user.id}\n"
        f"—————————————"
    )

    try:
        bot.send_message(ADMIN_ID, header)
        bot.send_message(ADMIN_ID, message.text)

        # Кнопка "Ответить"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "↩️ Ответить",
            callback_data=f"reply_{user.id}"
        ))
        bot.send_message(ADMIN_ID, "Ответить пользователю:", reply_markup=markup)

        bot.send_message(message.chat.id, "✅ Сообщение отправлено!", reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка отправки: {e}", reply_markup=main_menu())

    user_states.pop(message.chat.id, None)


# ===== Приём сообщений (медиа) =====
@bot.message_handler(
    func=lambda m: user_states.get(m.chat.id) == "writing",
    content_types=['photo', 'video', 'document', 'audio', 'voice', 'sticker']
)
def forward_media(message):
    user = message.from_user
    header = (
        f"📩 Новое сообщение (медиа)\n"
        f"От: {user.first_name or ''} {user.last_name or ''}\n"
        f"Username: @{user.username if user.username else 'нет'}\n"
        f"ID: {user.id}"
    )
    try:
        bot.send_message(ADMIN_ID, header)
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "↩️ Ответить",
            callback_data=f"reply_{user.id}"
        ))
        bot.send_message(ADMIN_ID, "Ответить пользователю:", reply_markup=markup)

        bot.send_message(message.chat.id, "✅ Сообщение отправлено!", reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}", reply_markup=main_menu())

    user_states.pop(message.chat.id, None)


# ===== Ответ от админа =====
@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def reply_to_user(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Недоступно")
        return

    target_id = int(call.data.split("_")[1])
    user_states[ADMIN_ID] = f"reply_to_{target_id}"

    bot.send_message(
        ADMIN_ID,
        f"✍️ Напиши ответ пользователю (ID: {target_id}):\n/cancel — отмена"
    )
    bot.answer_callback_query(call.id)


# ===== Отправка ответа пользователю =====
@bot.message_handler(
    func=lambda m: m.from_user.id == ADMIN_ID
    and isinstance(user_states.get(ADMIN_ID), str)
    and user_states.get(ADMIN_ID).startswith("reply_to_")
)
def send_reply(message):
    state = user_states.get(ADMIN_ID)
    target_id = int(state.replace("reply_to_", ""))

    try:
        bot.copy_message(target_id, ADMIN_ID, message.message_id)
        bot.send_message(ADMIN_ID, "✅ Ответ отправлен.")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ Ошибка: {e}")

    user_states.pop(ADMIN_ID, None)


# ===== Всё остальное =====
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(
        message.chat.id,
        "Используй кнопки меню 👇",
        reply_markup=main_menu()
    )


# ===== Запуск =====
if __name__ == "__main__":
    print("🤖 Бот запущен...")
    bot.infinity_polling()"   # Получить у @BotFather
ADMIN_ID = 123456789                    # Твой Telegram ID (узнать у @userinfobot)
CHANNEL_LINK = "https://t.me/your_channel"  # Ссылка на твой канал
CHANNEL_NAME = "Мой канал"              # Название канала

bot = telebot.TeleBot(BOT_TOKEN)

# Хранилище состояний (кто в режиме написания сообщения)
user_states = {}


# ===== ГЛАВНОЕ МЕНЮ =====
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_channel = types.KeyboardButton("📢 Ссылка на канал")
    btn_write = types.KeyboardButton("✉️ Написать мне")
    markup.add(btn_channel, btn_write)
    return markup


# ===== /start =====
@bot.message_handler(commands=['start'])
def start(message):
    text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Я бот для связи. Здесь ты можешь:\n"
        "• Получить ссылку на мой канал\n"
        "• Написать мне личное сообщение\n\n"
        "Выбери действие ниже 👇"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())


# ===== /help =====
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(
        message.chat.id,
        "Доступные команды:\n"
        "/start — главное меню\n"
        "/channel — ссылка на канал\n"
        "/write — написать сообщение\n"
        "/cancel — отменить написание",
        reply_markup=main_menu()
    )


# ===== Ссылка на канал =====
@bot.message_handler(commands=['channel'])
@bot.message_handler(func=lambda m: m.text == "📢 Ссылка на канал")
def send_channel(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"➡️ {CHANNEL_NAME}", url=CHANNEL_LINK))
    bot.send_message(
        message.chat.id,
        f"Вот ссылка на мой канал:\n{CHANNEL_LINK}",
        reply_markup=markup
    )


# ===== Написать мне =====
@bot.message_handler(commands=['write'])
@bot.message_handler(func=lambda m: m.text == "✉️ Написать мне")
def ask_message(message):
    user_states[message.chat.id] = "writing"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❌ Отмена"))
    bot.send_message(
        message.chat.id,
        "✍️ Напиши своё сообщение, и я передам его владельцу.\n\n"
        "Можно отправить текст, фото, видео или документ.",
        reply_markup=markup
    )


# ===== Отмена =====
@bot.message_handler(commands=['cancel'])
@bot.message_handler(func=lambda m: m.text == "❌ Отмена")
def cancel(message):
    user_states.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "Отменено.", reply_markup=main_menu())


# ===== Приём сообщений (текст) =====
@bot.message_handler(
    func=lambda m: user_states.get(m.chat.id) == "writing",
    content_types=['text']
)
def forward_text(message):
    user = message.from_user
    header = (
        f"📩 Новое сообщение\n"
        f"От: {user.first_name or ''} {user.last_name or ''}\n"
        f"Username: @{user.username if user.username else 'нет'}\n"
        f"ID: {user.id}\n"
        f"—————————————"
    )

    try:
        bot.send_message(ADMIN_ID, header)
        bot.send_message(ADMIN_ID, message.text)

        # Кнопка "Ответить"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "↩️ Ответить",
            callback_data=f"reply_{user.id}"
        ))
        bot.send_message(ADMIN_ID, "Ответить пользователю:", reply_markup=markup)

        bot.send_message(message.chat.id, "✅ Сообщение отправлено!", reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка отправки: {e}", reply_markup=main_menu())

    user_states.pop(message.chat.id, None)


# ===== Приём сообщений (медиа) =====
@bot.message_handler(
    func=lambda m: user_states.get(m.chat.id) == "writing",
    content_types=['photo', 'video', 'document', 'audio', 'voice', 'sticker']
)
def forward_media(message):
    user = message.from_user
    header = (
        f"📩 Новое сообщение (медиа)\n"
        f"От: {user.first_name or ''} {user.last_name or ''}\n"
        f"Username: @{user.username if user.username else 'нет'}\n"
        f"ID: {user.id}"
    )
    try:
        bot.send_message(ADMIN_ID, header)
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "↩️ Ответить",
            callback_data=f"reply_{user.id}"
        ))
        bot.send_message(ADMIN_ID, "Ответить пользователю:", reply_markup=markup)

        bot.send_message(message.chat.id, "✅ Сообщение отправлено!", reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}", reply_markup=main_menu())

    user_states.pop(message.chat.id, None)


# ===== Ответ от админа =====
@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def reply_to_user(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Недоступно")
        return

    target_id = int(call.data.split("_")[1])
    user_states[ADMIN_ID] = f"reply_to_{target_id}"

    bot.send_message(
        ADMIN_ID,
        f"✍️ Напиши ответ пользователю (ID: {target_id}):\n/cancel — отмена"
    )
    bot.answer_callback_query(call.id)


# ===== Отправка ответа пользователю =====
@bot.message_handler(
    func=lambda m: m.from_user.id == ADMIN_ID
    and isinstance(user_states.get(ADMIN_ID), str)
    and user_states.get(ADMIN_ID).startswith("reply_to_")
)
def send_reply(message):
    state = user_states.get(ADMIN_ID)
    target_id = int(state.replace("reply_to_", ""))

    try:
        bot.copy_message(target_id, ADMIN_ID, message.message_id)
        bot.send_message(ADMIN_ID, "✅ Ответ отправлен.")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ Ошибка: {e}")

    user_states.pop(ADMIN_ID, None)


# ===== Всё остальное =====
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(
        message.chat.id,
        "Используй кнопки меню 👇",
        reply_markup=main_menu()
    )


# ===== Запуск =====
if __name__ == "__main__":
    print("🤖 Бот запущен...")
    bot.infinity_polling()
