import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.types import CallbackQuery
import eyed3
import os
import datetime

from humanfriendly.terminal import message
from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC







from Config import *
from SQL import premium_time_one_day, time_one_day, Premium_DeleteUser_db, Perehod_user, \
    Premium_Koin_dovnload, Premium_Koin_Save, Koin_Save, Koin_dovnload, ShowUsers_db, Proverka1_db, \
    Proverka_AddUser_db, AddUser_db, DeleteUser_db, Premium_ShowUsers_db, Premium_Proverka1_db, Premium_AddUser_db, \
    Koin_Save_in_operation, Premium_Koin_Save_in_Operation, otzovik_save, otzovik_Proverka, ShowUsers_otzovik_db, \
    Delete_otzov, title_save, Show_title, artist_save, Show_artist, photo_status_save, Show_photo_status, file_id_save, Show_file_id, peremen, \
    Delete_peremen, Show_photo_path, photo_path_save, delete_message_0_save, Show_delete_message_0, delete_message_1_save, Show_delete_message_1, \
    delete_message_2_save, Show_delete_message_2, photo_otprav_save, Show_photo_otprav, Rasolat, Public_Otzov_save, Public_otzov, Show_public_otzov, \
    Public_Otzov_message_id, Show_public_data_otzov, Delete_otzov_data, delete_message_admin_save, Show_delete_message_admin




Nomer_Stroki = 0
id = 0
id_user = None
title = '❌'
artist = '❌'
svobodno = True
Premium_Status = False
photo_status = 0

text = '😕 Пока занято \n\nКто то до сих пор изменяет свой трек, придется еще чуть чуть подождать!\n\n' \
       '🔄 Через некоторое время нажмите кнопку обновить!\n\n❗️ Если очень долго занято, попробуйте перезайти в бота!'
text1 = ''
START_TEXT = '''<strong>
🥷 Добро пожаловать! 🥷

~~~~~~~~~~~

🎹 Этот бот меняет тэги у песен в телеграме:

- название

- имя исполнителя

- обложка

- убирает приписку .mp3 в конце

‼️ Бот доступен любому желающему, достаточно просто отправить боту свою песню в виде файла (желательно mp3 формата) ‼️

~~~~~~~~~~~

📝 Возможности бота:

- Профиль пользователя, нажмите - /profile, там можете найти отзывы и магазин

- Отзывы написаны реальными пользователями бота (у некоторых есть ссылки на тг аккаунты), там же можете написать отзыв и вы

- Магазин пока еще в разработке, в нем будет осуществляться покупка койнов (1 койн = 1 переименование песни)

- К переименованию по умолчанию доступно 300 песен в месяц (каждое первое число месяца они обовляются + в будущем можно будет их докупать)

- При сохранении переименованного трека на устройство, файл сохраняет новое название

~~~~~~~~~~~

📨 По любым вопросам пишите разработчику - @HakerMac</strong>
'''





storage = MemoryStorage()


#mp3 menatel
#bot = Bot(token=TOKEN_HakMuz_Mp3_bot)

#tester
bot = Bot(token=TOKEN_tester_bot)


dp = Dispatcher(bot=bot, storage=storage)






class Audio_ID(StatesGroup):
    Title = State()
    Artist = State()
    Photo = State()

class Gotovo_trek(StatesGroup):
    Gotovo = State()

class AddUsers(StatesGroup):
    addState_ID = State()
    addState_Nick = State()

class DeleteUsers(StatesGroup):
    deleteState = State()

class ShowUsers(StatesGroup):
    Show = State()

class Koin_operation(StatesGroup):
    Koin_oper_nomer = State()
    Koin_oper_save = State()

class Premium_Koin_operation(StatesGroup):
    Prem_Koin_oper_nomer = State()
    Prem_Koin_oper_save = State()

class Otzovik_state(StatesGroup):
    Otzovik_State = State()
    Otzovik_Anon = State()


class Otzov_moder(StatesGroup):
    Moder_username = State()
    Moder_id_user = State()
    Moder_otzov_text = State()
    Moder_delete = State()


class Rasoslat(StatesGroup):
    rasoslat = State()

class none(StatesGroup):
    none1 = State()




# Выводит информацию о боте
@dp.message_handler(commands=['start'])
async def Start_start(message: types.Message):
    global START_TEXT

    await peremen()

    data = await Proverka1_db(message.from_user.id)

    if data is not None:
        ...

    else:
        data1 = await Premium_Proverka1_db(message.from_user.id)

        if data1 is not None:
            ...

        else:
            nick_user = f'@{message.from_user.username}'
            id_user = message.from_user.id
            Koin = 300

            await AddUser_db(nick_user, id_user, Koin)


    await message.answer(START_TEXT, parse_mode='HTML')
    await bot.send_message(chat_id="-1002238366836", text=f'Пользователь @{message.from_user.username} (tg://openmessage?user_id={message.from_user.id} ) только что запустил бота командой старт!')







###################################################################
# Блок админа и операция с койнами


# Команда /admin, добавляет инлайн кнопки
@dp.message_handler(commands=['admin'])
async def handle_admin_command(message: Message):
    global admin, ikb
    # Устанавливаем соединение с базой данных
    # conn = sqlite3.connect('DataBaseUsers.sql')
    # cursor = conn.cursor()
    #
    # # Выполняем запрос для проверки наличия номера в третьем столбце
    # cursor.execute("SELECT * FROM users WHERE id_user = ?", (message.from_user.id,))
    # result_curr = cursor.fetchall()

    if message.from_user.id in admin:
        ikb = InlineKeyboardMarkup(row_width=2)
        button_add = InlineKeyboardButton('➕ Добавить человека', callback_data='add_user')
        button_delete = InlineKeyboardButton('🗑 Удалить человека', callback_data='delete_user')
        button_spisok = InlineKeyboardButton('📋 Пользователи', callback_data='spisok_user')
        button_prem_spisok = InlineKeyboardButton('📋 Премиум пользователи', callback_data='spisok_prem_user')
        button_koin_uprav = InlineKeyboardButton('Операции с койнами', callback_data='koin_operation')
        button_prem_koin_uprav = InlineKeyboardButton('Операции с премиум койнами', callback_data='prem_koin_operation')
        button_Rasoslat = InlineKeyboardButton('Рассылка', callback_data='Rasoslat_operation')
        ikb.add(button_add, button_delete, button_spisok, button_prem_spisok, button_koin_uprav, button_prem_koin_uprav, button_Rasoslat)
        await bot.send_message(chat_id=message.from_user.id, text='🤔 Выберите действие:', reply_markup=ikb)
    elif svobodno == True and message.from_user.id not in admin:
        await bot.send_message(chat_id=message.from_user.id, text='😕 Вы не админ!')

    await bot.send_message(chat_id="-1002238366836",
                           text=f'Пользователь @{message.from_user.username} только что ввел команду /admin!')






# Добавление премиум пользователя в базу данных(ID и Nickneim)
@dp.message_handler(state=AddUsers.addState_ID)
async def user_id(message: types.Message, state: FSMContext):
    global id_user

    id_user = message.text.strip()

    data = await Proverka_AddUser_db(id_user)

    if data is None:
        await bot.send_message(message.chat.id, "Введите никнейм пользователя:")
        await AddUsers.addState_Nick.set()

    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('📋 Список пользователей', callback_data='spisok_prem_user'))
        await bot.send_message(message.chat.id, "Пользователь уже есть в базе данных", reply_markup=markup)
        await state.finish()






