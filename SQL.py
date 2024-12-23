import sqlite3

















async def language_db():
    conn = sqlite3.connect('DataBaseLanguage.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS language_users (id int auto_increment primary key, id_user int, language varchar)')
    conn.commit()

    cur.close()
    conn.close()





#Создание премиум базы данных
async def handle_premium_database():
    global conn, cur

    conn = sqlite3.connect('DataBasePremiumUsers.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS premium_users (id int auto_increment primary key, nickname varchar(50), id_user int, premium_koin int)')
    conn.commit()

    cur.close()
    conn.close()




#Создание базы данных
async def handle_database():
    global conn, cur

    conn = sqlite3.connect('DataBaseUsers.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, nickname varchar(50), id_user int, koin int)')
    conn.commit()

    cur.close()
    conn.close()


# Проверка на премиум пользователя
async def Premium_Proverka1_db(user_id_db):
    conn = sqlite3.connect('DataBasePremiumUsers.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM premium_users WHERE id_user = ?", (user_id_db,))
    data = cur.fetchone()

    cur.close()
    conn.close()

    return data

# Проверка на существование пользователя
async def Proverka1_db(user_id_db):
    conn = sqlite3.connect('DataBaseUsers.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM users WHERE id_user = ?", (user_id_db,))
    data = cur.fetchone()

    cur.close()
    conn.close()

    return data

# Проверка при добавлении премиум пользователя
async def Proverka_AddUser_db(id_user):
    conn = sqlite3.connect('DataBasePremiumUsers.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT id_user FROM premium_users WHERE id_user = {id_user}")
    data = cur.fetchone()

    cur.close()
    conn.close()

    return data

# Добавление премиум пользователя
async def Premium_AddUser_db(nick_user, id_user, Premium_Koin):
    conn = sqlite3.connect('DataBasePremiumUsers.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO premium_users (nickname, id_user,premium_koin) VALUES ('%s', '%s', '%s')" % (nick_user, id_user, Premium_Koin))
    conn.commit()

    cur.close()
    conn.close()

# Добавление пользователя
async def AddUser_db(nick_user, id_user, Koin):
    conn = sqlite3.connect('DataBaseUsers.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (nickname, id_user, koin) VALUES ('%s', '%s', '%s')" % (nick_user, id_user, Koin))
    conn.commit()

    cur.close()
    conn.close()

# Удаление премиум пользователя
async def Premium_DeleteUser_db(id_user1):
    conn = sqlite3.connect('DataBasePremiumUsers.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT id_user FROM premium_users WHERE id_user = {id_user1}")
    data = cur.fetchone()

    if data is not None:
        cur.execute(f"DELETE FROM premium_users WHERE id_user = {id_user1}")

    conn.commit()

    cur.close()
    conn.close()

    return data

# Удаление пользователя
async def DeleteUser_db(id_user1):
    conn = sqlite3.connect('DataBaseUsers.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT id_user FROM users WHERE id_user = {id_user1}")
    data = cur.fetchone()

    if data is not None:
        cur.execute(f"DELETE FROM users WHERE id_user = {id_user1}")

    conn.commit()

    cur.close()
    conn.close()

    return data


# Показать всех премиум пользователей
async def Premium_ShowUsers_db():
    conn = sqlite3.connect('DataBasePremiumUsers.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM premium_users')
    users = cur.fetchall()

    cur.close()
    conn.close()

    return users

# Показать всех премиум пользователей
async def ShowUsers_db():
    conn = sqlite3.connect('DataBaseUsers.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    cur.close()
    conn.close()

    return users



async def Koin_dovnload(id_user1):
    conn = sqlite3.connect('DataBaseUsers.sql')
    cur = conn.cursor()

    cur.execute(f'SELECT koin FROM users WHERE id_user = {id_user1}')
    koin = cur.fetchone()

    cur.close()
    conn.close()

    if koin != None:
        return koin[0]
    else:
        return None


async def Koin_Save(koin, is_user):
    conn = sqlite3.connect('DataBaseUsers.sql')
    cur = conn.cursor()

    cur.execute(f'UPDATE users SET koin = {koin} WHERE id_user = {is_user}')
    conn.commit()

    cur.close()
    conn.close()

async def Koin_Save_in_operation(koin, id_user):
    conn = sqlite3.connect('DataBaseUsers.sql')
    cur = conn.cursor()

    cur.execute(f'UPDATE users SET koin = {koin} WHERE id_user = {id_user}')
    conn.commit()

    cur.close()
    conn.close()


async def Premium_Koin_dovnload(id_user1):
    conn = sqlite3.connect('DataBasePremiumUsers.sql')
    cur = conn.cursor()


    cur.execute(f'SELECT premium_koin FROM premium_users WHERE id_user = {id_user1}')
    premium_koin = cur.fetchone()

    cur.close()
    conn.close()


    if premium_koin != None:
        return premium_koin[0]
    else:
        return None


async def Premium_Koin_Save(premium_koin, id_user):
    conn = sqlite3.connect('DataBasePremiumUsers.sql')
    cur = conn.cursor()

    cur.execute(f'UPDATE premium_users SET premium_koin = {premium_koin} WHERE id_user = {id_user}')
    conn.commit()

    cur.close()
    conn.close()


async def Premium_Koin_Save_in_Operation(premium_koin, id_user):
    conn = sqlite3.connect('DataBasePremiumUsers.sql')
    cur = conn.cursor()

    cur.execute(f'UPDATE premium_users SET premium_koin = {premium_koin} WHERE id_user = {id_user}')
    conn.commit()

    cur.close()
    conn.close()


async def Perehod_user(id_user1):
    conn = sqlite3.connect('DataBasePremiumUsers.sql')
    cur = conn.cursor()

    cur.execute(f'SELECT nickname FROM premium_users WHERE id_user = {id_user1}')
    nickname = (cur.fetchone())[0]

    cur.close()
    conn.close()

    return nickname


async def premium_time_one_day():
    conn = sqlite3.connect('DataBasePremiumUsers.sql')
    cur = conn.cursor()

    cur.execute('UPDATE premium_users SET premium_koin = 600')
    conn.commit()

    cur.close()
    conn.close()

async def time_one_day():
    conn = sqlite3.connect('DataBaseUsers.sql')
    cur = conn.cursor()

    cur.execute('UPDATE users SET koin = 300')
    conn.commit()

    cur.close()
    conn.close()



# Проверка на существование отзыва и скачивание флага
async def otzovik_Proverka(id_user):
    conn = sqlite3.connect('DataBaseUsers_Otzovik.sql')
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS otzovik_users(id int auto_increment primary key, nickname varchar(50), id_user int, otzov varchar, otzov_flag int)')
    conn.commit()


    cur.execute(f"SELECT id_user FROM otzovik_users WHERE id_user = {id_user}")
    data_user = cur.fetchone()

    if data_user is not None:
        cur.execute(f"SELECT otzov_flag FROM otzovik_users WHERE id_user = {id_user}")
        otzov_flag = (cur.fetchone())[0]

    elif data_user is None:
        otzov_flag = 1


    cur.close()
    conn.close()

    return otzov_flag




# Сохранение отзыва
async def otzovik_save(nick_user, id_user, otzov, otzov_flag):
    conn = sqlite3.connect('DataBaseUsers_Otzovik.sql')
    cur = conn.cursor()


    cur.execute(f"SELECT id_user FROM otzovik_users WHERE id_user = {id_user}")
    data_user = cur.fetchone()

    if data_user is None:
        cur.execute(
            "INSERT INTO otzovik_users (nickname, id_user, otzov, otzov_flag) VALUES ('%s', '%s', '%s', '%s')" % (nick_user, id_user, otzov, otzov_flag))
        conn.commit()

    else:
        cur.execute(f'UPDATE otzovik_users SET otzov = {otzov} WHERE id_user = {id_user}')
        conn.commit()


        cur.execute(f'UPDATE otzovik_users SET otzov_flag = {otzov_flag} WHERE id_user = {id_user}')
        conn.commit()


    cur.close()
    conn.close()



async def ShowUsers_otzovik_db():
    conn = sqlite3.connect('DataBaseUsers_Otzovik.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM otzovik_users')
    users = cur.fetchall()

    cur.close()
    conn.close()

    return users






async def Delete_otzov(id_user):
    conn = sqlite3.connect('DataBaseUsers_Otzovik.sql')
    cur = conn.cursor()

    cur.execute(f'DELETE FROM otzovik_users WHERE id_user = {id_user}')
    conn.commit()


    cur.close()
    conn.close()


##############################################
# Блок переменных


async def Delete_peremen(id_user):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f'DELETE FROM peremen_users WHERE id_user = {id_user}')
    conn.commit()


    cur.close()
    conn.close()


async def peremen():
    global conn, cur

    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS peremen_users(id int auto_increment primary key, id_user int, title varchar, artist varchar, album varchar, photo_status int, photo_path varchar, file_id varchar, delete_message_0 int, delete_message_1 int, delete_message_2 int, photo_otprav int, delete_message_admin int)')
    conn.commit()

    cur.close()
    conn.close()


async def title_save(id_user, title):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT id_user FROM peremen_users WHERE id_user = {id_user}")
    data_user = cur.fetchone()

    if data_user is None:
        cur.execute(
            "INSERT INTO peremen_users (id_user, title) VALUES ('%s', '%s')" % (id_user,title))
        conn.commit()

    else:
        cur.execute('UPDATE peremen_users SET title = ? WHERE id_user = ?', (title, id_user))
        conn.commit()

    cur.close()
    conn.close()


async def Show_title(id_user):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT title FROM peremen_users WHERE id_user = {id_user}")
    title = cur.fetchone()

    cur.close()
    conn.close()

    if title != None:
        return title[0]
    else:
        return None





async def artist_save(id_user, artist):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT id_user FROM peremen_users WHERE id_user = {id_user}")
    data_user = cur.fetchone()

    if data_user is None:
        cur.execute(
            "INSERT INTO peremen_users (id_user, artist) VALUES ('%s', '%s')" % (id_user, artist))
        conn.commit()

    else:
        cur.execute('UPDATE peremen_users SET artist = ? WHERE id_user = ?', (artist, id_user))
        conn.commit()

    cur.close()
    conn.close()


async def Show_artist(id_user):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT artist FROM peremen_users WHERE id_user = {id_user}")
    artist = cur.fetchone()

    cur.close()
    conn.close()

    if artist != None:
        return artist[0]
    else:
        return None







async def album_save(id_user, album):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT id_user FROM peremen_users WHERE id_user = {id_user}")
    data_user = cur.fetchone()

    if data_user is None:
        cur.execute(
            "INSERT INTO peremen_users (id_user, album) VALUES ('%s', '%s')" % (id_user,album))
        conn.commit()

    else:
        cur.execute('UPDATE peremen_users SET album = ? WHERE id_user = ?', (album, id_user))
        conn.commit()

    cur.close()
    conn.close()


async def Show_album(id_user):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT album FROM peremen_users WHERE id_user = {id_user}")
    album = cur.fetchone()

    cur.close()
    conn.close()

    if album != None:
        return album[0]
    else:
        return None







async def photo_status_save(id_user, photo_status):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT id_user FROM peremen_users WHERE id_user = {id_user}")
    data_user = cur.fetchone()

    if data_user is None:
        cur.execute(
            "INSERT INTO peremen_users (id_user, photo_status) VALUES ('%s', '%s')" % (id_user,photo_status))
        conn.commit()

    else:
        cur.execute(f'UPDATE peremen_users SET photo_status = {photo_status} WHERE id_user = {id_user}')
        conn.commit()

    cur.close()
    conn.close()


async def Show_photo_status(id_user):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT photo_status FROM peremen_users WHERE id_user = {id_user}")
    photo_status = cur.fetchone()

    cur.close()
    conn.close()

    if photo_status != None:
        return photo_status[0]
    else:
        return None



async def language_save(id_user, language):
    conn = sqlite3.connect('DataBaseLanguage.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT id_user FROM language_users WHERE id_user = {id_user}")
    data_user = cur.fetchone()

    if data_user is None:
        cur.execute(
            "INSERT INTO language_users (id_user, language) VALUES ('%s', '%s')" % (id_user,language))
        conn.commit()

    else:
        cur.execute('UPDATE language_users SET language = ? WHERE id_user = ?', (language, id_user))
        conn.commit()

    cur.close()
    conn.close()


async def Show_language(id_user):
    conn = sqlite3.connect('DataBaseLanguage.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT id_user FROM language_users WHERE id_user = {id_user}")
    data_user = cur.fetchone()

    if data_user is None:
        cur.execute(
            "INSERT INTO language_users (id_user, language) VALUES ('%s', '%s')" % (id_user, 'ru'))
        conn.commit()

        cur.execute(f"SELECT language FROM language_users WHERE id_user = {id_user}")
        language = cur.fetchone()

    else:
        cur.execute(f"SELECT language FROM language_users WHERE id_user = {id_user}")
        language = cur.fetchone()

    cur.close()
    conn.close()

    if language != None:
        return language[0]
    else:
        return None






async def file_id_save(id_user, file_id):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    # Используем параметризованные запросы для предотвращения SQL-инъекций
    cur.execute("SELECT id_user FROM peremen_users WHERE id_user = ?", (id_user,))
    data_user = cur.fetchone()

    if data_user is None:
        cur.execute(
            "INSERT INTO peremen_users (id_user, file_id) VALUES (?, ?)", (id_user, file_id))
    else:
        cur.execute("UPDATE peremen_users SET file_id = ? WHERE id_user = ?", (file_id, id_user))

    conn.commit()
    cur.close()
    conn.close()



async def Show_file_id(id_user):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    # Используем параметризованный запрос
    cur.execute("SELECT file_id FROM peremen_users WHERE id_user = ?", (id_user,))
    file_id = (cur.fetchone())[0]


    cur.close()
    conn.close()

    return file_id




async def photo_path_save(id_user, photo_path):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    # Используем параметризованные запросы для предотвращения SQL-инъекций
    cur.execute("SELECT id_user FROM peremen_users WHERE id_user = ?", (id_user,))
    data_user = cur.fetchone()

    if data_user is None:
        cur.execute(
            "INSERT INTO peremen_users (id_user, photo_path) VALUES (?, ?)", (id_user, photo_path))
    else:
        cur.execute("UPDATE peremen_users SET photo_path = ? WHERE id_user = ?", (photo_path, id_user))

    conn.commit()
    cur.close()
    conn.close()




async def Show_photo_path(id_user):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    # Используем параметризованный запрос
    cur.execute("SELECT photo_path FROM peremen_users WHERE id_user = ?", (id_user,))
    photo_path = cur.fetchone()

    cur.close()
    conn.close()

    if photo_path != None:
        return photo_path[0]
    else:
        return None


async def delete_message_0_save(id_user, delete_message_0):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT id_user FROM peremen_users WHERE id_user = {id_user}")
    data_user = cur.fetchone()

    if data_user is None:
        cur.execute(
            "INSERT INTO peremen_users (id_user, delete_message_0) VALUES ('%s', '%s')" % (id_user,delete_message_0))
        conn.commit()

    else:
        cur.execute(f'UPDATE peremen_users SET delete_message_0 = {delete_message_0} WHERE id_user = {id_user}')
        conn.commit()

    cur.close()
    conn.close()


async def Show_delete_message_0(id_user):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT delete_message_0 FROM peremen_users WHERE id_user = {id_user}")
    delete_message_0 = cur.fetchone()

    cur.close()
    conn.close()

    if delete_message_0 != None:
        return delete_message_0[0]
    else:
        return None



async def delete_message_1_save(id_user, delete_message_1):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT id_user FROM peremen_users WHERE id_user = {id_user}")
    data_user = cur.fetchone()

    if data_user is None:
        cur.execute(
            "INSERT INTO peremen_users (id_user, delete_message_1) VALUES ('%s', '%s')" % (id_user,delete_message_1))
        conn.commit()

    else:
        cur.execute(f'UPDATE peremen_users SET delete_message_1 = {delete_message_1} WHERE id_user = {id_user}')
        conn.commit()

    cur.close()
    conn.close()


async def Show_delete_message_1(id_user):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT delete_message_1 FROM peremen_users WHERE id_user = {id_user}")
    delete_message_1 = cur.fetchone()

    cur.close()
    conn.close()

    if delete_message_1 != None:
        return delete_message_1[0]
    else:
        return None



async def delete_message_2_save(id_user, delete_message_2):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT id_user FROM peremen_users WHERE id_user = {id_user}")
    data_user = cur.fetchone()

    if data_user is None:
        cur.execute(
            "INSERT INTO peremen_users (id_user, delete_message_2) VALUES ('%s', '%s')" % (id_user,delete_message_2))
        conn.commit()

    else:
        cur.execute(f'UPDATE peremen_users SET delete_message_2 = {delete_message_2} WHERE id_user = {id_user}')
        conn.commit()

    cur.close()
    conn.close()


async def Show_delete_message_2(id_user):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT delete_message_2 FROM peremen_users WHERE id_user = {id_user}")
    delete_message_2 = cur.fetchone()

    cur.close()
    conn.close()

    if delete_message_2 != None:
        return delete_message_2[0]
    else:
        return None




async def delete_message_admin_save(id_user, delete_message_admin):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT id_user FROM peremen_users WHERE id_user = {id_user}")
    data_user = cur.fetchone()

    if data_user is None:
        cur.execute(
            "INSERT INTO peremen_users (id_user, delete_message_admin) VALUES ('%s', '%s')" % (id_user,delete_message_admin))
        conn.commit()

    else:
        cur.execute(f'UPDATE peremen_users SET delete_message_admin = {delete_message_admin} WHERE id_user = {id_user}')
        conn.commit()

    cur.close()
    conn.close()


async def Show_delete_message_admin(id_user):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT delete_message_admin FROM peremen_users WHERE id_user = {id_user}")
    delete_message_admin = cur.fetchone()

    cur.close()
    conn.close()

    if delete_message_admin != None:
        return delete_message_admin[0]
    else:
        return None




async def photo_otprav_save(id_user, photo_otprav):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT id_user FROM peremen_users WHERE id_user = {id_user}")
    data_user = cur.fetchone()

    if data_user is None:
        cur.execute(
            "INSERT INTO peremen_users (id_user, photo_otprav) VALUES ('%s', '%s')" % (id_user,photo_otprav))
        conn.commit()

    else:
        cur.execute(f'UPDATE peremen_users SET photo_otprav = {photo_otprav} WHERE id_user = {id_user}')
        conn.commit()

    cur.close()
    conn.close()


async def Show_photo_otprav(id_user):
    conn = sqlite3.connect('DataBaseUsers_Peremen.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT photo_otprav FROM peremen_users WHERE id_user = {id_user}")
    photo_otprav = cur.fetchone()

    cur.close()
    conn.close()

    if photo_otprav != None:
        return photo_otprav[0]
    else:
        return None



async def Rasolat():
    conn = sqlite3.connect('DataBaseUsers.sql')
    cur = conn.cursor()

    cur.execute(f'SELECT id_user FROM users')
    id = cur.fetchall()


    cur.close()
    conn.close()

    return id





async def Public_otzov():
    global conn, cur

    conn = sqlite3.connect('DataBasePublic_Otzov.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS public_otzov (id int auto_increment primary key, nickname varchar(50), id_user int, '
                'otzov varchar, id_message int)')
    conn.commit()

    cur.close()
    conn.close()



async def Public_Otzov_save(nickname, id_user, text):
    conn = sqlite3.connect('DataBasePublic_Otzov.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO public_otzov (nickname, id_user, otzov) VALUES (?, ?, ?)", (nickname, id_user, text))

    conn.commit()
    cur.close()
    conn.close()


async def Public_Otzov_message_id(message_id, user_id):
    conn = sqlite3.connect('DataBasePublic_Otzov.sql')
    cur = conn.cursor()

    cur.execute("UPDATE public_otzov SET id_message = ? WHERE id_user = ?", (message_id, user_id))


    conn.commit()
    cur.close()
    conn.close()



async def Show_public_otzov(id_message):
    conn = sqlite3.connect('DataBasePublic_Otzov.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM public_otzov WHERE id_message = {id_message}")
    otzov = cur.fetchone()

    cur.close()
    conn.close()

    return otzov


async def Show_public_data_otzov(id_user):
    conn = sqlite3.connect('DataBasePublic_Otzov.sql')
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM public_otzov WHERE id_user = {id_user}")
    otzov = cur.fetchone()

    cur.close()
    conn.close()

    return otzov


async def Delete_otzov_data(id_user):
    conn = sqlite3.connect('DataBasePublic_Otzov.sql')
    cur = conn.cursor()

    cur.execute(f'DELETE FROM public_otzov WHERE id_user = {id_user}')
    conn.commit()


    cur.close()
    conn.close()


