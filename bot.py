import telebot
from telebot import types
import sqlite3

TOKEN = '1628451769:AAF793AlM6Qzolx7dorEXlXYvl8e4JwbOe4'
bot = telebot.TeleBot(TOKEN)

sexes = ["мужчина", "женщина"]
clothes_types = ["низ", "верх", "обувь", "аксессуары"]
sizes = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL']
sneaker_sizes = ["6.5 US", "7 US", "7.5 US", "8 US", "8.5 US", "9 US", "9.5 US",
                 "10 US", "10.5 US", "11 US", "11.5 US", "12 US", "12.5 US", "13 US", "13.5 US"]
# клавиатура с полом
markup_gender = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("Мужчина")
item2 = types.KeyboardButton("Женщина")
markup_gender.add(item1, item2)


# клавиатура с размером обуви
markup_sneaker_sizes = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("6.5 US")
item2 = types.KeyboardButton("7 US")
item3 = types.KeyboardButton("7.5 US")
item4 = types.KeyboardButton("8 US")
item5 = types.KeyboardButton("8.5 US")
item6 = types.KeyboardButton("9 US")
item7 = types.KeyboardButton("9.5 US")
item8 = types.KeyboardButton("10 US")
item9 = types.KeyboardButton("10.5 US")
item10 = types.KeyboardButton("11 US")
item11 = types.KeyboardButton("11.5 US")
item12 = types.KeyboardButton("12 US")
item13 = types.KeyboardButton("12.5 US")
item14 = types.KeyboardButton("13 US")
item15 = types.KeyboardButton("13.5 US")
item16 = types.KeyboardButton("Главное меню")
markup_sneaker_sizes.add(item1, item2, item3, item4, item5, item6,
                         item7, item8, item9, item10, item11, item12, item13, item14, item15, item16)


# клавиатура с размером одежды
markup_sizes = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("XXS")
item2 = types.KeyboardButton("XS")
item3 = types.KeyboardButton("S")
item4 = types.KeyboardButton("M")
item5 = types.KeyboardButton("L")
item6 = types.KeyboardButton("XL")
item7 = types.KeyboardButton("XXL")
item8 = types.KeyboardButton("Главное меню")
markup_sizes.add(item1, item2, item3, item4, item5, item6, item7, item8)


# клавиатура с одеждой
markup_clothes = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("Низ")
item2 = types.KeyboardButton("Верх")
item3 = types.KeyboardButton("Обувь")
item4 = types.KeyboardButton("Аксессуары")
item5 = types.KeyboardButton("Главное меню")
markup_clothes.add(item1, item2, item3, item4, item5)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("Да")
item2 = types.KeyboardButton("Нет")
markup.add(item1, item2)


@bot.message_handler(commands=['start'])
def welcome(message):
    con = sqlite3.connect("clothes.db")
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE id=?",
                (message.from_user.id,))
    con.commit()
    con.close()
    stick = open("stickers/HI.tgs", 'rb')
    bot.send_sticker(message.chat.id, stick)
    bot.send_message(
        message.chat.id, 'Здравствуйте, {0.first_name}!\nЯ - <b>{1.first_name}</b>, помощник в выборе одежды!\n Укажите ваш пол.'
        .format(message.from_user, bot.get_me()), parse_mode='html',
        reply_markup=markup_gender)


@bot.message_handler(content_types=['text'])
def write(message):
    con = sqlite3.connect("clothes.db")
    cur = con.cursor()
    if message.text.lower() == 'главное меню':
        cur.execute("DELETE FROM users WHERE id=?", (message.from_user.id,))
        con.commit()
        bot.send_message(
            message.chat.id, "Укажите ваш пол", reply_markup=markup_gender)
    elif message.text.lower() in sexes:
        sex(message)
    elif message.text.lower() in clothes_types:
        if check_sex(message):
            clothes_type(message)
    elif message.text.upper() in sizes:
        if check_sex(message):
            if check_type(message):
                if cur.execute("SELECT type FROM users WHERE id=?", (message.from_user.id,)).fetchone()[0].lower() not in ['низ', 'верх']:
                    bot.send_message(
                        message.chat.id, "Данный размер не подходит для выбранного типа одежды")
                else:
                    chose(message)
    elif message.text.upper() in sneaker_sizes:
        if check_sex(message):
            if check_type(message):
                if cur.execute("SELECT type FROM users WHERE id=?", (message.from_user.id,)).fetchone()[0].lower() != 'обувь':
                    bot.send_message(
                        message.chat.id, "Данный размер не подходит для выбранного типа одежды")
                else:
                    chose(message)
    elif check_sex(message):
        if check_type(message):
            if check_size(message):
                if message.text.lower() == 'да':
                    selection(message)
                elif message.text.lower() == 'нет':
                    cur.execute("DELETE FROM users WHERE id=?",
                                (message.from_user.id,))
                    con.commit()
                    bot.send_message(
                        message.chat.id, "Укажите ваш пол", reply_markup=markup_gender)
    else:
        bot.send_message(message.chat.id, "Я вас не понимаю")