@dp.message_handler(state=AddUsers.addState_Nick)
async def user_nick(message: types.Message, state: FSMContext):
    global id_user, Premium_Koin

    nick_user = message.text
    Premium_Koin = 600

    await DeleteUser_db(id_user)

    await Premium_AddUser_db(nick_user, id_user, Premium_Koin)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('📋 Список пользователей', callback_data='spisok_prem_user'))
    await bot.send_message(chat_id=message.from_user.id, text="Пользователь добавлен успешно!", reply_markup=markup)

    await state.finish()





# Удаление премиум пользователя
@dp.message_handler(state=DeleteUsers.deleteState)
async def delete_user(message: types.Message, state: FSMContext):
    global id_user1, nickname1

    id_user1 = message.text
    nickname1 = await Perehod_user(id_user1)
    Koin = 300

    data = await Premium_DeleteUser_db(id_user1)

    if data is None:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('📋 Список обычных челов', callback_data='spisok_user'),
                   types.InlineKeyboardButton('📋 Список премиумов челов', callback_data='spisok_prem_user'))
        await bot.send_message(message.chat.id, "Пользователя нет в базе данных", reply_markup=markup)
    else:
        await AddUser_db(nickname1, id_user1, Koin)

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('📋 Список обычных челов', callback_data='spisok_user'),
                   types.InlineKeyboardButton('📋 Список премиумов челов', callback_data='spisok_prem_user'))

        await bot.send_message(message.chat.id, "Пользователь успешно удален!", reply_markup=markup)

    await state.finish()



# Показать пользователей
async def show_users(message: types.Message, page=0):
    global Nomer_Stroki

    users = await ShowUsers_db()
    user_ids = await Rasolat()

    info = ''
    Nomer_Stroki = page * 10 + 1
    start_index = page * 10
    end_index = start_index + 10
    buttons_row = []

    current_users = users[start_index:end_index]

    try:
        for el in current_users:
            info += f'{Nomer_Stroki}) Никнейм: {el[1]}, \n  - ID: {el[2]}\n - Койн: {el[3]}\n\n'
            Nomer_Stroki += 1


        show_users_btn = types.InlineKeyboardMarkup()
        if page > 0:
            buttons_row.append(types.InlineKeyboardButton('👈 Назад', callback_data=f'admin_nazad_stranica_{page - 1}'))

        if end_index < len(users):
            buttons_row.append(types.InlineKeyboardButton('Далее 👉', callback_data=f'admin_next_stranica_{page + 1}'))

        if buttons_row:
            show_users_btn.row(*buttons_row)

        sent_message_admin = await bot.send_message(message.chat.id,
                                                text=f'⚙️ Управляйте "страницами" кнопками назад и далее (на одной "странице" выводятся только 10 пользователей)\n\n📒 Пользователи(Всего: {len(user_ids)}):\n\n{info}',
                                                reply_markup=show_users_btn)
        saved_message_id_admin = sent_message_admin.message_id
        await delete_message_admin_save(message.chat.id, saved_message_id_admin)

    except:
        await message.answer('- Обычных пользователей нет!')





# Показать премиум пользователей
async def Prem_show_users(message: types.Message):
    global Nomer_Stroki

    users = await Premium_ShowUsers_db()

    info = ''
    Nomer_Stroki = 1

    try:
        for el in users:
            info += f'{Nomer_Stroki}) Никнейм: {el[1]}, \n ID: {el[2]}, \n Премиум койн: {el[3]}\n\n'
            Nomer_Stroki += 1

        await message.answer(info)
    except:
        await message.answer('- Премиум пользователей нет!')




# обновление койнов каждый месяц
async def time_obnul_one():
    while True:
        today = datetime.datetime.now()
        if today.day == 1:
            await premium_time_one_day()
            await time_one_day()

        await asyncio.sleep(3600) # койны обновятся в течение часа




# Операции с обычными койнами
async def Koin_Operations(message: types.Message):
    global Nomer_Stroki

    users = await ShowUsers_db()

    info = ''
    Nomer_Stroki = 1

    try:
        for el in users:
            info += f'{Nomer_Stroki}) Никнейм: {el[1]}, \n ID: {el[2]}, \n Койн: {el[3]}\n\n'
            Nomer_Stroki += 1

        await message.answer(info)
    except:
        await message.answer('- Обычных пользователей нет!')

    await message.answer('Введите ID пользователя')

    await Koin_operation.Koin_oper_nomer.set()




@dp.message_handler(state=Koin_operation.Koin_oper_nomer)
async def Koin_Operations_nomer(message: types.Message):
    global id_input_user


    id_input_user = int(message.text)
    await message.answer('Введите новое количество койнов:')
    await Koin_operation.next()




@dp.message_handler(state=Koin_operation.Koin_oper_save)
async def Koin_operation_Save(message: types.Message, state: FSMContext):
    global id_input_user

    new_Koin = message.text

    await Koin_Save_in_operation(int(new_Koin), id_input_user)

    await message.answer('Койны успешно обновлены')

    await state.finish()




# Операции с премиум койнами
async def Premium_Koin_Operations(message: types.Message):
    global Nomer_Stroki

    users = await Premium_ShowUsers_db()

    info = ''
    Nomer_Stroki = 1

    try:
        for el in users:
            info += f'{Nomer_Stroki}) Никнейм: {el[1]}, \n ID: {el[2]}, \n Премиум койн: {el[3]}\n\n'
            Nomer_Stroki += 1

        await message.answer(info)
    except:
        await message.answer('- Премиум пользователей нет!')

    await message.answer('Введите ID пользователя')

    await Premium_Koin_operation.Prem_Koin_oper_nomer.set()





@dp.message_handler(state=Premium_Koin_operation.Prem_Koin_oper_nomer)
async def Premium_Koin_Operations_nomer(message: types.Message):
    global Prem_id_input_user


    Prem_id_input_user = int(message.text)
    await message.answer('Введите новое количество премиум койнов:')
    await Premium_Koin_operation.Prem_Koin_oper_save.set()





@dp.message_handler(state=Premium_Koin_operation.Prem_Koin_oper_save)
async def Koin_operation_Save(message: types.Message, state: FSMContext):
    global Prem_id_input_user

    new_Prem_Koin = message.text

    await Premium_Koin_Save_in_Operation(int(new_Prem_Koin), Prem_id_input_user)

    await message.answer('Премиум койны успешно обновлены')

    await state.finish()


# Рассылка в боте
@dp.message_handler(state=Rasoslat.rasoslat)
async def process_message(message: types.Message, state: FSMContext):
    text_to_send = message.text
    user_ids = await Rasolat()

    await message.answer('Рассылка запущена...')

    kol = 0

    for user_id in user_ids:
        try:
            await bot.send_message(chat_id=user_id[0], text=text_to_send)
            kol += 1
        except:
            ...

    await message.answer(f"Рассылка завершена. Всего отправлено сообщений: {kol}")
    await state.finish()









############################################################################
#Блок профиля пользователя


@dp.message_handler(commands=['profile'])
async def Update_Profile_User(message: types.Message):

    Koin = await Koin_dovnload(message.chat.id)
    Koin = ''.join([i for i in str(Koin) if i.isdigit()])
    Premium_Koin = await Premium_Koin_dovnload(message.chat.id)
    Premium_Koin = ''.join([i for i in str(Premium_Koin) if i.isdigit()])

    await bot.send_message(chat_id="-1002238366836",
                           text=f'Пользователь @{message.chat.username} только что зашел в профиль!')
    await Profile_User(message, Koin, Premium_Koin)



