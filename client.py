import requests
import numpy as np
import cv2
import RSA
import base64



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

#test sign-up
'''
url = "http://127.0.0.1:5000/sign-up"

p, q, e, d, N = RSA.generateKeys(keysize=8)

data = {'name' :'Nam Anh', 
        'password':'hcmus2k1',
        'pubKey_e' : e,
        'pubKey_n' : N
    }


r = requests.post(url, data=data)
print(r.json())
verified_code = dict(r.json())['verified_code']
 
base64_bytes = verified_code.encode('ascii')
message_bytes = base64.b64decode(base64_bytes)
encypted_code = message_bytes.decode('ascii')


private_keys = '{} {} {}'.format(p, q , d)
decoded_auth_code = RSA.decrypt(encypted_code, private_keys, N)
print(decoded_auth_code)
data = {'name' :'Nam Anh', 
        'password':'cryptography',
        'pubKey_e' : e,
        'pubKey_n' : N,
        'decoded_auth_code' : decoded_auth_code
    }
url = "http://127.0.0.1:5000/sign-up-auth"

r = requests.post(url, data=data)
print(r.json())


'''


#test upload-img
'''
url = "http://127.0.0.1:5000/upload-img"

img = cv2.imread('thanhduy.jpg')
img = img.astype('int')
img_shape = img.shape

p, q, e, d, N = RSA.generateKeys(keysize=8)

pub_keys = str(e)+ " " + str(N)
pri_keys = str(p)+ " " + str(q) + " " + str(d)

def encrypt(x):
    copy = int(x)
    rsa = RSA.RSA(8, pub_keys)
    return rsa.encrypt_pixel(copy)

func1 = np.vectorize(encrypt)
encrypted_img = func1(img)
img_temp, img_data = divmod(encrypted_img, 255)
print('img_temp', img_temp)
lock_order = np.random.permutation(len(img_data))
print('lock_order', lock_order)


img_data = img_data[lock_order]
print('img_data', img_data)

img_temp = img_temp.ravel()
img_temp = matrix2string(img_temp)
lock_order = matrix2string(lock_order)


img_data = img_data.ravel()
img_data = matrix2string(img_data)

img_shape = list(img_shape)
img_shape = matrix2string(img_shape)



data = {'img_data':img_data,
        'img_temp':img_temp,
        'key_order':lock_order,
        'name': 'first_image.jpg', 
        'img_shape': img_shape}

r = requests.post(url, data=data, params={'id': 1})
print(r.json())
pri_keys = "{} {} {}".format(p, q, d)

print(pri_keys)
print(N)
'''







