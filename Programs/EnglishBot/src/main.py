import os
from dotenv import load_dotenv
import random
import psycopg2

from telebot import types, TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup


state_storage = StateMemoryStorage()   # хранилище состояний пользователей
load_dotenv() # Загружаем переменные окружения из .env

token_bot = os.getenv("TELEGRAM_TOKEN")
if not token_bot:
    raise ValueError("Не найден TELEGRAM_TOKEN в .env") 
 
db_password = os.getenv("db_PASSWORD")
if not db_password:
    raise ValueError("Не найден db_password в .env")     
            
bot = TeleBot(token_bot, state_storage=state_storage)   # создание экземпляра класса TeleBot

known_users = [] # список известных пользователей
userStep = {}   # шаги пользователей
buttons = []   # массив кнопок для вывода на экран

#функция принимает произвольное количество строк и объединяет их в одну строку, разделяя символом переноса строки (\n).
def show_hint(*lines): # создает строку-подсказку из массива строк
    return '\n'.join(lines)  

#функция возвращает строку с переводом английского слова на русский, используя словарь data
def show_target(data): # выводит целевой перевод
    return f"{data['target_word']} -> {data['translate_word']}"

#определяем команды, используемые в интерфейсе бота для взаимодействия с пользователями  (хранит названия команд, которые будут использованы для кнопок)
class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово🔙'
    NEXT = 'Дальше ⏭'

#определяем три возможных состояния пользователя: выбор целевого слова, ввод перевода и работа с дополнительными словами.
class MyStates(StatesGroup):
    target_word = State()           # Выбор целевого слова
    translate_word = State()        # Ввод перевода
    another_words = State()         # Дополнительные слова (не используется здесь)
    add_new_word = State()          # Новое состояние для ввода нового слова
    input_translation = State()     # Новое состояние для ввода перевода
    remove_word = State()           # Новый состояние для удаления слова

#функция проверяет, известно ли нам ID пользователя. Если нет — добавляет его в список и устанавливает начальное состояние.
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        known_users.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0

#Отвечает за отображение карточек со словом и кнопками выбора переводов. Используется также для инициализации нового пользователя.
@bot.message_handler(commands=['cards', 'start'])
def create_cards(message):
    cid = message.chat.id

 # Добавляем пользователя в базу данных при первом запуске, если в таблице users его нет
    try:
        with psycopg2.connect(database="for_telegram_bot_db", user="postgres", password=db_password) as conn:
            with conn.cursor() as cur:
                cur.execute("""--sql
                    INSERT INTO users (telegram_user_id) 
                    VALUES (%s) 
                    ON CONFLICT (telegram_user_id) DO NOTHING
                """, (cid,))
                conn.commit()
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")

    if cid not in known_users:
        known_users.append(cid)
        userStep[cid] = 0
        bot.send_message(cid, """   Привет 👋 Давай попрактикуемся в английском языке. 

    У тебя есть возможность использовать тренажёр, как конструктор, и собирать свою собственную базу для обучения. Для этого воспрользуйся инструментами:
    - добавить слово ➕,
    - удалить слово 🔙.

Ну что, начнём ⬇️""")
        
    # Формируем клавиатуру с вариантами переводов
    markup = types.ReplyKeyboardMarkup(row_width=2)
    global buttons
    buttons = []
    
    
    "---------------------------------------Получаем слова из БД----------------------------------------------"
    
    with psycopg2.connect(database="for_telegram_bot_db", user="postgres", password=db_password) as conn:
        
        # Получаем случайное слово из общего словаря
        with conn.cursor() as cur:
            cur.execute("""--sql
                SELECT word, translation FROM global_word ORDER BY RANDOM() LIMIT 1;
            """)
            global_result = cur.fetchone()
            # correct_result = cur.fetchone()
            # target_word, translate = correct_result

        # Проверяем наличие слов в личном словаре пользователя
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) FROM individual_word WHERE telegram_user_id=%s;
            """, (message.from_user.id,))
            count_personal_words = cur.fetchone()[0]
        
        # Если есть слова в личном словаре, берем случайное личное слово
        if count_personal_words > 0:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT word, translation FROM individual_word WHERE telegram_user_id=%s ORDER BY RANDOM() LIMIT 1;
                """, (message.from_user.id,))
                personal_result = cur.fetchone()
            
            # Объединяем оба результата вместе
            results = [global_result, personal_result]
            
            # Случайно выбираем один из результатов
            selected_result = random.choice(results)
            
        else:
            # Если личный словарь пуст, берём только из общего словаря
            selected_result = global_result
        
        target_word, translate = selected_result

        #Получаем не правильные вырианты 
        with conn.cursor() as cur:
            cur.execute("""
                SELECT word FROM global_word WHERE word != %s ORDER BY RANDOM() LIMIT 3;
            """, (target_word,))
            incorrect_results = cur.fetchall()
            others = [row[0] for row in incorrect_results]
           
    # Правильный вариант
    target_word_btn = types.KeyboardButton(target_word)
    buttons.append(target_word_btn)

    # Неправильные варианты
    other_words_btns = [types.KeyboardButton(word) for word in others]
    buttons.extend(other_words_btns)
    

    "----------------------------------Формируем и отображаем кнопки-------------------------------------- "
    
    random.shuffle(buttons)  # Перемешиваем порядок кнопок
       
    # Добавляем дополнительные кнопки (далее, добавить слово, удалить слово)
    next_btn = types.KeyboardButton(Command.NEXT)
    add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    buttons.extend([next_btn, add_word_btn, delete_word_btn])

    # Добавляем созданные кнопки в разметку
    markup.add(*buttons)

    # Отправляем приветствие и показываем первые кнопки
    greeting = f"Выбери перевод слова:\n🇷🇺 {translate}"
    bot.send_message(message.chat.id, greeting, reply_markup=markup)
    
    # Сохраняем состояние пользователя
    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['target_word'] = target_word
        data['translate_word'] = translate
        data['other_words'] = others