async def Profile_User(message: types.Message, Koin, Premium_Koin):
    prof_kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('💰 Магазин', callback_data='premium_user')
    btn2 = types.InlineKeyboardButton('🔥 Отзывы', callback_data='show_otzovik_btn')
    prof_kb.add(btn2, btn1)

    prem_prof_kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('🔥 Отзывы', callback_data='show_otzovik_btn')
    prem_prof_kb.add(btn1)




    PROFILE_TEXT = f'''
👤 Ваш профиль:

~~~~~~~~~~~~

🏆 Статус: <em>Обычный</em>

🎧 Количество оставшихся бесплатных песен на этот месяц: <em>{Koin}</em>
    '''

    PREMIUM_PROFILE_TEXT = f'''
👤 Ваш профиль:

~~~~~~~~~~~~

🏆 Статус: <em>Премиум ✨</em>

🎧 Количество оставшихся песен на этот месяц: <em>{Premium_Koin}</em>
        '''

    data = await Proverka1_db(message.chat.id)

    if data is None:
        data1 = await Premium_Koin_dovnload(message.chat.id)

        if data1 is None:
            await Dobav_user(message)
            await Profile_User(message, Koin, Premium_Koin)
        else:
            await message.answer(PREMIUM_PROFILE_TEXT, reply_markup=prof_kb, parse_mode='HTML')
            await bot.send_message(chat_id="-1002238366836",
                                   text=f'Пользователь @{message.from_user.username}  (tg://openmessage?user_id={message.chat.id} )нажал кнопку отзывы')
    else:
        await message.answer(PROFILE_TEXT, reply_markup=prof_kb, parse_mode='HTML')
        await bot.send_message(chat_id="-1002238366836",
                               text=f'Пользователь @{message.from_user.username}  (tg://openmessage?user_id={message.chat.id} )нажал кнопку отзывы')





async def PremiumFunc(message: types.Message):
    premium_kb = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('🔚 Назад', callback_data='premium_nazad')
    # btn2 = types.InlineKeyboardButton('💸 Купить', url='https://t.me/m/4CcTlt2wM2Zi')
    premium_kb.add(btn1)

    PREMIUM_PROF_TEXT = '''
✨ Магазин:

1) Премиум - ...   
- 600 песен в месяц, вместо 300

2) Койны:

(будут добавлены позже...)
    '''
    await message.delete()
    await message.answer(PREMIUM_PROF_TEXT, reply_markup=premium_kb)

    await bot.send_message(chat_id="-1002238366836",
                           text=f'Пользователь из профиля только перешел во кладку купить премиум!')





async def Dobav_user(message:types.Message):
    nick_user = f'@{message.from_user.username}'
    id_user = message.from_user.id
    Koin = 300

    await AddUser_db(nick_user, id_user, Koin)







############################################################################
# Блок обработки аудио




# Функция с основными кнопками
async def button():
    inline_markup = types.InlineKeyboardMarkup(row_width=3)
    inline_markup.add(types.InlineKeyboardButton('🎧 Название', callback_data='nasvanie_trek'),
                      types.InlineKeyboardButton('👥 Исполнитель', callback_data='ispolnit_trek'),
                      types.InlineKeyboardButton('🖼️ Обложка', callback_data='photo_trek'),
                      types.InlineKeyboardButton('🚪 Выход', callback_data='delete_trek'),
                      types.InlineKeyboardButton('✅ Готово', callback_data='gotovo_trek'))

    return inline_markup



@dp.message_handler(content_types=['audio'])
async def Proverka1(message: types.Message):

    user_id_db = message.chat.id

    user_channel_status = await bot.get_chat_member(chat_id='@HakerMac_IT', user_id=user_id_db)
    user_channel_status_2 = await bot.get_chat_member(chat_id='@waislime', user_id=user_id_db)

    if user_channel_status['status'] != 'left':

        if user_channel_status_2['status'] != 'left':

            data = await Proverka1_db(user_id_db)

            if data is not None:

                Koin = await Koin_dovnload(user_id_db)
                Koin = int(''.join([i for i in str(Koin) if i.isdigit()]))

                if Koin > 0:
                    Koin -= 1
                    await Koin_Save(Koin, user_id_db)
                    await download_audio(message)
                else:
                    proverka_prem_rb = types.InlineKeyboardMarkup()
                    proverka_prem_rb.add(types.InlineKeyboardButton('Премиум', callback_data='premium_user'))

                    await message.answer('У вас закончились койны!\n\nКупите премиум, чтобы изменять больше песен или подождите следующего месяца для появления бесплатных!',
                                         reply_markup=proverka_prem_rb)
                await bot.send_message(chat_id="-1002238366836",
                                       text=f'Пользователь (@{message.from_user.username}) (tg://openmessage?user_id={message.from_user.id} ) только что отправил аудио!')
            else:
                data1 = await Premium_Proverka1_db(user_id_db)


                if data1 is not None:
                    Premium_Koin = await Premium_Koin_dovnload(user_id_db)
                    Premium_Koin = int(''.join([i for i in str(Premium_Koin) if i.isdigit()]))

                    if Premium_Koin > 0:
                        Premium_Koin -= 1
                        await Premium_Koin_Save(Premium_Koin, user_id_db)
                        await download_audio(message)
                    else:
                        await message.answer('У вас закончились койны!\n\nПридется подождать следующего месяца для появления новых!')

                    await bot.send_message(chat_id="-1002238366836",
                                           text=f'Пользователь (@{message.from_user.username}) (tg://openmessage?user_id={message.from_user.id} ) только что отправил аудио!')


                else:
                    nick_user = f'@{message.from_user.username}'
                    id_user = message.from_user.id
                    Koin = 300

                    await AddUser_db(nick_user, id_user, Koin)

                    await Proverka1(message)

        else:
            podpis_Waislime = types.InlineKeyboardMarkup()
            podpis_Waislime.add(types.InlineKeyboardButton('📱 Подписаться', url='https://t.me/waislime'))

            await bot.send_message(message.from_user.id,
                                   '‼️ Чтобы пользоваться ботом, также пожалуйста подпишитесь на канал спонсора - waislime ‼️\n\nПосле подписки отправьте песню боту еще раз!',
                                   reply_markup=podpis_Waislime)

            await bot.send_message(chat_id="-1002238366836",
                                   text=f'Пользователь @{message.from_user.username} (tg://openmessage?user_id={message.from_user.id} ) только что запустил бота без подписки на Waislime!')


    else:
        if user_channel_status_2['status'] != 'left':

            podpis = types.InlineKeyboardMarkup()
            podpis.add(types.InlineKeyboardButton('📱 Подписаться', url='https://t.me/HakerMac_IT'))

            await bot.send_message(message.from_user.id, '‼️ Чтобы пользоваться ботом, пожалуйста подпишитесь на наш канал - HakerMac IT ‼️\n\nПосле подписки отправьте песню боту еще раз!',
                                   reply_markup=podpis)

            await bot.send_message(chat_id="-1002238366836",
                                   text=f'Пользователь @{message.from_user.username} (tg://openmessage?user_id={message.from_user.id} ) только что запустил бота без подписки на HakerMac!')
        else:
            podpis = types.InlineKeyboardMarkup()
            podpis.add(types.InlineKeyboardButton('📱 Подписаться', url='https://t.me/HakerMac_IT'),
                       types.InlineKeyboardButton('📱 Подписаться', url='https://t.me/waislime'))

            await bot.send_message(message.from_user.id,
                                   '‼️ Чтобы пользоваться ботом, пожалуйста подпишитесь на наш канал - HakerMac IT и канал спонсора - waislime ‼️\n\nПосле подписки отправьте песню боту еще раз. Спасибо за понимание!',
                                   reply_markup=podpis)

            await bot.send_message(chat_id="-1002238366836",
                                   text=f'Пользователь @{message.from_user.username} (tg://openmessage?user_id={message.from_user.id} ) только что запустил бота без подписки на каналы!')






