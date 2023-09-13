import telebot

from keyboards import *
from settings import *
from session import *
from phrases import *
from functions import *

bot = telebot.TeleBot(tokenAPI)

# проверка закончилась ли игра, для вывода текста
def checkGame(chat, lang):
    if not gameBJ[chat]['gameEnd']:
        return phGameStarted.get(lang)
    else:
        return phGameEnd.get(lang)

# проверка какой язык стоит у пользователя
def checkLang(message):
    print(message.from_user.language_code)
    if message.from_user.language_code in start.keys():
        return message.from_user.language_code
    else:
        return mainLang

@bot.message_handler(commands=['start'])
def cmdStart(message):
    languageChat = checkLang(message)

    bot.reply_to(message, start.get(languageChat), reply_markup=KBhelp(languageChat))

@bot.message_handler(commands=['help'])
def cmdHelp(message):
    languageChat = checkLang(message)

    bot.reply_to(message, help.get(languageChat), reply_markup=KBchoose(languageChat), parse_mode='HTML')

@bot.message_handler(commands=['rules'])
def cmdRules(message):
    languageChat = checkLang(message)

    bot.reply_to(message, rules.get(languageChat), reply_markup=KBcards(languageChat), parse_mode='HTML')

@bot.message_handler(commands=['bj'])
def cmdBj(message):
    languageChat = checkLang(message)

    bot.send_message(message.chat.id,
                     cmdBJ.get(languageChat),
                     reply_markup=KBstartgame(languageChat))

