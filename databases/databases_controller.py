import sqlite3

def connecting():
    global connect, cursor
    connect = sqlite3.connect("samirai_food.db")
    cursor = connect.cursor()
    if connect:
        print("samurai_food.db connected OK")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS menu(
        img TEXT,
        name TEXT PRIMARY KEY,
        descrip TEXT,
        value TEXT
        )""")
    connect.commit()
    

async def menu_add(data):
    print(data)
    cursor.execute("INSERT INTO menu VALUES (?, ?, ?, ?)", tuple(data.values()))
    connect.commit()
    print("values added to database OK")
    
    
async def load_menu_for_admin():
    data = cursor.execute("SELECT * FROM menu").fetchall()
    print(data)
    return data


async def del_from_menu(name):
    print("connected for db to del item from menu OK")
    cursor.execute("DELETE FROM menu WHERE name = ?", (name,))
    connect.commit()
    print("item was deleted OK")
    
    
async def load_menu():
    return cursor.execute("SELECT * FROM menu").fetchall()