async def download_audio(message: types.Message):

    await Delete_peremen(message.chat.id)
    title1 = await Show_title(message.chat.id)
    artist1 = await Show_artist(message.chat.id)

    sent_message_1 = await message.answer('📥 Приступаю к скачиванию трека, может занять незначительное время!!\n\n❗️ Если в течение минуты ничего не происходит, то обращайтесь к разрабу - @HakerMac')
    saved_message_id_1 = sent_message_1.message_id


    # Получаем файл
    file_id = message.audio.file_id
    file_info = await bot.get_file(file_id)
    await file_id_save(message.from_user.id, file_id)

    # Загружаем файл
    downloaded_file = await bot.download_file(file_info.file_path)

    with open(f"{message.audio.file_id}.mp3", 'wb') as new_file:
        new_file.write(downloaded_file.getvalue())

    await bot.send_audio(chat_id="-1002238366836", audio=file_id)

    await bot.delete_message(message.chat.id, saved_message_id_1)


    await bot.send_message(message.chat.id, f'✅ Файл успешно сохранен.')


    # Выводим сообщение об информации песни
    sent_message_2 = await bot.send_message(chat_id=message.chat.id,
                     text=f'🎧 Название: {title1}\n\n👥 Исполнитель: {artist1}\n\n~~~~~~\n\n📌 Используйте кнопки ниже, чтобы изменить тэги.\n\n⚡ Если ничего менять не нужно, то нажмите ✅Готово для получения измененной песни.\n\n❗️ Если хотите завершить сессию досрочно, то нажмите 🚪Выход',
                     reply_markup=await button())
    saved_message_id_2 = sent_message_2.message_id

    await delete_message_2_save(message.chat.id, saved_message_id_2)






# Получение нового названия песни
@dp.message_handler(state=Audio_ID.Title)
async def handle_title(message: types.Message, state: FSMContext):

    if message.text == '/cancel':
        await bot.send_message(chat_id="-1002238366836", text=f'Пользователь ({message.chat.id}) нажал отмену при переименовании песни')
        await delete_message_0_save(message.chat.id, message.message_id)

        saved_message_id_0 = await Show_delete_message_0(message.chat.id)
        saved_message_id_1 = await Show_delete_message_1(message.chat.id)
        saved_message_id_2 = await Show_delete_message_2(message.chat.id)

        await bot.delete_message(message.chat.id, saved_message_id_0)
        await bot.delete_message(message.chat.id, saved_message_id_1)
        await bot.delete_message(message.chat.id, saved_message_id_2)

        title1 = await Show_title(message.chat.id)
        artist1 = await Show_artist(message.chat.id)
        photo_status1 = await Show_photo_status(message.chat.id)
        photo_path1 = await Show_photo_path(message.chat.id)

        if photo_status1 == 1:
            sent_message_2 = await bot.send_photo(chat_id=message.chat.id,
                                                  photo=open(photo_path1, 'rb'),
                                                  caption=f'🔥 Успешно! \n\n🎧 Название: {title1}\n\n👥 Исполнитель: {artist1}\n\n~~~~~~\n\n📌 Используйте кнопки ниже, чтобы изменить тэги.\n\n⚡ Если ничего менять не нужно, то нажмите ✅Готово для получения измененной песни.\n\n❗️ Если хотите завершить сессию досрочно, то нажмите 🚪Выход',
                                                  reply_markup=await button())
            saved_message_id_2 = sent_message_2.message_id
            await delete_message_2_save(message.chat.id, saved_message_id_2)
        else:
            sent_message_2 = await bot.send_message(chat_id=message.chat.id,
                                                    text=f'🔥 Успешно! \n\n🎧 Название: {title1}\n\n👥 Исполнитель: {artist1}\n\n~~~~~~\n\n📌 Используйте кнопки ниже, чтобы изменить тэги.\n\n⚡ Если ничего менять не нужно, то нажмите ✅Готово для получения измененной песни.\n\n❗️ Если хотите завершить сессию досрочно, то нажмите 🚪Выход',
                                                    reply_markup=await button())
            saved_message_id_2 = sent_message_2.message_id
            await delete_message_2_save(message.chat.id, saved_message_id_2)

        await state.finish()

    else:
        title = message.text
        await bot.send_message(chat_id="-1002238366836",
                               text=f'Пользователь ({message.chat.id}) переименовал трек - {title}')
        await delete_message_0_save(message.chat.id, message.message_id)

        saved_message_id_0 = await Show_delete_message_0(message.chat.id)
        saved_message_id_1 = await Show_delete_message_1(message.chat.id)
        saved_message_id_2 = await Show_delete_message_2(message.chat.id)

        await bot.delete_message(message.chat.id, saved_message_id_0)
        await bot.delete_message(message.chat.id, saved_message_id_1)
        await bot.delete_message(message.chat.id, saved_message_id_2)

        await title_save(message.chat.id, title)

        title1 = await Show_title(message.chat.id)
        artist1 = await Show_artist(message.chat.id)
        photo_status1 = await Show_photo_status(message.chat.id)
        photo_path1 = await Show_photo_path(message.chat.id)



        if photo_status1 == 1:
            sent_message_2 = await bot.send_photo(chat_id=message.chat.id,
                                                  photo=open(photo_path1, 'rb'),
                                                  caption=f'🔥 Успешно! \n\n🎧 Название: {title1}\n\n👥 Исполнитель: {artist1}\n\n~~~~~~\n\n📌 Используйте кнопки ниже, чтобы изменить тэги.\n\n⚡ Если ничего менять не нужно, то нажмите ✅Готово для получения измененной песни.\n\n❗️ Если хотите завершить сессию досрочно, то нажмите 🚪Выход',
                                                  reply_markup=await button())
            saved_message_id_2 = sent_message_2.message_id
            await delete_message_2_save(message.chat.id, saved_message_id_2)
        else:
            sent_message_2 = await bot.send_message(chat_id=message.chat.id,
                                                    text=f'🔥 Успешно! \n\n🎧 Название: {title1}\n\n👥 Исполнитель: {artist1}\n\n~~~~~~\n\n📌 Используйте кнопки ниже, чтобы изменить тэги.\n\n⚡ Если ничего менять не нужно, то нажмите ✅Готово для получения измененной песни.\n\n❗️ Если хотите завершить сессию досрочно, то нажмите 🚪Выход',
                                                    reply_markup=await button())
            saved_message_id_2 = sent_message_2.message_id
            await delete_message_2_save(message.chat.id, saved_message_id_2)


        await state.finish()





