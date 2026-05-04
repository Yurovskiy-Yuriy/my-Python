import psycopg2

# Функция, удаляющая таблицы.
def del_db(conn):    
    with conn.cursor() as cur:
        # удаление таблиц
        cur.execute("""--sql
        DROP TABLE phone;
        DROP TABLE client;
        """)
    conn.commit()

# Функция, создающая структуру БД (таблицы).
def create_db(conn):
    with conn.cursor() as cur:
        # создаем клиента
        cur.execute("""--sql
        CREATE TABLE IF NOT EXISTS client(
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            email TEXT UNIQUE  -- ублали NOT NULL, теперь это поле не обязателно       
        );
        """)

    # создаем БД телефонов ("один-ко-многим" (1:N))
        cur.execute("""--sql
        CREATE TABLE IF NOT EXISTS phone(
            id SERIAL PRIMARY KEY,
            phone_number TEXT NOT NULL,
            client_id INTEGER NOT NULL REFERENCES client(id) ON DELETE CASCADE
        );
        """)
    conn.commit()  # фиксируем в БД

# Функция, позволяющая добавить нового клиента.
def add_client(conn, name, surname, email=None):    
    with conn.cursor() as cur:
        if email is None:
            cur.execute("""--sql
            INSERT INTO client (name, surname) 
            VALUES (%s, %s)
            """, (name, surname))
        else:
            cur.execute("""--sql
            INSERT INTO client (name, surname, email) 
            VALUES (%s, %s, %s)
            """, (name, surname, email))
    conn.commit()
#P.s. В Python + PostgreSQL для подстановки значений используются %s (независимо от типа данных)
#Значения передаются отдельным кортежем/словарем вторым аргументом

# Функция для удаления ограничения NOT NULL с колонки email
def drop_not_null_constraint(conn):
    with conn.cursor() as cur:
        cur.execute("""--sql
        ALTER TABLE client 
        ALTER COLUMN email 
        DROP NOT NULL;
        """)
        conn.commit()

# Функция, позволяющая добавить телефон для существующего клиента.
def add_phone(conn, client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute("""--sql
        INSERT INTO phone (phone_number, client_id) 
        VALUES (%s, %s)
        RETURNING id, phone_number, client_id;
        """, (phone_number, client_id))
        
        id, phone, client = cur.fetchone()  # распаковываем кортеж
        print(f"Добавлен телефон {phone} с ID {id} для клиента {client}")

# Функция, позволяющая изменить данные о клиенте.
def change_client(conn, client_id, name=None, surname=None, email=None):
        updates = []
        params = []
        
        if name is not None:
            updates.append("name = %s")
            params.append(name)
        
        if surname is not None:
            updates.append("surname = %s")
            params.append(surname)
        
        if email is not None:
            updates.append("email = %s")
            params.append(email)

        params.append(client_id)

        with conn.cursor() as cur:
            query = f"""--sql
            UPDATE client 
            SET {', '.join(updates)} 
            WHERE id = %s
            RETURNING id, name, surname, email;
            """
            
            cur.execute(query, params)

            result = cur.fetchone()
            conn.commit()
    
        print(f"Клиент ID {client_id} успешно обновлен:")
        print(f"  Имя: {result[1]}")
        print(f"  Фамилия: {result[2]}")
        print(f"  Email: {result[3]}")

# Функция, позволяющая удалить телефон для существующего клиента.
def delete_phone_by_id(conn, phone_id):
    with conn.cursor() as cur:
        cur.execute("""--sql
        DELETE FROM phone 
        WHERE id = %s
        RETURNING id, phone_number, client_id;
        """, (phone_id,))
        
        deleted = cur.fetchone()
        conn.commit()
        
        print(f"Телефон {deleted[1]} (ID: {deleted[0]}) удален у клиента ID {deleted[2]}")
        

# Функция, позволяющая удалить существующего клиента.
def delete_client(conn, client_id):
    with conn.cursor() as cur:
        
        cur.execute("""--sql
        DELETE FROM client 
        WHERE id = %s
        RETURNING id, name, surname, email;
        """, (client_id,))
        
        deleted = cur.fetchone()
        conn.commit()
        
        print(f"Клиент ID {deleted[0]} успешно удален:")
        print(f"Имя: {deleted[1]} {deleted[2]}")
        print(f"Email: {deleted[3]}")

# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
 
def find_client(name = None, surname = None, email = None, number = None):
    with conn.cursor() as cur:
        cur.execute("""--sql
                   SELECT c.*, t.number
                     FROM clients c 
                     FUll OUTER JOIN telephones t ON c.id = t.client
                    WHERE (name = %(name)s or %(name)s is NULL) 
                          and (surname = %(surname)s or %(surname)s is NULL)
                          and (email = %(email)s or %(email)s is NULL)
                          and (number = %(number)s or %(number)s is NULL);
                   """, {'name':name, 'surname':surname, 'email':email, 'number':number})
        print(f'Найденная запись клиента:', cur.fetchall())

if __name__ == '__main__':
    with psycopg2.connect(database="client_db", user="postgres", password="308") as conn:
        del_db(conn)

        create_db(conn)

        add_client(conn, 'Мария', 'Иванова', 'maria@email.com')
        add_client(conn, 'Петр', 'Петров', 'Petr@email.com')
        
        drop_not_null_constraint(conn)
        add_client(conn, 'Иван', 'Иванов')

        add_phone(conn, 1, +7777777777)
        add_phone(conn, 1, +7777778888)
        add_phone(conn, 1, +777777999)
        add_phone(conn, 2, +777555555)
        add_phone(conn, 3, +775454544)

        change_client(conn, 1, name = 'Маргарита')
        change_client(conn, 2, name = 'Сидоров')

        delete_phone_by_id(conn, 5)

        delete_client(conn, 3)
        find_client(None,'Иванов', None, None)

    conn.close()