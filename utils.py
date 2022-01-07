import sqlite3
import numpy as np
import base64
import cv2

def matrix2string(m):
    string = ' '.join(str(x) for x in m)
    
    string = string.encode('ascii')
    base64_bytes = base64.b64encode(string)
    encoded_auth_code = base64_bytes.decode('ascii')
    return encoded_auth_code

def string2matrix(m):
    
    base64_bytes = m.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    matrix = message_bytes.decode('ascii')

    matrix = np.array([int(x) for x in matrix.split()])
    return matrix


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

    sql = '''
    SELECT u.id 
    from user u
    where u.name=? and u.password=? and u.pubKey_e=? and u.pubKey_n=?
    '''
    id = conn.execute(sql, (user['name'], user['password'],
                       user['pub_keys']['pubKey_e'], 
                       user['pub_keys']['pubKey_n'])).fetchone()
                    
    conn.close()
    return id[0]
    


def sign_in(user_info):
    id = user_info['id']
    password = user_info['password']

    conn = sqlite3.connect('DB/database.db')
    sql ='''
    SELECT id, password FROM user WHERE id = ?
    '''
    user = conn.execute(sql, (id,)).fetchone()
    conn.close()
    if user:
        if user[1] == password:
            return True
        else:
            return False
    else:
        return False


def get_list_img(user_info):
    id = user_info['id']
    
    conn = sqlite3.connect('DB/database.db')
    sql = '''
    SELECT id, name from image where id_user=?
    '''
    list_info_img = conn.execute(sql, (id,)).fetchall()
    conn.close()
    ans = []
    for row in list_info_img:
        temp = dict()
        temp['id'] = row[0]
        temp['name'] = row[1]
        ans.append(temp)
    return ans
    

    


def upload_img(id_user, img):
    img_data = img['img_data']
    img_temp = img['img_temp']
    key_order = img['key_order']
    name = img['name']
    img_shape = img['img_shape']

    conn = sqlite3.connect('DB/database.db')
    sql='''
    SELECT * from user where id=?
    '''
    user = conn.execute(sql, (id_user, )).fetchone()
    if not user:
        return False
    
    sql = '''
    INSERT INTO image(id_user, img_data, img_temp, key_order,name, img_shape)
    VALUES(?, ?, ?, ?, ?, ?)
    '''
    conn.execute(sql, (id_user, img_data, img_temp, key_order, name, img_shape))
    conn.commit()
    return True


def download_img(info):
    id = info['id']
    id_user = info['id_user']

    conn = sqlite3.connect('DB/database.db')
    sql ='''
    SELECT * from image where id=? and id_user=?
    '''
    img = conn.execute(sql,(id, id_user)).fetchone()
    
    conn.close()
    if not img:
        return None

    img_data = img[2]
    img_temp = img[3]
    key_order = img[4]
    img_shape = img[6]

    img_shape = string2matrix(img_shape)
    img_shape = tuple(img_shape)

    img_data = string2matrix(img_data)
    img_data = img_data.reshape(img_shape)


    img_temp = string2matrix(img_temp)
    key_order = string2matrix(key_order)

    img_temp = img_temp.reshape(img_data.shape).astype(np.int32)

    key_order = np.argsort(key_order)
    img_data = img_data[key_order]


    new_img = img_temp*255 + img_data
    
    new_img = new_img.ravel()
    new_img = matrix2string(new_img)
    return new_img



if __name__ == '__main__':
    download_img({'id': 1, 'id_user': 1})