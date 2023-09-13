from random import choice
from settings import *
from session import *

# Генерация рандомной карты
def generateNumbers():
    pointsFromCards = choice(list(cards.keys()))
    temp = choice(list(cards[pointsFromCards].keys()))

    return pointsFromCards, choice(cards[pointsFromCards][temp])

# Создание новой сессии/игры
def newGame(chat, user):
    gameBJ.setdefault(chat, {'user': {user: {'name': '', 'points': 0, 'cards': [],
                                             'stand': False, 'freeze': False, 'status': ''}},
                             'dealer': {'deal': {'points': 0, 'cards': [], 'status': ''}}, 'turn': 0, 'gameEnd': False})

# Проверка на туз (если туз в начале игры - +11 очков)
def getCards(chat):
    playerPoints1, firstCard = generateNumbers()
    playerPoints2, secondCard = generateNumbers()

    if playerPoints1 == 1 and gameBJ[chat]['turn'] <= 2:
        playerPoints1 += 10
    if playerPoints2 == 1 and gameBJ[chat]['turn'] <= 2:
        playerPoints2 += 10

    return playerPoints1, firstCard, playerPoints2, secondCard

# mode 1 - user, mode 0 - dealer. Для вывода карт игрока и дилера в игру.
def loadCards(chat, user, dealOrNot):
    if dealOrNot == 1:
        tempCards = gameBJ[chat]['user'][user]['cards']
    else:
        tempCards = gameBJ[chat]['dealer']['deal']['cards']
    plCards = ''
    for el in tempCards:
        plCards += f'{el}\n'

    return plCards

# Тут прописана логика дилера, а так же если игрок сглупит в начале со счетом (например player - 6, dealer - 10)
# и нажмет на кнопку stand, получим "why?" игроку в колоду (пасхалка)
def saveCards(chat, user):
    plPoints1, card1, plPoints2, card2 = getCards(chat)
    if gameBJ[chat]['turn'] <= 1:
        gameBJ[chat]['dealer']['deal']['points'] += plPoints2
        gameBJ[chat]['turn'] += 1
        gameBJ[chat]['dealer']['deal']['cards'] += [card2]
        gameBJ[chat]['user'][user]['points'] += plPoints1
        gameBJ[chat]['user'][user]['cards'] += [card1]
    else:
        if gameBJ[chat]['user'][user]['points'] < gameBJ[chat]['dealer']['deal']['points']:
            if gameBJ[chat]['user'][user]['stand']:
                gameBJ[chat]['user'][user]['cards'] += ['why?']
            else:
                gameBJ[chat]['user'][user]['points'] += plPoints1
                gameBJ[chat]['turn'] += 1
                gameBJ[chat]['user'][user]['cards'] += [card1]
        else:
            if gameBJ[chat]['user'][user]['stand']:
                gameBJ[chat]['dealer']['deal']['points'] += plPoints2
                gameBJ[chat]['turn'] += 1
                gameBJ[chat]['dealer']['deal']['cards'] += [card2]
            else:
                gameBJ[chat]['dealer']['deal']['points'] += plPoints2
                gameBJ[chat]['turn'] += 1
                gameBJ[chat]['dealer']['deal']['cards'] += [card2]
                gameBJ[chat]['user'][user]['points'] += plPoints1
                gameBJ[chat]['user'][user]['cards'] += [card1]

# Удаление игры
def removeGame(chat):
    if chat in gameBJ.keys():
        gameBJ.pop(chat)
    else:
        print('spamming! 01')

# Вывод игрока в сообщение
def loadPlayer(chat, user):
    return f'{gameBJ[chat]["user"][user]["name"]} ({gameBJ[chat]["user"][user]["points"]}): \n' \
f'{loadCards(chat, user, 1)}'

# Вывод дилера в сообщение
def loadDealer(chat, user):
    return f'Dealer ({gameBJ[chat]["dealer"]["deal"]["points"]}):\n' \
f'{loadCards(chat, user, 0)}'

# заморозить игрока (анти-спам)
def freeze(chat, user, mode):
    if chat in gameBJ.keys():
        if mode == 1:
            gameBJ[chat]['user'][user]['freeze'] = True
        if mode == 0:
            gameBJ[chat]['user'][user]['freeze'] = False
    else:
        print('spamming 02!')

# Закончить игру (для вывода сообщения о завершении игры)
def endGame(chat):
    if chat in gameBJ.keys():
        gameBJ[chat]['gameEnd'] = True
    else:
        print('spamming 06!')

# Сменить статус игрока (выиграл/проиграл/ничья)
def changeStatusPlayer(chat, user, mode):
    if chat in gameBJ.keys():
        if mode == 0:
            gameBJ[chat]['user'][user]['status'] = 'lose'
        elif mode == 1:
            gameBJ[chat]['user'][user]['status'] = 'win'
        elif mode == 2:
            gameBJ[chat]['user'][user]['status'] = 'tie'
    else:
        print('spamming 07!')

# Сменить статус дилера (дополнительная логика и защита от спама)
def changeStatusDealer(chat, user, mode):
    if chat in gameBJ.keys():
        if mode == 0:
            if gameBJ[chat]['dealer']['deal']['points'] > 21 or gameBJ[chat]['user'][user]['status'] == 'win':
                gameBJ[chat]['dealer']['deal']['status'] = 'lose'
        elif mode == 1:
            if not gameBJ[chat]['dealer']['deal']['points'] > 21 and gameBJ[chat]['user'][user]['status'] == 'lose':
                gameBJ[chat]['dealer']['deal']['status'] = 'win'
        elif mode == 2:
            gameBJ[chat]['dealer']['deal']['status'] = 'tie'
    else:
        print('spamming 07!')