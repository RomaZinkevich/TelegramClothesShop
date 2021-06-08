import telebot
from telebot import types
import sqlite3

spisok = [('Кофты',), ('Спортивки',),
          ('Футболки',), ("Кроссовки")]
sizes = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', ]
sneaker_sizes = ["6.5 US", "7 US", "7.5 US", "8 US", "8.5 US", "9 US", "9.5 US",
                 "10 US", "10.5 US", "11 US", "11.5 US", "12 US", "12.5 US", "13 US", "13.5 US", ]
TOKEN = '1640222828:AAG1OHmbAc6NfjgrmCZCKS-2bZOfxHhKfdI'
bot = telebot.TeleBot(TOKEN)
FLAG = False


@bot.message_handler(commands=['start'])
def welcome(message):
    stick = open("stickers/HI.tgs", 'rb')
    bot.send_sticker(message.chat.id, stick)

    # клавиатура у ввода
    markup_gender = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Мужчина")
    item2 = types.KeyboardButton("Женщина")
    markup_gender.add(item1, item2)

    bot.send_message(
        message.chat.id, 'Здравствуйте, {0.first_name}!\nЯ - <b>{1.first_name}</b>, помощник в выборе одежды!\n Укажите ваш пол.'
        .format(message.from_user, bot.get_me()), parse_mode='html',
        reply_markup=markup_gender)


@bot.message_handler(content_types=['text'])
def write(message):
    markup_gender = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Мужчина")
    item2 = types.KeyboardButton("Женщина")
    markup_gender.add(item1, item2)
    if message.chat.type == 'private':
        userid = message.from_user.id
        typ = False
        main = types.KeyboardButton("Главное меню")

        markup_clothes = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Футболки")
        item2 = types.KeyboardButton("Кофты")
        item3 = types.KeyboardButton("Спортивки")
        item4 = types.KeyboardButton("Кроссовки")
        markup_clothes.add(item1, item2, item3, item4, main)

        markup_size_sneakers = types.ReplyKeyboardMarkup(
            resize_keyboard=True)
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
        markup_size_sneakers.add(item1, item2, item3, item4, item5, item6,
                                 item7, item8, item9, item10, item11,
                                 item12, item13, item14, item15, main)

        markup_size = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("XXS")
        item2 = types.KeyboardButton("XS")
        item3 = types.KeyboardButton("S")
        item4 = types.KeyboardButton("M")
        item5 = types.KeyboardButton("L")
        item6 = types.KeyboardButton("XL")
        item7 = types.KeyboardButton("XXL")
        markup_size.add(item1, item2, item3, item4,
                        item5, item6, item7, main)

        con = sqlite3.connect("clothes.db")
        cur = con.cursor()
        ids = cur.execute("""SELECT userid from users""").fetchall()

        if message.text == 'Мужчина' or message.text == 'Женщина':
            if (userid,) not in ids:
                cur.execute("""INSERT INTO users VALUES(?,?,?,?,?)""",
                            (userid, message.text, False, False, ''))
            else:
                standes = cur.execute(
                    """UPDATE users SET gender = ? WHERE userid = ?""", (message.text, userid))
            con.commit()
            con.close()
            bot.send_message(
                message.chat.id, 'Отлично! Пол указали. Какая одежда вам нужна?', reply_markup=markup_clothes)
        elif (userid,) not in ids:
            bot.send_message(
                message.chat.id, 'Извините, я вас не понимаю 😢')
        else:
            con = sqlite3.connect("clothes.db")
            cur = con.cursor()
            typee = cur.execute(
                """SELECT type from users where userid=?""", (userid,)).fetchone()
            if message.text == 'Футболки' or message.text == 'Кофты' or message.text == 'Спортивки':
                standes = cur.execute(
                    """UPDATE users SET type = ?,size=0 WHERE userid = ?""", (message.text, userid))
                bot.send_message(
                    message.chat.id, 'Принято')
                bot.send_message(
                    message.chat.id, 'Отлично! Давай выберем размер', reply_markup=markup_size)
                con.commit()
            elif message.text == 'Кроссовки':
                standes = cur.execute(
                    """UPDATE users SET type = ?,size=0 WHERE userid = ?""", (message.text, userid))
                bot.send_message(
                    message.chat.id, 'Принято')
                bot.send_message(
                    message.chat.id, 'Отлично! Давай выберем размер', reply_markup=markup_size_sneakers)
                con.commit()
            elif message.text not in spisok + sizes + sneaker_sizes:
                bot.send_message(
                    message.chat.id, 'Извините, я вас не понимаю 😢')
            if typee != (0,) and message.text in sizes:
                standes = cur.execute(
                    """UPDATE users SET size = ? WHERE userid = ?""", (message.text, userid))
                bot.send_message(
                    message.chat.id, 'Принял')
                con.commit()
                con.close()
                chose(userid, message.chat.id)
            elif typee == ('Кроссовки',) and message.text in sneaker_sizes:
                standes = cur.execute(
                    """UPDATE users SET size = ? WHERE userid = ?""", (message.text, userid))
                bot.send_message(
                    message.chat.id, 'Принял')
                con.commit()
                con.close()
                chose(userid, message.chat.id)
            if message.text == "Главное меню":
                bot.send_message(
                    message.chat.id, "Укажите ваш пол", reply_markup=markup_gender)

        # except Exception as e:
        #     print(e)
        #     bot.send_message(
        #         message.chat.id, 'Упс... Что-то пошло не так. Попробуй написать /start')


def chose(userid, msgid):
    con = sqlite3.connect("clothes.db")
    cur = con.cursor()
    users = cur.execute(
        """SELECT * FROM users WHERE userid=? """, (userid,)).fetchone()
    clothess = cur.execute(
        """SELECT * FROM clothe WHERE type=?""", (users[2],)).fetchall()
    for i in clothess:
        if users[1] in i[3] and users[3] in i[2]:
            sdi = cur.execute(
                """SELECT clothes FROM users WHERE userid=?""", (userid,)).fetchone()
            if not sdi[0]:
                sd = cur.execute(
                    """UPDATE users SET clothes=? WHERE userid=?""", ((i[0] + ":" + i[4]), userid))
            elif str(i[0]) not in sdi[0]:
                sd = cur.execute(
                    """UPDATE users SET clothes=? WHERE userid=?""", ((sdi[0] + ";" + str(i[0]) + ":" + i[4]), userid))
    sdi = cur.execute(
        """SELECT clothes FROM users WHERE userid=?""", (userid,)).fetchone()
    if not sdi:
        bot.send_message(
            message.chat.id, "Похоже ничего по вашим требованиям не найдено")
    else:
        sdi = sdi[0].split(";")
        for i in sdi:
            i = i.split(":")
            msg, photo = i[0], open(i[1], 'rb')
            bot.send_message(msgid, msg)
            print(photo)
            bot.send_photo(msgid, photo)

    con.commit()
    con.close()


bot.polling(none_stop=True)
