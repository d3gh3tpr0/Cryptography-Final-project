import sqlite3

def check_user(user):
    if (user['name'] == '' or user['password'] == ''  or user['pub_keys']['pubKey_e'] == '' or user['pub_keys']['pubKey_n'] == '') :
        return False
    else:
        return True


def insert_user(user):
    conn = sqlite3.connect('DB/database.db')
    
    sql = '''
    INSERT INTO user(name, password, pubKey_e, pubKey_n) 
    VALUES (?, ?, ?, ?)
    '''
    conn.execute(sql, (user['name'], user['password'],
                       user['pub_keys']['pubKey_e'], 
                       user['pub_keys']['pubKey_n']))
    conn.commit()
    conn.close()






def get_all(query):
    conn = sqlite3.connect('db/db.db')
    data = conn.execute(query).fetchall()

    conn.close()
    return data

def get_news_by_id(news_id):
    conn = sqlite3.connect('db/db.db')
    sql = '''
    SELECT N.subject, N.description, N.image, N.original_url, C.name, C.url,
    FROM news N INNER JOIN category C ON N.category_id = C.id 
    WHERE id = ?
    '''
    news = conn.execute(sql, (news_id,)).fetchone()
    conn.close()
    return news

def get_category_by_id(category_id):
    conn = sqlite3.connect('db/db.db')
    sql = '''
    SELECT * FROM category C WHERE C.id = ?
    '''
    category = conn.execute(sql, (category_id,)).fetchone()
    conn.close()
    return category

def add_comment(category_id, content):
    conn = sqlite3.connect('db/db.db')
    sql = '''
    INSERT INTO comment(content, catagory_id) VALUES (?, ?)
    '''
    conn.execute(sql, (content, category_id))
    conn.commit()
    conn.close()




if __name__ == '__main__':
    conn = sqlite3.connect('DB/database.db')
    a = conn.execute('Select * from user').fetchall()
    print(a)