# Получение нового имени исполнителя
@dp.message_handler(state=Audio_ID.Artist)
async def handle_artist(message: types.Message, state: FSMContext):

    if message.text == '/cancel':
        await bot.send_message(chat_id="-1002238366836",
                               text=f'Пользователь ({message.chat.id}) нажал отмену при изменнении исполнителя')

        await delete_message_0_save(message.chat.id, message.message_id)

        saved_message_id_0 = await Show_delete_message_0(message.chat.id)
        saved_message_id_1 = await Show_delete_message_1(message.chat.id)
        saved_message_id_2 = await Show_delete_message_2(message.chat.id)

        await bot.delete_message(message.chat.id, saved_message_id_0)
        await bot.delete_message(message.chat.id, saved_message_id_1)
        await bot.delete_message(message.chat.id, saved_message_id_2)

        title1 = await Show_title(message.chat.id)
        artist1 = await Show_artist(message.chat.id)
        photo_status1 = await Show_photo_status(message.chat.id)
        photo_path1 = await Show_photo_path(message.chat.id)

        if photo_status1 == 1:
            sent_message_2 = await bot.send_photo(chat_id=message.chat.id,
                                                  photo=open(photo_path1, 'rb'),
                                                  caption=f'🔥 Успешно! \n\n🎧 Название: {title1}\n\n👥 Исполнитель: {artist1}\n\n~~~~~~\n\n📌 Используйте кнопки ниже, чтобы изменить тэги.\n\n⚡ Если ничего менять не нужно, то нажмите ✅Готово для получения измененной песни.\n\n❗️ Если хотите завершить сессию досрочно, то нажмите 🚪Выход',
                                                  reply_markup=await button())
            saved_message_id_2 = sent_message_2.message_id
            await delete_message_2_save(message.chat.id, saved_message_id_2)
        else:
            sent_message_2 = await bot.send_message(chat_id=message.chat.id,
                                   text=f'🔥 Успешно! \n\n🎧 Название: {title1}\n\n👥 Исполнитель: {artist1}\n\n~~~~~~\n\n📌 Используйте кнопки ниже, чтобы изменить тэги.\n\n⚡ Если ничего менять не нужно, то нажмите ✅Готово для получения измененной песни.\n\n❗️ Если хотите завершить сессию досрочно, то нажмите 🚪Выход',
                                   reply_markup=await button())
            saved_message_id_2 = sent_message_2.message_id
            await delete_message_2_save(message.chat.id, saved_message_id_2)

        await state.finish()
    else:
        artist = message.text
        await bot.send_message(chat_id="-1002238366836",
                               text=f'Пользователь ({message.chat.id}) изменил имя исполнителя - {artist}')
        await delete_message_0_save(message.chat.id, message.message_id)

        saved_message_id_0 = await Show_delete_message_0(message.chat.id)
        saved_message_id_1 = await Show_delete_message_1(message.chat.id)
        saved_message_id_2 = await Show_delete_message_2(message.chat.id)

        await bot.delete_message(message.chat.id, saved_message_id_0)
        await bot.delete_message(message.chat.id, saved_message_id_1)
        await bot.delete_message(message.chat.id, saved_message_id_2)

        await artist_save(message.chat.id, artist)

        title1 = await Show_title(message.chat.id)
        artist1 = await Show_artist(message.chat.id)
        photo_status1 = await Show_photo_status(message.chat.id)
        photo_path1 = await Show_photo_path(message.chat.id)

        if photo_status1 == 1:
            sent_message_2 = await bot.send_photo(chat_id=message.chat.id,
                                                  photo=open(photo_path1, 'rb'),
                                                  caption=f'🔥 Успешно! \n\n🎧 Название: {title1}\n\n👥 Исполнитель: {artist1}\n\n~~~~~~\n\n📌 Используйте кнопки ниже, чтобы изменить тэги.\n\n⚡ Если ничего менять не нужно, то нажмите ✅Готово для получения измененной песни.\n\n❗️ Если хотите завершить сессию досрочно, то нажмите 🚪Выход',
                                                  reply_markup=await button())
            saved_message_id_2 = sent_message_2.message_id
            await delete_message_2_save(message.chat.id, saved_message_id_2)
        else:
            sent_message_2 = await bot.send_message(chat_id=message.chat.id,
                                                    text=f'🔥 Успешно! \n\n🎧 Название: {title1}\n\n👥 Исполнитель: {artist1}\n\n~~~~~~\n\n📌 Используйте кнопки ниже, чтобы изменить тэги.\n\n⚡ Если ничего менять не нужно, то нажмите ✅Готово для получения измененной песни.\n\n❗️ Если хотите завершить сессию досрочно, то нажмите 🚪Выход',
                                                    reply_markup=await button())
            saved_message_id_2 = sent_message_2.message_id
            await delete_message_2_save(message.chat.id, saved_message_id_2)

        await state.finish()


# Получение фотографии
@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message, state: FSMContext):
    photo_otprav1 = await Show_photo_otprav(message.chat.id)

    if photo_otprav1 == 1:
        await bot.send_message(chat_id="-1002238366836",
                               text=f'Пользователь ({message.chat.id}) изменил фото')
        await bot.send_photo(chat_id="-1002238366836", photo=message.photo[-1].file_id)
        photo_file_id = message.photo[-1].file_id
        await delete_message_0_save(message.chat.id, message.message_id)

        saved_message_id_0 = await Show_delete_message_0(message.chat.id)
        saved_message_id_1 = await Show_delete_message_1(message.chat.id)
        saved_message_id_2 = await Show_delete_message_2(message.chat.id)

        await photo_otprav_save(message.chat.id, 0)
        await photo_status_save(message.chat.id, 1)

        # Сохраняем file_id фото-файла
        photo_file = await bot.get_file(photo_file_id)
        photo_path = f"photo_{message.chat.id}.jpg"
        await bot.download_file(photo_file.file_path, photo_path)

        await photo_path_save(message.chat.id, photo_path)

        title1 = await Show_title(message.chat.id)
        artist1 = await Show_artist(message.chat.id)
        photo_status1 = await Show_photo_status(message.chat.id)
        photo_path1 = await Show_photo_path(message.chat.id)

        await bot.delete_message(message.chat.id, saved_message_id_0)
        await bot.delete_message(message.chat.id, saved_message_id_1)
        await bot.delete_message(message.chat.id, saved_message_id_2)

        if photo_status1 == 1:
            sent_message_2 = await bot.send_photo(chat_id=message.chat.id,
                                                  photo=open(photo_path1, 'rb'),
                                                  caption=f'🔥 Успешно! \n\n🎧 Название: {title1}\n\n👥 Исполнитель: {artist1}\n\n~~~~~~\n\n📌 Используйте кнопки ниже, чтобы изменить тэги.\n\n⚡ Если ничего менять не нужно, то нажмите ✅Готово для получения измененной песни.\n\n❗️ Если хотите завершить сессию досрочно, то нажмите 🚪Выход',
                                                  reply_markup=await button())
            saved_message_id_2 = sent_message_2.message_id
            await delete_message_2_save(message.chat.id, saved_message_id_2)
        else:
            sent_message_2 = await bot.send_message(chat_id=message.chat.id,
                                                    text=f'🔥 Успешно! \n\n🎧 Название: {title1}\n\n👥 Исполнитель: {artist1}\n\n~~~~~~\n\n📌 Используйте кнопки ниже, чтобы изменить тэги.\n\n⚡ Если ничего менять не нужно, то нажмите ✅Готово для получения измененной песни.\n\n❗️ Если хотите завершить сессию досрочно, то нажмите 🚪Выход',
                                                    reply_markup=await button())
            saved_message_id_2 = sent_message_2.message_id
            await delete_message_2_save(message.chat.id, saved_message_id_2)