def check_sex(message):
    con = sqlite3.connect("clothes.db")
    cur = con.cursor()
    if not cur.execute("SELECT sex FROM users WHERE id=?", (message.from_user.id,)).fetchone():
        bot.send_message(message.chat.id, "Сначала выберите пол",
                         reply_markup=markup_gender)
        return False
    return True


def check_type(message):
    con = sqlite3.connect("clothes.db")
    cur = con.cursor()
    if not cur.execute("SELECT type FROM users WHERE id=?", (message.from_user.id,)).fetchone()[0]:
        bot.send_message(
            message.chat.id, "Сначала выберите тип одежды", reply_markup=markup_clothes)
        return False
    return True


def check_size(message):
    con = sqlite3.connect("clothes.db")
    cur = con.cursor()
    if not cur.execute("SELECT size FROM users WHERE id=?", (message.from_user.id,)).fetchone()[0]:
        if cur.execute("SELECT type FROM users WHERE id=?", (message.from_user.id,)).fetchone()[0] in ['низ', 'верх']:
            markup = markup_sizes
        else:
            markup = markup_sneaker_sizes
        bot.send_message(
            message.chat.id, "Сначала выберите размер одежды", reply_markup=markup)
        return False
    return True


def sex(message):  # Выбор пола
    con = sqlite3.connect("clothes.db")
    cur = con.cursor()
    ids = cur.execute("SELECT id FROM users").fetchall()
    main_id = message.from_user.id
    if (main_id,) not in ids:
        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                    (main_id, message.text, None, None))
    else:
        cur.execute("UPDATE users SET sex=? WHERE id=?",
                    (message.text, main_id))
    con.commit()
    con.close()
    bot.send_message(
        message.chat.id, "Выберите интересующий вас тип одежды", reply_markup=markup_clothes)


def clothes_type(message):  # Выбор типа одежды
    con = sqlite3.connect("clothes.db")
    cur = con.cursor()
    ids = cur.execute("SELECT id FROM users").fetchall()
    main_id = message.from_user.id
    if (main_id,) not in ids:
        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                    (main_id, None, message.text, None))
    else:
        cur.execute("UPDATE users SET type=? WHERE id=?",
                    (message.text, main_id))
    con.commit()
    con.close()
    if message.text.lower() in ['низ', 'верх']:
        bot.send_message(message.chat.id, "Выберите размер",
                         reply_markup=markup_sizes)
    elif message.text.lower() == 'обувь':
        bot.send_message(message.chat.id, "Выберите размер",
                         reply_markup=markup_sneaker_sizes)
    elif message.text.lower() == 'аксессуары':
        con = sqlite3.connect("clothes.db")
        cur = con.cursor()
        cur.execute("UPDATE users SET size=? WHERE id=?",
                    ("Not used", main_id))
        con.commit()
        text = cur.execute("SELECT sex FROM users WHERE id=?",
                           (main_id,)).fetchone()[0]
        bot.send_message(message.chat.id, f"Все параметры указаны. {text}, аксессуары. Верно?",
                         reply_markup=markup)


def chose(message):
    main_id = message.from_user.id
    con = sqlite3.connect("clothes.db")
    cur = con.cursor()
    cur.execute("UPDATE users SET size=? WHERE id=?",
                (message.text, main_id))
    text = cur.execute("SELECT * FROM users WHERE id=?", (main_id,)).fetchone()
    con.commit()
    con.close()
    bot.send_message(message.chat.id, f"Все параметры указаны. {text[1]}, {text[2]}, {text[3]}. Верно?",
                     reply_markup=markup)


def selection(message):
    main_id = message.from_user.id
    bot.send_message(message.chat.id, "Подбираем одежду",
                     reply_markup=types.ReplyKeyboardRemove())
    con = sqlite3.connect("clothes.db")
    cur = con.cursor()
    parametres = cur.execute("SELECT * FROM users WHERE id=?",
                             (main_id,)).fetchone()
    _, sex, clothes_type, size = parametres
    sex, clothes_type, size = sex.lower(), clothes_type.lower(), size.upper()
    result = cur.execute("SELECT name,photo,size FROM clothes WHERE sex=? AND type=?",
                         (sex, clothes_type)).fetchall()
    final_result = []
    for i in result:
        sizes = i[2].split(';')
        for j in sizes:
            if j == size:
                final_result.append([i[0], i[1]])
    for i in final_result:
        photo = open(i[1], 'rb')
        bot.send_photo(message.chat.id, photo, caption=i[0])


[['2 пар футболок', 'image\\male\\2packnike-tshirt.png'],
    ['ветровка наса', 'image\\male\\nasajacket.png']]


bot.polling(none_stop=True)
