from functions import *

# Все фразы делал через словарь, его можно дополнять разными языками доступными в телеграмме.

help = {'ru': '''
<b>Список команд</b>:
    /bj - Играть Blackjack (SinglePlayer)
    /help - Список команд
    /rules - Правила игры
    ''',
    'uk': '''
<b>Перелік команд</b>:
    /bj - Грати Blackjack (SinglePlayer)
    /help - Перелік команд
    /rules - Правила гри
    ''',
    'en': '''
<b>List of commands:</b>
    /bj - Play Blackjack
    /help - list of commands
    /rules - rules of the game
    '''}

rules = {
    'ru': '''   <b>Rules Blackjack</b>
    Блэкджек также известен как «21». Суть игры проста: набрать 21 очко или больше, чем на руках у дилера, но ни в коем случае не больше 21. 
    
    Если игрок собирает больше 21, он «сгорает». В случае ничьи игрок и дилер остаются при своих. Чтобы узнать значения карт, нажмите на кнопку.
''',
    'uk': '''   <b>Rules Blackjack</b>
    Блекджек також відомий як "21". Суть гри проста: набрати 21 очко або більше, ніж на руках дилера, але в жодному разі не більше 21.
    
    Якщо гравець збирає більше 21, він згорає. У разі нічиї гравець і дилер залишаються при своїх. Щоб дізнатися про значення карт, натисніть кнопку.''',
    'en': '''   <b>Rules Blackjack</b>
    Blackjack is also known as "21". The essence of the game is simple: score 21 points or more than the dealer's hand, but in no case more than 21.
    
    If a player collects more than 21, he "burns out". In case of a draw, the player and the dealer remain on their own. To find out the meanings of the cards, click on the button.
    '''
}

cardsButton = {
    'ru': 'Карты',
    'uk': 'Карти',
    'en': 'Cards'
}

start = {
    'ru': 'Добро пожаловать! Язык - RU',
    'uk': 'Ласкаво просимо! Мова - UA',
    'en': 'Welcome! Language - EN'
}

inlineHelp = {
    'ru': 'Помощь',
    'uk': 'Допомога',
    'en': 'Help'
}

cmdBJ = {
    'ru': 'Blackjack singleplayer. Нажмите кнопку чтобы начать!',
    'uk': 'Blackjack singleplayer. Натисніть на кнопку щоб почати!',
    'en': 'Blackjack singleplayer. Press the button to start!'
}

buttonBJ = {
    'ru': 'Играть',
    'uk': 'Грати',
    'en': 'Play'
}

protectionSpam = {
    'ru': 'Сработала защита от спама.',
    'uk': 'Спрацював захист від спама.',
    'en': 'Spam protection worked'
}

gameStarted = {
    'ru': 'Игра уже идёт!',
    'uk': 'Гра вже йде!',
    'en': 'Game already started!'
}

gameNotStarted = {
    'ru': 'Вы не начали игру!',
    'uk': 'Ви ще не почали гру!',
    'en': 'Game is not started!'
}

joinGame = {
    'ru': 'Присоедениться',
    'uk': 'Приєднатися',
    'en': 'Join'
}

startButton = {
    'ru': 'Начать',
    'uk': 'Почати',
    'en': 'Start'
}

rulesButton = {
    'ru': 'Правила',
    'uk': 'Правила',
    'en': 'Rules'
}

cardsList = {
    'ru': '''<b>У каждой карты есть 4 масти. Это ♥ — черви, ♦ — бубны, ♠ — пики, ♣ — трефы (крести). Список карт и сколько очков даёт определенная карта:</b>
    
King (Король), Queen (Королева), Jack (Валет), Ten (Десять)- 10 очков
Nine (Девять) - 9 очков
Eight (Восемь) - 8 очков
Seven (Семь) - 7 очков
Six (Шесть) - 6 очков
Five (Пять) - 5 очков
Four (Четыре) - 4 очков
Three (Три) - 3 очков
Two (Два) - 2 очков
Ace (Туз) - 1/11 очков

В случае если туз падает в начале игры, то игроку дается 11 очков. А если посреди игры, то это 1 очко. Приятной игры в Blackjack!''',

    'uk': '''<b>Кожна карта має 4 масти. Це ♥ — черві, ♦ бубни, ♠ — піки, ♣ — трефи (хрести). Список карт та скільки поінтів дає певна карта:</b>
    
King (Король), Queen (Королева), Jack (Валет), Ten (Десять) - 10 поінтів
Nine (Дев'ять) – 9 понтів
Eight (Вісім) – 8 поінтів
Seven (Сім) – 7 поінтів
Six (Шість) – 6 поінтів
Five (П'ять) – 5 поінтів
Four (Чотири) - 4 поінтів
Three (Три) - 3 поінтів
Two (Два) – 2 поінтів
Ace (Туз) – 1/11 поінтів

Якщо туз падає на початку гри, гравцю дається 11 поінтів. А якщо серед гри, то це один поінтів. Приємної ігри у Blackjack!''',
    'en': '''<b>Each card has 4 suits. These are ♥ - hearts, ♦ - diamonds, ♠ - spades, ♣ - clubs (crosses). List of cards and how many points each card gives:</b>
    
King (King), Queen (Queen), Jack (Jack), Ten (Ten) - 10 points
Nine (Nine) - 9 points
Eight (Eight) - 8 points
Seven (Seven) - 7 points
Six (Six) - 6 points
Five (Five) - 5 points
Four (Four) - 4 points
Three (Three) - 3 points
Two (Two) - 2 points
Ace (Ace) - 1/11 points

If the ace falls at the beginning of the game, then the player is given 11 points. And if in the middle of the game, then this is 1 point. Have fun playing Blackjack!'''
}

phGameEnd = {
    'ru': 'Игра окончена!',
    'uk': 'Гра закінчена!',
    'en': 'Game is end!'
}

phGameStarted = {
    'ru': 'Игра началась!',
    'uk': 'Гра почалась!',
    'en': 'Game is started!'
}

phrases_winner = {
    'ru': 'Победитель - ',
    'uk': 'Переможець - ',
    'en': 'Winner - '
}

phrases_loser = {
    'ru': 'Неудачник - ',
    'uk': 'Невдаха - ',
    'en': 'Loser - '
}

phrases_tie = {
    'ru': 'Ничья! ',
    'uk': 'Нічия! ',
    'en': 'Tie! '
}

removingGame = {
    'ru': 'Удаление игры...',
    'uk': 'Видалення гри...',
    'en': 'Removing game...'
}

def gameText(chat, user, checker, pStatus, dStatus, lang):
    playerPrefix = ''
    dealerPrefix = ''
    if pStatus == 'win':
        playerPrefix = phrases_winner.get(lang)
    elif pStatus == 'lose':
        playerPrefix = phrases_loser.get(lang)
    elif pStatus == 'tie':
        playerPrefix = phrases_tie.get(lang)

    if dStatus == 'win':
        dealerPrefix = phrases_winner.get(lang)
    elif dStatus == 'lose':
        dealerPrefix = phrases_loser.get(lang)
    elif dStatus == 'tie':
        dealerPrefix = phrases_tie.get(lang)

    return {
        'ru': f'''{checker}
{playerPrefix}{loadPlayer(chat, user)}


{dealerPrefix}{loadDealer(chat, user)}''',
        'uk': f'''{checker}
{playerPrefix}{loadPlayer(chat, user)}

{dealerPrefix}{loadDealer(chat, user)}
''',
        'en': f'''{checker}
{playerPrefix}{loadPlayer(chat, user)}

{dealerPrefix}{loadDealer(chat, user)}
'''

    }
