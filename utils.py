import sqlite3

def check_user(user):
    if (user['name'] == '' or user['password'] == ''  or user['pub_keys']['pubKey_e'] == '' or user['pub_keys']['pubKey_n'] == '') :
        return False
    else:
        return True


def insert_user(user):
    conn = sqlite3.connect('DB/database.db')
    
    # sql = '''
    # INSERT INTO user(name, password, pubKey_e, pubKey_n) 
    # VALUES (?, ?, ?, ?)
    # '''
    # conn.execute(sql, (user['name'], user['password'],
    #                    user['pub_keys']['pubKey_e'], 
    #                    user['pub_keys']['pubKey_n']))
    # conn.commit()
    sql = '''
    SELECT u.id 
    from user u
    where u.name=? and u.password=? and u.pubKey_e=? and u.pubKey_n=?
    '''
    id = conn.execute(sql, (user['name'], user['password'],
                       user['pub_keys']['pubKey_e'], 
                       user['pub_keys']['pubKey_n'])).fetchone()
                    
    conn.close()
    return id
    


def sign_in(id, password):
    conn = sqlite3.connect('DB/database.db')
    sql ='''
    SELECT * FROM user WHERE id = ?
    '''
    user = conn.execute(sql, (id,)).fetchone()
    pass

def insert_img(image):
    buffer = image['buffer']
    id_user = image['id_user']
    img_name = image['name']
    img_own = image['own']
    pass





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
    user = {'name': 'Trung Hieu',
            'password': 'yeuemhung',
            'pub_keys': {
                'pubKey_e' : 235,
                'pubKey_n' : 37001
            }
    }
    print(insert_user(user)[0])
