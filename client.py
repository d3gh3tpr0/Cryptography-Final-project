import requests
import numpy as np
import matplotlib.pyplot as plt
import RSA
import base64

url = "http://127.0.0.1:5000/sign-up"

p, q, e, d, N = RSA.generateKeys(keysize=8)

data = {'name' :'Tien Hung', 
        'password':'yeuemhieu',
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
data = {'name' :'Tien Hung', 
        'password':'yeuemHieu',
        'pubKey_e' : e,
        'pubKey_n' : N,
        'decoded_auth_code' : decoded_auth_code
    }
url = "http://127.0.0.1:5000/sign-up-auth"

r = requests.post(url, data=data)
print(r.json())