@bot.callback_query_handler(lambda a: True)
def inline(query):
    global gameBJ

    languageChat = checkLang(query)

    if query.data == 'b1':
        bot.send_message(query.message.chat.id, help.get(languageChat), reply_markup=KBchoose(languageChat),
                         parse_mode='HTML')

    elif query.data == 'rules':
        bot.send_message(query.message.chat.id, rules.get(languageChat), reply_markup=KBcards(languageChat),
                         parse_mode='HTML')

    elif query.data == 'cards':
        bot.send_message(query.message.chat.id, cardsList.get(languageChat), reply_markup=KBstartgame(languageChat),
                         parse_mode='HTML')

    elif query.data == 'startgame':
        if query.from_user.id not in gameBJ.keys():
            newGame(query.from_user.id, query.from_user.id) # создание игры/сессии

            # выдача карт
            saveCards(query.from_user.id, query.from_user.id)
            saveCards(query.from_user.id, query.from_user.id)

            # проверка никнейма (в группах будет написанно Player(ID)
            if not query.message.chat.first_name == None:
                gameBJ[query.from_user.id]['user'][query.from_user.id]['name'] = query.message.chat.first_name
            elif not query.message.chat.username == None:
                gameBJ[query.from_user.id]['user'][query.from_user.id]['name'] = query.message.chat.username
            else:
                gameBJ[query.from_user.id]['user'][query.from_user.id]['name'] = f'Player{query.from_user.id}'

            # проверка на то, выиграл ли кто-то в начале игры.
            if gameBJ[query.from_user.id]['user'][query.from_user.id]['points'] == 21 and \
                    gameBJ[query.from_user.id]['dealer']['deal']['points'] == 21: # tie
                changeStatusPlayer(query.from_user.id, query.from_user.id, 2)
                changeStatusDealer(query.from_user.id, query.from_user.id, 2)
                endGame(query.from_user.id)
                bot.send_message(query.message.chat.id, gameText(query.from_user.id,
                                               query.from_user.id,
                                               checkGame(query.from_user.id, languageChat),
                                               gameBJ[query.from_user.id]['user'][query.from_user.id]['status'],
                                               gameBJ[query.from_user.id]['dealer']['deal']['status'],
                                               languageChat).get(languageChat),
                                 reply_markup=KBstartgame(languageChat))
                removeGame(query.from_user.id)

            elif gameBJ[query.from_user.id]['dealer']['deal']['points'] == 21 or gameBJ[query.from_user.id]['user'][query.from_user.id]['points'] > 21: # lose
                changeStatusPlayer(query.from_user.id, query.from_user.id, 0)
                changeStatusDealer(query.from_user.id, query.from_user.id, 1)
                endGame(query.from_user.id)
                bot.send_message(query.message.chat.id, gameText(query.from_user.id,
                                               query.from_user.id,
                                               checkGame(query.from_user.id, languageChat),
                                               gameBJ[query.from_user.id]['user'][query.from_user.id]['status'],
                                               gameBJ[query.from_user.id]['dealer']['deal']['status'],
                                               languageChat).get(
                    languageChat), reply_markup=KBstartgame(languageChat))
                removeGame(query.from_user.id)

            elif gameBJ[query.from_user.id]['user'][query.from_user.id]['points'] == 21 or gameBJ[query.from_user.id]['dealer']['deal']['points'] > 21: # win
                changeStatusPlayer(query.from_user.id, query.from_user.id, 1)
                changeStatusDealer(query.from_user.id, query.from_user.id, 0)
                endGame(query.from_user.id)
                bot.send_message(query.message.chat.id, gameText(query.from_user.id,
                                               query.from_user.id,
                                               checkGame(query.from_user.id, languageChat),
                                               gameBJ[query.from_user.id]['user'][query.from_user.id]['status'],
                                               gameBJ[query.from_user.id]['dealer']['deal']['status'],
                                               languageChat).get(
                    languageChat), reply_markup=KBstartgame(languageChat))
                removeGame(query.from_user.id)

            else:
                bot.send_message(query.message.chat.id, gameText(query.from_user.id,
                                               query.from_user.id,
                                               checkGame(query.from_user.id, languageChat),
                                               gameBJ[query.from_user.id]['user'][query.from_user.id]['status'],
                                               gameBJ[query.from_user.id]['dealer']['deal']['status'],
                                               languageChat).get(
                    languageChat), reply_markup=KBblackjack)

            print(gameBJ)

        else:
            # Если человек уже начал игру, то получим ошибку
            bot.send_message(query.message.chat.id,
                             gameStarted.get(languageChat))

    elif query.data == 's_hit':
        if query.from_user.id in gameBJ.keys() and query.from_user.id in gameBJ[query.from_user.id]['user'].keys():
            if not gameBJ[query.from_user.id]['user'][query.from_user.id]['freeze']:
                saveCards(query.from_user.id, query.from_user.id)  # выдаем карты

                bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                      text=gameText(query.from_user.id,
                                                query.from_user.id,
                                                checkGame(query.from_user.id, languageChat),
                                                gameBJ[query.from_user.id]['user'][query.from_user.id]['status'],
                                                gameBJ[query.from_user.id]['dealer']['deal']['status'],
                                               languageChat).get(languageChat),
                                      reply_markup=KBblackjack)

                # При спаме кнопками бывает такое что сессия удаляется в этом месте.
                if not query.from_user.id in gameBJ.keys():
                    print('spamming 03!')

                elif gameBJ[query.from_user.id]['user'][query.from_user.id]['points'] == 21 and gameBJ[query.from_user.id]['dealer']['deal']['points'] == 21:
                    changeStatusPlayer(query.from_user.id, query.from_user.id, 2)  # ничья
                    changeStatusDealer(query.from_user.id, query.from_user.id, 2)
                    endGame(query.from_user.id)
                    bot.edit_message_text(gameText(query.from_user.id,
                                                query.from_user.id,
                                                checkGame(query.from_user.id, languageChat),
                                                gameBJ[query.from_user.id]['user'][query.from_user.id]['status'],
                                                gameBJ[query.from_user.id]['dealer']['deal']['status'],
                                               languageChat).get(languageChat),
                                      query.message.chat.id, query.message.message_id, reply_markup=KBstartgame(languageChat))
                    removeGame(query.from_user.id)

                elif gameBJ[query.from_user.id]['dealer']['deal']['points'] == 21 or gameBJ[query.from_user.id]['user'][query.from_user.id]['points'] > 21:
                    changeStatusPlayer(query.from_user.id, query.from_user.id, 0)  # проиграл
                    changeStatusDealer(query.from_user.id, query.from_user.id, 1)  # выиграл
                    endGame(query.from_user.id)
                    bot.edit_message_text(gameText(query.from_user.id,
                                                query.from_user.id,
                                                checkGame(query.from_user.id, languageChat),
                                                gameBJ[query.from_user.id]['user'][query.from_user.id]['status'],
                                                gameBJ[query.from_user.id]['dealer']['deal']['status'],
                                               languageChat).get(languageChat),
                                      query.message.chat.id, query.message.message_id, reply_markup=KBstartgame(languageChat))
                    removeGame(query.from_user.id)

                elif gameBJ[query.from_user.id]['user'][query.from_user.id]['points'] == 21 or gameBJ[query.from_user.id]['dealer']['deal']['points'] > 21:
                    changeStatusPlayer(query.from_user.id, query.from_user.id, 1)
                    changeStatusDealer(query.from_user.id, query.from_user.id, 0)
                    endGame(query.from_user.id)
                    bot.edit_message_text(gameText(query.from_user.id,
                                                query.from_user.id,
                                                checkGame(query.from_user.id, languageChat),
                                                gameBJ[query.from_user.id]['user'][query.from_user.id]['status'],
                                                gameBJ[query.from_user.id]['dealer']['deal']['status'],
                                               languageChat).get(languageChat),
                                      query.message.chat.id, query.message.message_id, reply_markup=KBstartgame(languageChat))
                    removeGame(query.from_user.id)
                print(gameBJ)
            else:
                # Ещё одна защита от спама
                print('spamming 05!')
                bot.answer_callback_query(query.id, protectionSpam.get(languageChat))

        else:
            bot.answer_callback_query(query.id, gameNotStarted.get(languageChat))

    elif query.data == 's_stand':
        if query.from_user.id in gameBJ.keys() and query.from_user.id in gameBJ[query.from_user.id]['user'].keys():
            if not gameBJ[query.from_user.id]['user'][query.from_user.id]['freeze']:
                freeze(query.from_user.id, query.from_user.id, 1)
                gameBJ[query.from_user.id]['user'][query.from_user.id]['stand'], end = True, False
                while not end:
                    saveCards(query.from_user.id, query.from_user.id)
                    bot.edit_message_text(gameText(query.from_user.id,
                                                query.from_user.id,
                                                checkGame(query.from_user.id, languageChat),
                                                gameBJ[query.from_user.id]['user'][query.from_user.id]['status'],
                                                gameBJ[query.from_user.id]['dealer']['deal']['status'],
                                               languageChat).get(languageChat),
                                      query.message.chat.id, query.message.message_id, reply_markup=KBblackjack)
                    if not query.from_user.id in gameBJ.keys():
                        print('spamming 04!')
                        break

                    if gameBJ[query.from_user.id]['dealer']['deal']['points'] > 21:
                        changeStatusPlayer(query.from_user.id, query.from_user.id, 1)
                        changeStatusDealer(query.from_user.id, query.from_user.id, 0)
                        endGame(query.from_user.id)
                        bot.edit_message_text(gameText(query.from_user.id,
                                                query.from_user.id,
                                                checkGame(query.from_user.id, languageChat),
                                                gameBJ[query.from_user.id]['user'][query.from_user.id]['status'],
                                                gameBJ[query.from_user.id]['dealer']['deal']['status'],
                                               languageChat).get(languageChat),
                                      query.message.chat.id, query.message.message_id, reply_markup=KBstartgame(languageChat))
                        freeze(query.from_user.id, query.from_user.id, 0)
                        removeGame(query.from_user.id)
                        break

                    elif gameBJ[query.from_user.id]['user'][query.from_user.id]['points'] < gameBJ[query.from_user.id]['dealer']['deal']['points']:
                        changeStatusPlayer(query.from_user.id, query.from_user.id, 0)
                        changeStatusDealer(query.from_user.id, query.from_user.id, 1)
                        endGame(query.from_user.id)
                        bot.edit_message_text(gameText(query.from_user.id,
                                                query.from_user.id,
                                                checkGame(query.from_user.id, languageChat),
                                                gameBJ[query.from_user.id]['user'][query.from_user.id]['status'],
                                                gameBJ[query.from_user.id]['dealer']['deal']['status'],
                                               languageChat).get(languageChat),
                                      query.message.chat.id, query.message.message_id, reply_markup=KBstartgame(languageChat))
                        freeze(query.from_user.id, query.from_user.id, 0)
                        removeGame(query.from_user.id)
                        break

                    elif gameBJ[query.from_user.id]['dealer']['deal']['points'] < gameBJ[query.from_user.id]['user'][query.from_user.id]['points']:
                        continue

                    elif gameBJ[query.from_user.id]['dealer']['deal']['points'] == gameBJ[query.from_user.id]['user'][query.from_user.id]['points']:
                        changeStatusPlayer(query.from_user.id, query.from_user.id, 2)
                        changeStatusDealer(query.from_user.id, query.from_user.id, 2)
                        endGame(query.from_user.id)
                        bot.edit_message_text(gameText(query.from_user.id,
                                                query.from_user.id,
                                                checkGame(query.from_user.id, languageChat),
                                                gameBJ[query.from_user.id]['user'][query.from_user.id]['status'],
                                                gameBJ[query.from_user.id]['dealer']['deal']['status'],
                                               languageChat).get(languageChat),
                                      query.message.chat.id, query.message.message_id, reply_markup=KBstartgame(languageChat))
                        freeze(query.from_user.id, query.from_user.id, 0)
                        removeGame(query.from_user.id)
                        break

                    elif gameBJ[query.from_user.id]['dealer']['deal']['points'] > gameBJ[query.from_user.id]['user'][query.from_user.id]['points']:
                        changeStatusPlayer(query.from_user.id, query.from_user.id, 0)
                        changeStatusDealer(query.from_user.id, query.from_user.id, 1)
                        endGame(query.from_user.id)
                        bot.edit_message_text(gameText(query.from_user.id,
                                                query.from_user.id,
                                                checkGame(query.from_user.id, languageChat),
                                                gameBJ[query.from_user.id]['user'][query.from_user.id]['status'],
                                                gameBJ[query.from_user.id]['dealer']['deal']['status'],
                                               languageChat).get(languageChat),
                                      query.message.chat.id, query.message.message_id, reply_markup=KBstartgame(languageChat))
                        freeze(query.from_user.id, query.from_user.id, 0)
                        removeGame(query.from_user.id)
                        break

                    print(gameBJ)
            else:
                print('spamming 05!')
                bot.answer_callback_query(query.id, protectionSpam.get(languageChat))
        else:
            bot.answer_callback_query(query.id, gameNotStarted.get(languageChat))

bot.polling()


