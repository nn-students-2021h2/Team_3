import requests
import json
from random import randint
from tokennn import BASE_URL

def get_num_tok():
    return str(randint(0,9))

def get_chr_tok():
    return chr(randint(44, 90))

def one_sym_gen():
    ch = randint(0, 1)
    if ch == 0:
        return get_num_tok()
    else:
        return get_chr_tok()

def id_generator():
    len = randint(10, 15)
    token = ""
    for sym in range(len):
        token += one_sym_gen()
    return token

class command:
    def __init__(self, com_name):
        self.command_name = com_name
        self.id = id_generator()

class user:
    def __init__(self, chat_id):
        self.name = 'user'
        self.chat_id = chat_id
        self.command = 'no command'
        self.dreams = 'no dreams'
        self.leader = 0
        self.status = 'registration'
        self.usr_id = 0

    def name(self, name):
        self.name = name
    def command_id(self, command):
        self.command = command
    def dreams(self, dreams):
        self.dreams = dreams
    def leader(self):
        self.leader = 1

sendd = BASE_URL + 'sendMessage'

#ввести кнопки для этого
def msg_handler(msg, chat_id):
    print(msg['text'])
    if msg['text'] == '/start':
        text = 'Добро пожаловать в игру Тайный Санта! Надеюсь, что ты знаешь правила :)\n' \
               'Если же ты не знаком с правилами игры, то смело нажимай на кнопку "Правила игры"\n' \
               'Ты хочешь зарегистрировать новую команду? Или присоединиться к друзьям?'
        requests.post(sendd, params={'chat_id': chat_id, "text": text})
    elif msg['text'] == 'Зарегистрировать команду':
        text='Замечательно! Хоу-хоу-хоу\nКак будет называться твоя команда?'
        requests.post(sendd , params = {'chat_id': chat_id, "text": text})
    elif msg['text'] == 'У меня уже есть команда!':
        text = 'Отлично, введи секретный токен своей команды!'
        requests.post(sendd, params={'chat_id': chat_id, "text": text})
    else:
         requests.post(sendd, params = {'chat_id': chat_id, "text": "Данный раздел на разработке ;) зайдите позже"})

last_update_id = None
while True:
    r = requests.get(BASE_URL + 'getUpdates', params={'offset': last_update_id, 'timeout': 10})
    response_dict = json.loads(r.text)
    for upd in response_dict["result"]:
        #регистрация пользователя
        last_update_id = upd["update_id"] + 1
        try:
            msg = upd["message"]
            chat_id = msg["chat"]["id"]
            if "text" in msg:
                last_data = msg_handler(msg, chat_id)
        except:
            print(upd)
