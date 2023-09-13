from telebot import types
from phrases import *

# создание клавиатур (lang - язык который стоит у пользователя)

def KBstartgame(lang):
    ikb = types.InlineKeyboardMarkup()
    ikb.add(types.InlineKeyboardButton(buttonBJ.get(lang), callback_data='startgame'))

    return ikb

# кнопки без перевода
KBblackjack = types.InlineKeyboardMarkup()
KBblackjack.add(types.InlineKeyboardButton('Hit', callback_data='s_hit'),
                        types.InlineKeyboardButton('Stand', callback_data='s_stand'))

def KBhelp(lang):
    ikb = types.InlineKeyboardMarkup()
    ikb.add(types.InlineKeyboardButton(inlineHelp.get(lang), callback_data='b1'))

    return ikb
def KBrules(lang):
    ikb = types.InlineKeyboardMarkup()
    ikb.add(types.InlineKeyboardButton(rulesButton.get(lang), callback_data='rules'))

    return ikb
def KBcards(lang):
    ikb = types.InlineKeyboardMarkup()
    ikb.add(types.InlineKeyboardButton(cardsButton.get(lang), callback_data='cards'))

    return ikb
def KBchoose(lang):
    ikb = types.InlineKeyboardMarkup()
    ikb.add(types.InlineKeyboardButton(rulesButton.get(lang), callback_data='rules'),
             types.InlineKeyboardButton(buttonBJ.get(lang), callback_data='startgame'))

    return ikb