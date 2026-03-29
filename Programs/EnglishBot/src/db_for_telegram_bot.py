import psycopg2
import os

from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

load_dotenv() # Загружаем переменные из .env

db_password = os.getenv("db_PASSWORD")
if not db_password:
    raise ValueError("Не найден db_password в .env")    

# Функция, создающая базу данных
def create_database(db_name, user, password):
    # Подключаемся к стандартной базе данных postgres
    conn = psycopg2.connect(database="postgres", user=user, password=password)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    with conn.cursor() as cur:
        # Проверяем, существует ли база данных
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cur.fetchone()
        
        if not exists:
            cur.execute(f'CREATE DATABASE {db_name}')
            print(f"База данных '{db_name}' создана")
        else:
            print(f"База данных '{db_name}' уже существует")
    
    conn.close()

# Функция, создающая таблицы.
def create_db(conn):
    with conn.cursor() as cur:
        # создаем пользователя
        cur.execute("""--sql
        CREATE TABLE IF NOT EXISTS users(
            telegram_user_id BIGINT PRIMARY KEY
        );
        """)
	
	  # создаем общий словарь
        cur.execute("""--sql
        CREATE TABLE IF NOT EXISTS global_word(
            id SERIAL PRIMARY KEY,
            word VARCHAR(255) NOT NULL,
            translation VARCHAR(255) NOT NULL
        );
        """)

	# создаем индивидуальный словарь 
        cur.execute("""--sql
        CREATE TABLE IF NOT EXISTS individual_word(
            id SERIAL PRIMARY KEY,
            word VARCHAR(255) NOT NULL,
            translation VARCHAR(255) NOT NULL,	
            telegram_user_id BIGINT NOT NULL REFERENCES users(telegram_user_id) ON DELETE CASCADE
        );
        """)
    conn.commit()  

# Функция, добавляем слова в словарь
def add_global_word (conn, word, translation):    
    with conn.cursor() as cur:
        cur.execute("""--sql
        INSERT INTO global_word (word, translation) 
        VALUES (%s, %s)
        """, (word, translation))
    conn.commit()


# Функция, позволяющая добавить индивидуальное слово для пользователя
def add_individual_word(conn, telegram_user_id, word, translation):
    with conn.cursor() as cur:
        cur.execute("""--sql
        INSERT INTO individual_word (word, translation, telegram_user_id) 
        VALUES (%s, %s, %s)
        RETURNING word;
        """, (word, translation, telegram_user_id))
        
        word  = cur.fetchone()[0]
        print(f"Новое слово {word} добавлено")
        conn.commit()



if __name__ == '__main__':
    db_name = "for_telegram_bot_db"
    user = "postgres"
    password = db_password
    
    # Создаем базу данных, если её нет
    create_database(db_name, user, password)

    # Подключаемся к созданной базе данных
    with psycopg2.connect(database="for_telegram_bot_db", user="postgres", password=db_password) as conn:
        # Создаем таблицы
        create_db(conn)
  
        # Добавляем слова в общий словарь
        eng_word = ['apple', 'book', 'cat', 'dog', 'house', 'car', 'tree', 'sun', 'moon', 'star', 'water', 'fire']
        rus_word = ['яблоко', 'книга', 'кошка', 'собака', 'дом', 'машина', 'дерево', 'солнце', 'луна', 'звезда', 'вода', 'огонь']
        for x, y in zip(eng_word, rus_word):
        	add_global_word(conn, x, y)

       