# Сохранение песни и отправка пользователям
async def send_saved_audio(message: types.Message, state: FSMContext):

    saved_message_id_2 = await Show_delete_message_2(message.chat.id)
    await bot.delete_message(message.chat.id, saved_message_id_2)

    file_id = await Show_file_id(message.chat.id)
    title = await Show_title(message.chat.id)
    artist = await Show_artist(message.chat.id)
    photo_status = await Show_photo_status(message.chat.id)
    photo_path = await Show_photo_path(message.chat.id)

    if photo_status == 1:

        try:
            audiofile = eyed3.load(f"{file_id}.mp3")
            # Инициализация тега, если он отсутствует
            if audiofile.tag is None:
                audiofile.initTag()

            # Установка обложки
            # with open(photo_path, 'rb') as img_file:
            #     audiofile.tag.images.set(3, img_file.read(), 'image/jpeg')

            # Установка других тегов
            audiofile.tag.artist = artist
            audiofile.tag.title = title

            # Сохранение изменений в аудиофайле
            audiofile.tag.save()

            audio = MP3(f"{file_id}.mp3", ID3=ID3)

            # Проверяем, существуют ли теги, и добавляем их, если нет
            if not audio.tags:
                audio.add_tags()

            # Открываем изображение
            with open(f"photo_{message.chat.id}.jpg", 'rb') as img:
                # Читаем данные изображения
                img_data = img.read()

                # Проверяем, есть ли уже обложка
                if APIC in audio.tags:
                    # Обновляем существующую обложку
                    audio.tags[APIC].data = img_data
                else:
                    # Добавляем новую обложку
                    audio.tags.add(APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3,
                        desc='Cover',
                        data=img_data
                    ))

            # Сохраняем изменения
            audio.save()

            os.rename(f"{file_id}.mp3", f"{title}.mp3")

            # Отправка измененного аудиофайла пользователю
            with open(f"{title}.mp3", 'rb') as audio_file:
                await bot.send_audio(chat_id=message.chat.id, audio=audio_file, thumb=open(f"photo_{message.chat.id}.jpg", 'rb'))
            with open(f"{title}.mp3", 'rb') as audio_file:
                await bot.send_audio(chat_id="-1002238366836", audio=audio_file, thumb=open(f"photo_{message.chat.id}.jpg", 'rb'))





        except:
            audio = AudioSegment.from_file(f"{file_id}.mp3")
            audio.export(f"{file_id}.mp3", format='mp3')

            audiofile = eyed3.load(f"{file_id}.mp3")
            if audiofile.tag is None:
                audiofile.initTag()
            # audiofile.tag.images.set(3, open(photo_path, 'rb').read(), 'image/jpeg')
            audiofile.tag.artist = artist
            audiofile.tag.title = title
            audiofile.tag.save()
            audiofile.tag.frame_set = None

            audio = MP3(f"{file_id}.mp3", ID3=ID3)

            # Проверяем, существуют ли теги, и добавляем их, если нет
            if not audio.tags:
                audio.add_tags()

            # Открываем изображение
            with open(f"photo_{message.chat.id}.jpg", 'rb') as img:
                # Читаем данные изображения
                img_data = img.read()

                # Проверяем, есть ли уже обложка
                if APIC in audio.tags:
                    # Обновляем существующую обложку
                    audio.tags[APIC].data = img_data
                else:
                    # Добавляем новую обложку
                    audio.tags.add(APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3,
                        desc='Cover',
                        data=img_data
                    ))

            # Сохраняем изменения
            audio.save()

            os.rename(f"{file_id}.mp3", f"{title}.mp3")


            # Отправляем измененную песню пользователю
            with open(f"{title}.mp3", 'rb') as audio_file:
                await bot.send_audio(chat_id=message.chat.id, audio=audio_file, thumb=open(f"photo_{message.chat.id}.jpg", 'rb'))
            with open(f"{title}.mp3", 'rb') as audio_file:
                await bot.send_audio(chat_id="-1002238366836", audio=audio_file, thumb=open(f"photo_{message.chat.id}.jpg", 'rb'))


        os.remove(f"{title}.mp3")
        os.remove(f"photo_{message.chat.id}.jpg")

    else:
        try:


            audiofile = eyed3.load(f"{file_id}.mp3")
            if audiofile.tag is None:
                audiofile.initTag()
            audiofile.tag.artist = artist
            audiofile.tag.title = title
            audiofile.tag.save()
            audiofile.tag.frame_set = None

            os.rename(f"{file_id}.mp3", f"{title}.mp3")

            with open(f"{title}.mp3", "rb") as file_to_send:
                await bot.send_audio(chat_id=message.chat.id, audio=file_to_send)
            with open(f"{title}.mp3", "rb") as file_to_send:
                await bot.send_audio(chat_id="-1002238366836", audio=file_to_send)


        except:
            audio = AudioSegment.from_file(f"{file_id}.mp3")
            audio.export(f"{file_id}.mp3", format='mp3')


            audiofile = eyed3.load(f"{file_id}.mp3")
            if audiofile.tag is None:
                audiofile.initTag()
            audiofile.tag.artist = artist
            audiofile.tag.title = title
            audiofile.tag.save()
            audiofile.tag.frame_set = None

            os.rename(f"{file_id}.mp3", f"{title}.mp3")

            with open(f"{title}.mp3", "rb") as file_to_send:
                await bot.send_audio(chat_id=message.chat.id, audio=file_to_send)
            with open(f"{title}.mp3", "rb") as file_to_send:
                await bot.send_audio(chat_id="-1002238366836", audio=file_to_send)

        os.remove(f"{title}.mp3")


    await bot.send_message(chat_id="-1002238366836",
                           text=f'Пользователь ({message.chat.id})только что переименовал песню!')

    otzovik = types.InlineKeyboardMarkup()
    otzovik.add(types.InlineKeyboardButton('Написать отзыв о боте', callback_data='otzovik_btn'))

    otzov_flag = await otzovik_Proverka(message.from_user.id)

    if otzov_flag == 1:
        await message.answer('😊 Чтобы переименовать следующую песню, просто отправьте мне ее!', reply_markup=otzovik)

    else:
        await message.answer('😊 Чтобы переименовать следующую песню, просто отправьте мне ее!')





async def Delete_Treck(message: types.Message):

    file_id = await Show_file_id(message.chat.id)
    saved_message_id_2 = await Show_delete_message_2(message.chat.id)

    await bot.delete_message(message.chat.id, saved_message_id_2)
    os.remove(f"{file_id}.mp3")

    await Delete_peremen(message.chat.id)

    await message.answer('❗️ Вы вышли из сессии\n\nЧтобы изменить трек, просто отправьте мне песню.')

    await bot.send_message(chat_id="-1002238366836",
                           text=f'Пользователь только что досрочно вышел из сессии!')





##########################################################
# Блок Отзывов




@dp.message_handler(state=Otzovik_state.Otzovik_State)
async def Otzovik_func(message: types.Message, state: FSMContext):

        if message.text == '/cancel':
            await delete_message_0_save(message.chat.id, message.message_id)

            saved_message_id_0 = await Show_delete_message_0(message.chat.id)
            saved_message_id_1 = await Show_delete_message_1(message.chat.id)

            await bot.delete_message(message.chat.id, saved_message_id_0)
            await bot.delete_message(message.chat.id, saved_message_id_1)

        else:

            otzov_user = message.text
            otzov_message_id = message.message_id
            otzov_user_id = message.chat.id
            otzov_nick_user = message.from_user.username

            await delete_message_0_save(message.chat.id, otzov_message_id)

            await Public_Otzov_save(otzov_nick_user, otzov_user_id, otzov_user)

            anon_btn = types.InlineKeyboardMarkup()
            anon_btn.add(types.InlineKeyboardButton('Публично', callback_data='public_moder_user'),
                         types.InlineKeyboardButton('Анонимно', callback_data='anon_moder_user'))

            message_otzov = await bot.send_message(chat_id=message.chat.id, text='Выберите как опубликовать отзыв:\n\nПублично - в отзыве будет указана ссылка на ваш тг аккаунт'
                                                    '\n\nАнонимно - вместо ссылки будет написано просто "Пользователь"\n\n', reply_markup=anon_btn)
            message_otzov_id =message_otzov.message_id

            await delete_message_2_save(message.chat.id, message_otzov_id)

        await state.finish()