#Обработка нажатия кнопки "Далее", снова вызывается метод create_cards, который заново генерирует новую карточку
@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def next_cards(message):
    create_cards(message)


"---------------------------------Удаление нового слова из таблицу------------------------------------"

#Используется для удаления текущего слова из базы данных.
@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def start_remove_word(message):
    bot.send_message(message.chat.id, "Введите слово, которое хотите удалить.")
    bot.set_state(message.from_user.id, MyStates.remove_word, message.chat.id)

# Обработчик удаления слова
@bot.message_handler(state=MyStates.remove_word)
def process_delete_word(message):
    word_to_delete = message.text.strip().lower()
    
    with psycopg2.connect(database="for_telegram_bot_db", user="postgres", password=db_password) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM individual_word 
                WHERE word=%s AND telegram_user_id=%s;
            """, (word_to_delete, message.from_user.id))
            deleted_count = cur.rowcount
            conn.commit()
    
    if deleted_count > 0:
        bot.send_message(message.chat.id, f"Слово '{word_to_delete}' успешно удалено!")
    else:
        bot.send_message(message.chat.id, f"Слово '{word_to_delete}' не найдено в вашей коллекции.")
    
    bot.delete_state(message.from_user.id, message.chat.id)  #очистка текущего состояния пользователя 

    create_cards(message)  # возращаем карточки с кнопками


"-------------------------------Добавление нового слова в таблицу---------------------------------"

# Функция добавляет слово в индивидуальный словарь пользователя
def add_individual_word(conn, telegram_user_id, word, translation):

    with conn.cursor() as cur:
        cur.execute("""--sql
        INSERT INTO individual_word (word, translation, telegram_user_id) 
        VALUES (%s, %s, %s)
        RETURNING word;
        """, (word, translation, telegram_user_id))
        
        word = cur.fetchone()[0]
        print(f"Новое слово {word} добавлено")
        conn.commit()

#Обработка добавления слова, временно переключается в режим ожидания ввода нового слова 
@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
def add_word(message):
    bot.send_message(message.chat.id, "Введите английское слово:")
    bot.set_state(message.from_user.id, MyStates.add_new_word, message.chat.id)
    
# Прием введенного слова
@bot.message_handler(state=MyStates.add_new_word)
def receive_word(message):
    word = message.text.strip().lower()
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["new_word"] = word
    bot.send_message(message.chat.id, f"Введите перевод слова '{word}' на русский:")
    bot.set_state(message.from_user.id, MyStates.input_translation, message.chat.id)

# Прием перевода и сохранение в базу данных
@bot.message_handler(state=MyStates.input_translation)
def receive_translation(message):
    translation = message.text.strip().lower()
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        new_word = data["new_word"]
    
    # Подключение к базе данных и добавление нового слова
    with psycopg2.connect(database="for_telegram_bot_db", user="postgres", password=db_password) as conn:
        add_individual_word(conn, message.from_user.id, new_word, translation)
        conn.commit()
    
    bot.send_message(message.chat.id, f"Слово '{new_word}' успешно добавлено!")
    bot.delete_state(message.from_user.id, message.chat.id)      #очистка текущего состояния пользователя 

    create_cards(message)  # возращаем карточки с кнопками


"-----------------------Основная логика обработки текста от пользователя----------------------------"

#Проверяет правильность выбранного варианта перевода и формирует подсказки либо сообщение об ошибке.
@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_reply(message):
    text = message.text
    markup = types.ReplyKeyboardMarkup(row_width=2)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_word = data['target_word']
        if text == target_word:
            hint = show_target(data)
            hint_text = ["Отлично!❤", hint]
           
            hint = show_hint(*hint_text)

            # Отправляем сообщение БЕЗ изменения клавиатуры
            bot.send_message(message.chat.id, hint)

            return  # выходим из хендлера, чтобы ниже ничего не выполнялось

        else: 
            # Если выбран неверный перевод,
            for btn in buttons:
                if btn.text == text:
                    btn.text = text + '❌'
                    break
            hint = show_hint("Допущена ошибка!",
                             f"Попробуй ещё раз вспомнить слово 🇷🇺{data['translate_word']}")
            
    # Обновляем разметку кнопок и отправляем новое сообщение
    markup.add(*buttons)
    bot.send_message(message.chat.id, hint, reply_markup=markup)


"--------------------------------------Запуск бота------------------------------------------------"
#добавляем фильтрацию по состоянию и начинаем основной цикл прослушивания сообщений
bot.add_custom_filter(custom_filters.StateFilter(bot))

# Начинаем постоянный опрос серверов Telegram для приёма новых сообщений 
bot.infinity_polling(skip_pending=True)  
