import telebot
from telebot import types
import random
bot = telebot.TeleBot("Ключ от бота")

start = 221
player_number = 0
count = 0

@bot.message_handler(commands=["start"])
def hello(message):
    bot.send_message(message.chat.id, "Привет! Это Игра с конфетами.\n\
Введи команду: /button")


@bot.message_handler(commands=["button"])
def button(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Узнать правила игры")
    but2 = types.KeyboardButton("Играть!")
    markup.add(but1)
    markup.add(but2)
    bot.send_message(message.chat.id, "Нажми на нужную кнопку",
                     reply_markup=markup)


@bot.message_handler(content_types="text")
def controller(message):
    if message.text == "Узнать правила игры":
        bot.send_message(message.chat.id, "Условия игры следующие:\n\
1) На столе лежит 221 конфета. Вы играете против Меня. Ходим поочередно.\n\
2) Первый ход определяется жеребьёвкой.\n\
3) За один ход можно забрать не более чем 28 конфет, но не меньше 1.\n\
4) Все конфеты оппонента достаются сделавшему последний ход.")
        button(message)
    elif message.text == "Играть!":
        start_game(message)


def start_game(message):
    restart_game(message)
    global player_number
    bot.send_message(message.chat.id, 'Давай начнём!\n\
Происходит жеребьёвка')
    player_number = random.randint(1, 2)
    if player_number == 1:
        bot.send_message(message.chat.id, "Первым хожу я.")
        game_move_bot(message)
    else:
        bot.send_message(message.chat.id, "Первым ходите Вы!")
        game_move_player(message)


def game_move_bot(message):
    global start
    global count
    if not checkFinish():
        count += 1
        bot.send_message(
            message.chat.id, f'{count} ход: На столе сейчас лежит {start} конфет(а).')
        if start >= 28:
            candies = random.randint(1, 28)
            start -= candies
            bot.send_message(message.chat.id, f'Я возьму {candies} конфет(ы).')
            game_move_player(message)
        else:
            candies = start
            start -= candies
            bot.send_message(message.chat.id, f'Я возьму {candies} конфет(ы).')
            game_move_player(message)
    else:
        bot.send_message(
            message.chat.id, f'Игра окончена. Поздравляю! Победа за тобой!')
        button(message)


def game_move_player(message):
    global start
    global count
    if not checkFinish():
        count += 1
        bot.send_message(message.chat.id, f'{count} ход: На столе сейчас лежит {start} конфет(а).\n\
Сколько конфет Вы возьмете со стола: ')
        bot.register_next_step_handler(message, user_num_step1)
    else:
        bot.send_message(message.chat.id, f'Игра окончена. Я победил!')
        button(message)


def checkFinish():
    global start
    if start <= 0:
        return True
    else:
        return False


def user_num_step1(message):
    global start
    if start >= 28:
        user_input = message.text
        while not user_input.isdigit():
            bot.send_message(
                message.chat.id, f'{user_input} - не число! Попробуйте снова.')
            bot.send_message(
                message.chat.id, f'Сколько конфет Вы возьмете со стола: ')
            bot.register_next_step_handler(message, user_num_step1)
            user_input = num
        while int(user_input) < 1 or int(user_input) > 28:
            bot.send_message(
                message.chat.id, f'Вы должны взять хотя бы 1 конфету, но не больше 28. Попробуйте снова.')
            bot.send_message(
                message.chat.id, f'Сколько конфет Вы возьмете со стола: ')
            bot.register_next_step_handler(message, user_num_step1)
            user_input = num
            while not user_input.isdigit():
                bot.send_message(
                    message.chat.id, f'{user_input} - не число! Попробуйте снова.')
                bot.send_message(
                    message.chat.id, f'Сколько конфет Вы возьмете со стола: ')
                bot.register_next_step_handler(message, user_num_step1)
                user_input = num
    elif 0 < start and start< 28:
        user_input = message.text
        while not user_input.isdigit():
            bot.send_message(
                message.chat.id, f'{user_input} - не число! Попробуйте снова.')
            bot.send_message(
                message.chat.id, f'Сколько конфет Вы возьмете со стола: ')
            bot.register_next_step_handler(message, user_num_step1)
            user_input = num
        while int(user_input) < 1 or int(user_input) > start:
            bot.send_message(
                message.chat.id, f'Вы должны взять хотя бы 1 конфету, но не больше {start}. Попробуйте снова.')
            bot.send_message(
                message.chat.id, f'Сколько конфет Вы возьмете со стола: ')
            bot.register_next_step_handler(message, user_num_step1)
            user_input = num
            while not user_input.isdigit():
                bot.send_message(
                    message.chat.id, f'{user_input} - не число! Попробуйте снова.')
                bot.send_message(
                    message.chat.id, f'Сколько конфет Вы возьмете со стола: ')
                bot.register_next_step_handler(message, user_num_step1)
                user_input = num
    num = int(user_input)
    start -= num
    game_move_bot(message)


def restart_game(message):
    global start
    global player_number
    global count
    start = 221
    player_number = 0
    count = 0
    button(message)


bot.infinity_polling()