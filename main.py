import telebot
from telebot import types
from io import BytesIO
import db
bot = telebot.TeleBot('5984279352:AAGi2LWnzqatf7vZP4RHMMxd__iFyfNe5Uc')

phonenumber = ''
time = ''
www = ''
oldMesId = 0
newMesId = 0
@bot.message_handler(commands=['phonenumber'])
def phone(message):
    global time
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить телефон",request_contact=True)
    time = message.text
    keyboard.add(button_phone)
    bot.send_message(message.chat.id, 'Отправьте через меню.',
                     reply_markup=keyboard)



@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        keyboard2 = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Вы успешно отправили свой номер и были записаны на прием!',reply_markup=keyboard2)
        global phonenumber
        phonenumber = str(message.contact.phone_number)
        myMessageuser(message)

        user_id = str(message.contact.user_id)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Узнать про рабочее время и адрес')
    item2 = types.KeyboardButton('Как записаться?')
    item3 = types.KeyboardButton('Свободное время')
    item4 = types.KeyboardButton('Как получить справку?')
    item5 = types.KeyboardButton('Что у вас болит?')
    item6 = types.KeyboardButton('Мои сеансы')
    markup.add(item1, item2, item3, item4, item5, item6)

    bot.send_message(message.chat.id, 'Привет, {0.first_name}.\n'
                                      'Я - индивидуальный бот Медикера Университета Нархоз!'.format(message.from_user),
                     reply_markup=markup)

    bot.send_message(message.chat.id, 'Выберите пункт из меню выше !')