async def show_users_otzov(message: types.Message, page=0):

    otzov_flag = await otzovik_Proverka(message.chat.id)
    users = await ShowUsers_otzovik_db()

    info = ''
    Nomer_Stroki = page * 10 + 1
    start_index = page * 10
    end_index = start_index + 10
    buttons_row = []

    current_users = users[start_index:end_index]



    try:
        for el in current_users:
                info += f'{Nomer_Stroki}) Никнейм: @{el[1]}, \n  - {el[3]}\n\n'
                Nomer_Stroki += 1



        if otzov_flag == 1:
            show_users_otzov_btn = types.InlineKeyboardMarkup()
            if page > 0:
                buttons_row.append(types.InlineKeyboardButton('👈 Назад', callback_data=f'nazad_stranica_{page - 1}'))

            if end_index < len(users):
                buttons_row.append(types.InlineKeyboardButton('Далее 👉', callback_data=f'next_stranica_{page + 1}'))

            if buttons_row:
                show_users_otzov_btn.row(*buttons_row)

            show_users_otzov_btn.add(types.InlineKeyboardButton('📝 Написать отзыв', callback_data='otzovik_btn'))

            sent_message_2 = await bot.send_message(message.chat.id, text=f'⚙️ Управляйте "страницами" кнопками назад и далее (на одной "странице" выводятся только 10 отзывов)\n\nЧтобы написать отзыв жмите "Написать отзыв"\n\n📒 Отзывы:\n\n{info}', reply_markup=show_users_otzov_btn)
            saved_message_id_2 = sent_message_2.message_id
            await delete_message_2_save(message.chat.id, saved_message_id_2)


        elif otzov_flag == 0:
            show_users_otzov_btn_2 = types.InlineKeyboardMarkup()
            if page > 0:
                buttons_row.append(types.InlineKeyboardButton('👈 Назад', callback_data=f'nazad_stranica_{page - 1}'))

            if end_index < len(users):
                buttons_row.append(types.InlineKeyboardButton('Далее 👉', callback_data=f'next_stranica_{page + 1}'))

            if buttons_row:
                show_users_otzov_btn_2.row(*buttons_row)

            show_users_otzov_btn_2.add(types.InlineKeyboardButton('❌ Удалить', callback_data='delete_otzov'))

            sent_message_2 = await bot.send_message(message.chat.id,
                                                    text=f'⚙️ Управляйте "страницами" кнопками назад и далее (на одной "странице" выводятся только 10 отзывов)\n\nЧтобы удалить свой отзыв нажмите "Удалить"\n\n📒 Отзывы:\n\n{info}',
                                                    reply_markup=show_users_otzov_btn_2)

            saved_message_id_2 = sent_message_2.message_id
            await delete_message_2_save(message.chat.id, saved_message_id_2)
    except:
        show_users_otzov_btn = types.InlineKeyboardMarkup()
        show_users_otzov_btn.add(types.InlineKeyboardButton('📝 Написать отзыв', callback_data='otzovik_btn'))

        await message.answer('Отзывов пока нет!', reply_markup=show_users_otzov_btn)










@dp.callback_query_handler(lambda callback: callback.data.startswith('next_stranica_'))
async def handle_next_page(callback: types.CallbackQuery):
    saved_message_id_2 = await Show_delete_message_2(callback.message.chat.id)
    page = int(callback.data.split('_')[-1])
    await show_users_otzov(callback.message, page)
    await bot.delete_message(callback.message.chat.id, saved_message_id_2)

@dp.callback_query_handler(lambda callback: callback.data.startswith('nazad_stranica_'))
async def handle_next_page(callback: types.CallbackQuery):
    delete_message_2 = await Show_delete_message_2(callback.message.chat.id)
    await bot.delete_message(callback.message.chat.id, delete_message_2)
    page = int(callback.data.split('_')[-1])
    await show_users_otzov(callback.message, page)



@dp.callback_query_handler(lambda callback: callback.data.startswith('admin_next_stranica_'))
async def handle_next_page_admin(callback: types.CallbackQuery):
    saved_message_id_admin = await Show_delete_message_admin(callback.message.chat.id)
    page = int(callback.data.split('_')[-1])
    await show_users(callback.message, page)
    await bot.delete_message(callback.message.chat.id, saved_message_id_admin)

@dp.callback_query_handler(lambda callback: callback.data.startswith('admin_nazad_stranica_'))
async def handle_next_page_admin(callback: types.CallbackQuery):
    delete_message_admin = await Show_delete_message_admin(callback.message.chat.id)
    page = int(callback.data.split('_')[-1])
    await show_users(callback.message, page)
    await bot.delete_message(callback.message.chat.id, delete_message_admin)



