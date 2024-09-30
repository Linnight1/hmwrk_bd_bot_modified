import sqlite3

def initiate_db(id, title, description, price):
    connection = sqlite3.connect("../Lib/Bot/database.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INT NOT NULL
    );
    ''')
    add_product = cursor.execute("SELECT * FROM Products WHERE id = ?", (id,))
    if add_product.fetchone() is None:
        cursor.execute(f'''
    INSERT INTO Products VALUES ("{id}", "{title}", "{description}", "{price}")
''')
    connection.commit()
    connection.close()

def add_user(username, email, age):
    connection = sqlite3.connect("../Lib/Bot/database.db")
    cursor = connection.cursor()

    cursor.execute(f'''
    INSERT INTO Users VALUES("{username}", "{email}", "{age}", "{1000}")
''')
    connection.commit()
    connection.close()
def is_included(username):
    connection = sqlite3.connect("../Lib/Bot/database.db")
    cursor = connection.cursor()
    cursor.execute('''
              CREATE TABLE IF NOT EXISTS Users(
              id INT PRIMARY KEY,
              username TEXT NOT NULL,
              email TEXT NOT NULL,
              balance INT NOT NULL)
              ''')
    user = cursor.execute("SELECT username FROM Users WHERE username=?", (username,))
    if user.fetchone() is None:
        return True
    else:
        return False

def get_all_products(product):
    connection = sqlite3.connect("../Lib/Bot/database.db")
    cursor = connection.cursor()
    product_list = cursor.execute("SELECT title, description, price FROM Products WHERE id=?", (product,))
    get_product = ""
    for product in product_list:
        get_product += f"Название: {product[0]} | Описание: {product[1]} | Цена:{product[2]}"
    connection.commit()
    return get_product



initiate_db(1,"Бальзам-ополаскиватель 'Лошадиная сила'", "Счастье для волос", "100 рублей" )
initiate_db(2,"Маска для волос 'Лошадиная сила'", "Счастье для ваших волос", "150 рублей")
initiate_db(3,"Гель 'Лошадиная сила'", "Гель с конским каштаном и экстрактом пиявки","200 руб")
initiate_db(4,"Детский шампунь 'Лошадиная сила'", "Лошадиная сила для ваших детей", "250 руб")
# connection = sqlite3.connect("../Lib/Bot/database.db")
# cursor = connection.cursor()
#
# cursor.execute("DELETE FROM Products WHERE id < ?", (10, ))
# connection.commit()
# connection.close()