@bot.message_handler(commands=['back'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Узнать про рабочее время и адрес')
    item2 = types.KeyboardButton('Как записаться?')
    item3 = types.KeyboardButton('Свободное время')
    item4 = types.KeyboardButton('Как получить справку?')
    item5 = types.KeyboardButton('Что у вас болит?')
    item6 = types.KeyboardButton('Мои сеансы')

    markup.add(item1, item2, item3, item4, item5, item6)

    bot.send_message(message.chat.id, 'Вы вернулись на главное меню'.format(message.from_user),
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Узнать про рабочее время и адрес':

            bot.send_message(message.chat.id, 'Рабочее время медикера по будним дням с 9:00 до 18:00')
            bot.send_message(message.chat.id, 'А обед у нас 13:00-14:00!\n'
                                              'А адрес можете узнать нажав снизу')
            bot.send_location(message.chat.id, 43.214424836450256, 76.87135500922092)



        elif message.text == 'Свободное время':
            markup = types.ReplyKeyboardMarkup()
            item1 = types.KeyboardButton('9:00-10:00')
            item2 = types.KeyboardButton('11:00-12:00')
            item3 = types.KeyboardButton('14:00-15:00')
            item4 = types.KeyboardButton('16:00-18:00')
            back = types.KeyboardButton('Вернуться назад:')

            markup.add(item1, item2, item3, item4, back)

            msg = bot.send_message(message.chat.id, 'Выберите удобное вам время, а я запишу и передам врачу!',
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, time_bron)


        elif message.text == 'Как записаться?':
            bot.send_message(message.chat.id,
                             'Для того что-бы записаться вам нужно нажать кнопку свободное время и выбрать удобное вам время!')


        elif message.text == 'Как получить справку?':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('У меня есть направление:')
            item2 = types.KeyboardButton('У меня нету направления:')
            back = types.KeyboardButton('Вернуться назад:')

            markup.add(item1, item2, back)

            bot.send_message(message.chat.id,
                             'У вас есть направление записанное врачом во время болезни?'.format(message.from_user),
                             reply_markup=markup)

        elif message.text == 'У меня есть направление:':
            bot.send_message(message.chat.id,
                             'Если у вас есть направление от Медикера то вам необходимо пройти по адресу Навои 310 и взять там справку.')

        elif message.text == 'У меня нету направления:':
            bot.send_message(message.chat.id,
                             'Если у вас нет направления, то вам необходимо обратиться к медикеру Нархоза и попросить направление.')


        elif message.text == 'Мои сеансы':
            sss1 = db.mySeanss(str(message.from_user.first_name))
            myText = '<strong>Мои записанные сеансы:</strong> \n'
            for iu22 in sss1:
                myText = myText+'<b>Время:</b> '+str(iu22[4]) + '\n <b>Причина визита:</b> '+str(iu22[3]) + '\n'
            bot.send_message(message.chat.id, text=myText, parse_mode='html')


        #


        elif message.text == 'Что у вас болит?':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Голова')
            item2 = types.KeyboardButton('Живот')
            item3 = types.KeyboardButton('Ангина')
            item4 = types.KeyboardButton('Температура')
            item5 = types.KeyboardButton('Пропал аппетит')
            item6 = types.KeyboardButton('Теряю сознание')
            item7 = types.KeyboardButton('Другое...')

            back = types.KeyboardButton('Вернуться назад:')

            markup.add(item1, item2, item3, item4, item5, item6, item7, back)

            bot.send_message(message.chat.id,
                             'Выберите ниже!'.format(message.from_user),
                             reply_markup=markup)





        elif message.text == 'Голова':
            bot.send_message(message.chat.id,
                             'Если у вас болит голова, попробуйте слегка помассировать область или же принять обезбаливающее и отдохнуть.')
            bot.send_message(message.chat.id, 'Если это не помогает , почитайте поподробнее:')
            bot.send_message(message.chat.id,
                             'https://msk.ramsaydiagnostics.ru/blog/chto-delat-esli-postoyanno-bolit-golova/')

        elif message.text == 'Живот':
            bot.send_message(message.chat.id,
                             'Если у вас болит живот ничего не пейте и не ешьте, лягьте в постель, измерьте температуру и вызовите скорую помощь')
            bot.send_message(message.chat.id, 'Если это не помогает , почитайте поподробнее:')
            bot.send_message(message.chat.id,
                             'https://www.14crp.by/zog/neotlozhnaya-pomoshch/chto-delat-esli-bolit-zhivot')

        elif message.text == 'Ангина':
            bot.send_message(message.chat.id,
                             'Если у вас ангина, опаласкивание рта солевым раствором немного уменьшит боль, после идите к врачу и возьмите направление и нужные лекарства')
            bot.send_message(message.chat.id, 'Если это не помогает , почитайте поподробнее:')
            bot.send_message(message.chat.id,
                             'https://medkom62.ru/uslugi/fizicheskim-licam/priem-specialistov/lor/angina.html')

        elif message.text == 'Температура':

            bot.send_message(message.chat.id,
                             'Если у вас температура выше 38 градусов в домашних условиях сбивать его не стоит, вы можете ухудшить свое состояние, примите теплый душ, \n'
                             'наденьте легкую одежду и немного поспите, а дальше посоветуйтесь с врачом.')
            bot.send_message(message.chat.id, 'Если это не помогает , почитайте поподробнее:')
            bot.send_message(message.chat.id,
                             'https://www.medicina.ru/press-tsentr/statyi/chto-delat-pri-povyshenii-temperatury/')

        elif message.text == 'Пропал аппетит':
            bot.send_message(message.chat.id,
                             'Если у вас нет аппетита к слову совсем, сдайте анализы, посмотрите не болеете ли вы ничем, как обычно аппетита нет при разных болезнях, \n'
                             'и проследите за своим состоянием, температура или другое.')
            bot.send_message(message.chat.id, 'Если это не помогает , почитайте поподробнее:')
            bot.send_message(message.chat.id, 'https://lifehacker.ru/ne-xochetsya-est/')

        elif message.text == 'Теряю сознание':
            bot.send_message(message.chat.id,
                             'Если вы внезапно чувствуете головокружение или падаете в обморок ,то в срочном порядке обратитесь к врачу, ведь его последствия могут быть, \n'
                             'плохими. Возможно из-за недостаточности крови случается это, но лучше всего предотвратить заранее.')
            bot.send_message(message.chat.id, 'Если это не помогает , почитайте поподробнее:')
            bot.send_message(message.chat.id, 'https://citilab.clinic/obmorok.php')

        elif message.text == 'Другое...':
            bot.send_message(message.chat.id, 'Если у вас другая проблема, контакты врача ниже. Обратитесь!')
            bot.send_message(message.chat.id, 'Telegram: @yryssdaulet , \n'
                                              'WhatsApp: +77762153287')

        elif message.text == 'Свободное время':
            markup = types.ReplyKeyboardMarkup()
            item1 = types.KeyboardButton('9:00-10:00')
            item2 = types.KeyboardButton('11:00-12:00')
            item3 = types.KeyboardButton('14:00-15:00')
            item4 = types.KeyboardButton('16:00-18:00')
            back = types.KeyboardButton('Вернуться назад:')

            markup.add(item1, item2, item3, item4, back)

            msg = bot.send_message(message.chat.id, 'Выберите удобное вам время, а я запишу и передам врачу!',
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, time_bron)

        elif message.text == 'Вернуться назад:':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Узнать про рабочее время и адрес')
            item2 = types.KeyboardButton('Как записаться?')
            item3 = types.KeyboardButton('Свободное время')
            item4 = types.KeyboardButton('Как получить справку?')
            item5 = types.KeyboardButton('Что у вас болит?')

            markup.add(item1, item2, item3, item4, item5)

            bot.send_message(message.chat.id, 'Вы вернулись на главное меню'.format(message.from_user),
                             reply_markup=markup)
        elif message.id == oldMesId+3:
            global www
            www = message.text

            createNewSeans(message)


def time_bron(message):
    if message.text == '9:00-10:00':
        # bot.send_message(message.chat.id, text='Нажмите на кнопку и отправьте номер')
        phone(message)

    elif message.text == '11:00-12:00':
        # bot.send_message(message.chat.id, text='Нажмите на кнопку и отправьте номер')
        phone(message)


    elif message.text == '14:00-15:00':
        # bot.send_message(message.chat.id,text='Нажмите на кнопку и отправьте номер')
        phone(message)


    elif message.text == '16:00-18:00':
        # bot.send_message(message.chat.id, text='Нажмите на кнопку и отправьте номер')
        phone(message)

def myMessageuser(message):
    global oldMesId
    bot.send_message(message.chat.id, text='Напишите причину вашего визита?(Детали)')
    oldMesId = message.id
    # createNewSeans(message)

def createNewSeans(message):
    # print(message.text)
    print(www)
    print(phonenumber)
    print(time)
    print(message.from_user.first_name)
    db.newJob(myName=message.from_user.first_name, myNomer=phonenumber,myTime=time,muMesage=www)
    bot.send_message(message.chat.id, 'Вот наш адрес, приходите по нему по выбранному времени')
    bot.send_location(message.chat.id, 43.214424836450256, 76.87135500922092)
    with open('qwe.pdf', "rb") as misc:
        f = misc.read()
    bot.send_document(message.chat.id, f, caption='Перед входом покажите этот талон')
    opros(message)


def opros(message):
    markup1 = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text='Да, я хочу на главное меню' , callback_data='yes')
    item2 = types.InlineKeyboardButton(text='Нет, я закончил, я ухожу!', callback_data='no')
    markup1.add(item1,item2)

    bot.send_message(message.chat.id, text='Вы хотите вернуться на главное меню?', reply_markup=markup1)


@bot.callback_query_handler(func=lambda call: True)
def poka(call):
    if call.data == 'yes':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Узнать про рабочее время и адрес')
        item2 = types.KeyboardButton('Как записаться?')
        item3 = types.KeyboardButton('Свободное время')
        item4 = types.KeyboardButton('Как получить справку?')
        item5 = types.KeyboardButton('Что у вас болит?')
        item6 = types.KeyboardButton('Мои сеансы')

        markup.add(item1, item2, item3, item4, item5, item6)

        bot.send_message(call.message.chat.id, 'Вы вернулись на главное меню'.format(call.message.from_user),
                         reply_markup=markup)

    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'Желаю скорейшего выздоровления, пока!')
        bot.send_message(call.message.chat.id, 'Если вы хотите заново начать \n /start')


bot.polling()
