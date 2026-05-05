import telebot
import random
from datetime import datetime

TOKEN = '8747455700:AAGELyFUJ2ngZO1eGOoE0-U-C7g27X7DhEM'

bot = telebot.TeleBot(TOKEN)

# ===== КАБИНЕТЫ =====
rooms = {
    'математика': '13',
    'алгебра': '13',
    'геометрия': '13',
    'русский': '41',
    'литература': '41',
    'физика': '67',
    'история': '32',
    'химия': '26',
    'биология': '24',
    'обзр': '32',
    'обществознание': '33',
    'география': '31',
    'английский': '21/46',
    'физра': 'спорт. зал',
    'физкультура': 'спорт. зал',
    'труд': 'тех/м.лаб',
    'информатика': '1'
}

# ===== РАСПИСАНИЕ =====
schedule = {
    'понедельник': '1. Биология\n2. Русский язык\n3. Физра\n4. Английский\n5. ОБЗР\n6. Алгебра\n8. История',
    'вторник': '3. История\n4. Алгебра\n5. Химия\n6. Физика\n7. Русский язык\n8. Литература',
    'среда': '1. Русский язык\n2. Литература\n3. География\n4. Физика\n5. Геометрия\n6. Вероятность и статистика\n7. Английский',
    'четверг': '1. Литература\n2. Биология\n3. Алгебра\n4. Труд\n5. География\n6. Уравнения и неравенства (с/к)',
    'пятница': '1. Химия\n2. Физра\n3. Физика\n4. Английский / Информатика\n5. Информатика / Английский\n6. Геометрия\n7. Обществознание'
}

# ===== КНОПКИ =====
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add('🏫 Кабинеты', '📅 Расписание', '🎲 Рандомайзер')
keyboard.add('🧮 Калькулятор')


# ===== КОМАНДА СТАРТ =====
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, 'Привет! Я бот 9В класса 👋\n\nНапиши название предмета или жми кнопки👇',
                     reply_markup=keyboard)


# ===== КАБИНЕТЫ =====
@bot.message_handler(func=lambda m: m.text == '🏫 Кабинеты')
def show_rooms(m):
    text = '🏫 КАБИНЕТЫ 9В:\n\n'
    for subj, room in rooms.items():
        text += f'{subj} → каб. {room}\n'
    bot.send_message(m.chat.id, text)


# ===== РАСПИСАНИЕ (на сегодня) =====
@bot.message_handler(func=lambda m: m.text == '📅 Расписание')
def show_schedule(m):
    today = datetime.today().strftime('%A').lower()
    days = {'monday': 'понедельник', 'tuesday': 'вторник', 'wednesday': 'среда', 'thursday': 'четверг',
            'friday': 'пятница'}
    day_ru = days.get(today, 'понедельник')

    if day_ru in schedule:
        text = f'📅 РАСПИСАНИЕ НА {day_ru.upper()}:\n\n{schedule[day_ru]}'
    else:
        text = '🥳 ВЫХОДНОЙ! Отдыхай!'

    bot.send_message(m.chat.id, text)


# ===== ПОИСК КАБИНЕТА =====
@bot.message_handler(func=lambda m: m.text.lower() in rooms)
def find_room(m):
    room = rooms[m.text.lower()]
    bot.send_message(m.chat.id, f'📖 {m.text} → каб. {room}')


# ===== РАНДОМАЙЗЕР =====
@bot.message_handler(func=lambda m: m.text == '🎲 Рандомайзер')
def rand_start(m):
    bot.send_message(m.chat.id, 'Напиши два числа через пробел, например: 1 10')


@bot.message_handler(func=lambda m: ' ' in m.text and m.text.replace(' ', '').isdigit())
def do_rand(m):
    a, b = map(int, m.text.split())
    if a > b:
        a, b = b, a
    bot.send_message(m.chat.id, f'🎲 {random.randint(a, b)}')


# ===== КАЛЬКУЛЯТОР =====
@bot.message_handler(func=lambda m: m.text == '🧮 Калькулятор')
def calc_start(m):
    bot.send_message(m.chat.id, 'Напиши пример, например: 2+2 или 10*5')


@bot.message_handler(func=lambda m: any(s in m.text for s in '+-*/') and not m.text.startswith('/'))
def do_calc(m):
    try:
        allowed = '0123456789+-*/.()'
        if all(c in allowed for c in m.text):
            result = eval(m.text)
            bot.send_message(m.chat.id, f'✅ = {result}')
        else:
            bot.send_message(m.chat.id, '❌ Только цифры и знаки + - * /')
    except:
        bot.send_message(m.chat.id, '❌ Ошибка! Напиши 2+2')


# ===== ЗАПУСК =====
print('Бот 9В запущен!')
bot.infinity_polling()
