import mysql.connector

# Тест підключення до бази даних
def test_database_connection():
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="bot_database"
        )
        
        if conn.is_connected():
            print("Тест підключення до бази даних: Підключення до бази даних вдале")
    except mysql.connector.Error as error:
        print("Помилка підключення до бази даних:", error)
    finally:
        if conn:
            conn.close()

# Тест додавання запису
def test_insert_record():
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="bot_database"
        )
        
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO `users-currencies` (userid, currency_name, quantity) VALUES (%s, %s, %s)",
            (12345, 'USD', 100)
        )
        
        conn.commit()
        
        if cursor.rowcount > 0:
            print("Тест додавання запису: Запис успішно додано")
        
        cursor.close()
    except mysql.connector.Error as error:
        print("Помилка додавання запису:", error)
    finally:
        if conn:
            conn.close()

# Тест оновлення запису
def test_update_record():
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="bot_database"
        )
        
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE `users-currencies` SET quantity = %s WHERE userid = %s AND currency_name = %s",
            (200, 12345, "USD")
        )
        
        conn.commit()
        
        if cursor.rowcount > 0:
            print("Тест оновлення запису: Запис успішно оновлено")
        
        cursor.close()
    except mysql.connector.Error as error:
        print("Помилка оновлення запису:", error)
    finally:
        if conn:
            conn.close()

# Тест видалення запису
def test_delete_record():
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="bot_database"
        )
        
        cursor = conn.cursor()
        
        cursor.execute(
            "DELETE FROM `users-currencies` WHERE userid = %s AND currency_name = %s",
            (12345, "USD")
        )
        
        conn.commit()
        
        if cursor.rowcount > 0:
            print("Тест видалення запису: Запис успішно видалено")
        
        cursor.close()
    except mysql.connector.Error as error:
        print("Помилка видалення запису:", error)
    finally:
        if conn:
            conn.close()

# Тест отримання даних
def test_fetch_data():
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="bot_database"
        )
        
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT currency_name, quantity FROM `users-currencies` WHERE userid = %s", 
            (12345,)
        )
        
        rows = cursor.fetchall()
        
        for row in rows:
            print(row)
        
        cursor.close()
    except mysql.connector.Error as error:
        print("Помилка отримання даних:", error)
    finally:
        if conn:
            conn.close()

# Тест валідації даних
def test_data_validation():
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="bot_database"
        )
        
        cursor = conn.cursor()
        
        try:
            cursor.execute(
            "INSERT INTO `users-currencies` (userid, currency_name, quantity) VALUES (%s, %s, %s)",
            (12345, 'USD', 'invalid')
            )
            conn.commit()
            print("Тест валідації даних: Дані успішно вставлено (некоректні дані)")
        except mysql.connector.Error as error:
            print("Помилка вставлення некоректних даних:", error)
        
        cursor.close()
    except mysql.connector.Error as error:
        print("Помилка валідації даних:", error)
    finally:
        if conn:
            conn.close()

# Виклик функцій для тестування
test_database_connection()
test_insert_record()
test_update_record()
test_delete_record()
test_fetch_data()
test_data_validation()