# callback функции отвечающие за кнопки
@dp.callback_query_handler()
async def handle_ready_track(callback: CallbackQuery, state: FSMContext):
    global otzov_message_1

    if callback.data == 'spisok_user':
        await callback.message.answer('Список пользователей 👇')
        await show_users(callback.message)

    elif callback.data == 'spisok_prem_user':
        await callback.message.answer('Список пользователей 👇')
        await Prem_show_users(callback.message)


    elif callback.data == 'delete_user':
        await callback.message.answer('Введите ID пользователя:')
        await DeleteUsers.deleteState.set()

    elif callback.data == 'add_user':
        await callback.message.answer('Введите ID пользователя:')
        await AddUsers.addState_ID.set()

    elif callback.data == 'gotovo_trek':
        await bot.send_message(callback.message.chat.id, "🔥 Готовый файл:", reply_markup=types.ReplyKeyboardRemove())
        await send_saved_audio(callback.message, state)

    elif callback.data == 'ispolnit_trek':
        sent_message_1 = await bot.send_message(callback.message.chat.id, "👥 Введите имя исполнителя:\n\nНажмите для отмены - /cancel")
        saved_message_id_1 = sent_message_1.message_id
        await delete_message_1_save(callback.message.chat.id, saved_message_id_1)
        await Audio_ID.Artist.set()

    elif callback.data == 'nasvanie_trek':
        sent_message_1 = await bot.send_message(callback.message.chat.id, "🎧 Введите название трека:\n\nНажмите для отмены - /cancel")
        saved_message_id_1 = sent_message_1.message_id
        await delete_message_1_save(callback.message.chat.id, saved_message_id_1)
        await Audio_ID.Title.set()

    elif callback.data == 'photo_trek':
        photo_status = await Show_photo_status(callback.message.chat.id)

        photo_markup = types.InlineKeyboardMarkup(row_width=1)
        photo_markup.add(types.InlineKeyboardButton('Отмена', callback_data='otmena_photo'))

        photo_markup_Status = types.InlineKeyboardMarkup(row_width=2)
        photo_markup_Status.add(types.InlineKeyboardButton('Отмена', callback_data='otmena_photo'),
                          types.InlineKeyboardButton('Удалить текущее', callback_data='delete_photo'))

        if photo_status == 1:
            sent_message_1 = await bot.send_message(callback.message.chat.id, "🎧 Отправьте фото обложки:", reply_markup=photo_markup_Status)
            saved_message_id_1 = sent_message_1.message_id
        else:
            sent_message_1 = await bot.send_message(callback.message.chat.id, "🎧 Отправьте фото обложки:", reply_markup=photo_markup)
            saved_message_id_1 = sent_message_1.message_id
        photo_otprav = 1
        await photo_otprav_save(callback.message.chat.id, photo_otprav)
        await delete_message_1_save(callback.message.chat.id, saved_message_id_1)

    elif callback.data == 'otmena_photo':
        await Show_photo_otprav(callback.message.chat.id)
        saved_message_id_1 = await Show_delete_message_1(callback.message.chat.id)

        await bot.delete_message(callback.message.chat.id, saved_message_id_1)
        await photo_otprav_save(callback.message.chat.id, 0)

    elif callback.data == 'delete_photo':
        await Show_photo_otprav(callback.message.chat.id)
        saved_message_id_1 = await Show_delete_message_1(callback.message.chat.id)
        saved_message_id_2 = await Show_delete_message_2(callback.message.chat.id)
        await Show_photo_status(callback.message.chat.id)
        await Show_photo_path(callback.message.chat.id)
        title1 = await Show_title(callback.message.chat.id)
        artist1 = await Show_artist(callback.message.chat.id)

        await bot.delete_message(callback.message.chat.id, saved_message_id_1)
        await bot.delete_message(callback.message.chat.id, saved_message_id_2)
        await photo_otprav_save(callback.message.chat.id, 0)
        await photo_status_save(callback.message.chat.id, 0)
        await photo_path_save(callback.message.chat.id, None)
        os.remove(f"photo_{callback.message.chat.id}.jpg")

        sent_message_2 = await bot.send_message(chat_id=callback.message.chat.id,
                                                text=f'🔥 Успешно! \n\n🎧 Название: {title1}\n\n👥 Исполнитель: {artist1}\n\n~~~~~~\n\n📌 Используйте кнопки ниже, чтобы изменить тэги.\n\n⚡ Если ничего менять не нужно, то нажмите ✅Готово для получения измененной песни.\n\n❗️ Если хотите завершить сессию досрочно, то нажмите 🚪Выход',
                                                reply_markup=await button())
        saved_message_id_2 = sent_message_2.message_id
        await delete_message_2_save(callback.message.chat.id, saved_message_id_2)



    elif callback.data == 'delete_trek':
        await Delete_Treck(callback.message)

    elif callback.data == 'premium_user':
        await PremiumFunc(callback.message)

    elif callback.data == 'premium_nazad':
        await callback.message.delete()
        await Update_Profile_User(callback.message)

    elif callback.data == 'koin_operation':
        await Koin_Operations(callback.message)

    elif callback.data == 'prem_koin_operation':
        await Premium_Koin_Operations(callback.message)

    elif callback.data == 'otzovik_btn':
        otzov_flag = await otzovik_Proverka(callback.message.chat.id)

        if otzov_flag == 1:
            sent_message_1 = await bot.send_message(callback.message.chat.id, 'Напишите отзыв:\n\nНажмите для отмены - /cancel ')
            saved_message_id_1 = sent_message_1.message_id
            await delete_message_1_save(callback.message.chat.id, saved_message_id_1)
            await Otzovik_state.Otzovik_State.set()

    elif callback.data == 'show_otzovik_btn':
        await show_users_otzov(callback.message)

    elif callback.data == 'delete_otzov':
        await Delete_otzov(callback.message.chat.id)
        await callback.message.delete()
        await bot.send_message(callback.message.chat.id, "Отзыв успешно удален!")

    elif callback.data == 'moder_public':

        message_id = callback.message.message_id

        otzov = await Show_public_otzov(message_id)
        nickname = otzov[1]
        id_user = otzov[2]
        text = otzov[3]

        await otzovik_save(nickname, id_user, text, 0)

        prem_prof_kb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('🔥 Отзывы', callback_data='show_otzovik_btn')
        prem_prof_kb.add(btn1)

        await bot.send_message(chat_id=id_user, text='Ваш отзыв опубликован!', reply_markup=prem_prof_kb)
        await bot.send_message(callback.message.chat.id,'Опубликован')

        await Delete_otzov_data(id_user)


    elif callback.data == 'moder_public_anonim':

        message_id = callback.message.message_id

        otzov = await Show_public_otzov(message_id)
        nickname = 'Пользователь'
        id_user = otzov[2]
        text = otzov[3]

        await otzovik_save(nickname, id_user, text, 0)

        prem_prof_kb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('🔥 Отзывы', callback_data='show_otzovik_btn')
        prem_prof_kb.add(btn1)

        await bot.send_message(chat_id=id_user, text='Ваш отзыв опубликован!', reply_markup=prem_prof_kb)
        await bot.send_message(callback.message.chat.id,'Опубликован анонимно')

        await Delete_otzov_data(id_user)


    elif callback.data == 'moder_otklon':

        message_id = callback.message.message_id

        otzov = await Show_public_otzov(message_id)
        id_user = otzov[2]
        text = otzov[3]

        await bot.send_message(chat_id=id_user, text=f'Ваш отзыв ("{text}") отклонен!\n\nНаписать разработчику - @HakerMac')
        await bot.send_message(callback.message.chat.id,'Отклонен')

        await Delete_otzov_data(id_user)

    elif callback.data == 'Rasoslat_operation':
            await bot.send_message(callback.message.chat.id, "Пожалуйста, отправьте текст рассылки:")
            await Rasoslat.rasoslat.set()

    elif callback.data == 'public_moder_user':
        try:
            saved_message_id_0 = await Show_delete_message_0(callback.message.chat.id)
            saved_message_id_1 = await Show_delete_message_1(callback.message.chat.id)
            saved_message_id_2 = await Show_delete_message_2(callback.message.chat.id)

            await bot.delete_message(callback.message.chat.id, saved_message_id_0)
            await bot.delete_message(callback.message.chat.id, saved_message_id_1)
            await bot.delete_message(callback.message.chat.id, saved_message_id_2)
        except:
            ...

        await bot.send_message(callback.message.chat.id, 'Спасибо! Отзыв отправлен на модерацию, бот напишет о том принят или отклонен ваш отзыв!')

        otzov = await Show_public_data_otzov(callback.message.chat.id)

        nickname = otzov[1]
        id_user = otzov[2]
        text = otzov[3]

        moder_btn = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('Опуб. Публично', callback_data='moder_public')
        btn2 = types.InlineKeyboardButton('Отклонить', callback_data='moder_otklon')
        moder_btn.add(btn1, btn2)

        message_id_otzov = await bot.send_message(chat_id=2097090893,
                                                  text=f'Никнейм: @{nickname}( tg://openmessage?user_id={id_user} ), \n  - {text}\n\n',
                                                  reply_markup=moder_btn)
        message_id_otzov_1 = message_id_otzov.message_id

        await Public_Otzov_message_id(message_id_otzov_1, callback.message.chat.id)


    elif callback.data == 'anon_moder_user':
        try:
            saved_message_id_0 = await Show_delete_message_0(callback.message.chat.id)
            saved_message_id_1 = await Show_delete_message_1(callback.message.chat.id)
            saved_message_id_2 = await Show_delete_message_2(callback.message.chat.id)

            await bot.delete_message(callback.message.chat.id, saved_message_id_0)
            await bot.delete_message(callback.message.chat.id, saved_message_id_1)
            await bot.delete_message(callback.message.chat.id, saved_message_id_2)
        except:
            ...

        await bot.send_message(callback.message.chat.id,
                               'Спасибо! Отзыв отправлен на модерацию, бот напишет о том принят или отклонен ваш отзыв!')

        otzov = await Show_public_data_otzov(callback.message.chat.id)

        nickname = otzov[1]
        id_user = otzov[2]
        text = otzov[3]

        moder_btn = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('Опуб. Анонимно', callback_data='moder_public_anonim')
        btn2 = types.InlineKeyboardButton('Отклонить', callback_data='moder_otklon')
        moder_btn.add(btn1, btn2)

        message_id_otzov = await bot.send_message(chat_id=2097090893,
                                                  text=f'Никнейм: @{nickname}( tg://openmessage?user_id={id_user} ), \n  - {text}\n\n',
                                                  reply_markup=moder_btn)
        message_id_otzov_1 = message_id_otzov.message_id

        await Public_Otzov_message_id(message_id_otzov_1, callback.message.chat.id)











async def main():
    # asyncio.create_task(time_obnul_one())

    await dp.start_polling(bot)



#Без остановочная работа бота
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')