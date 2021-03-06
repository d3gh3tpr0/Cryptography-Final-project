from flask import Flask, jsonify, request
import utils
import RSA
import base64
import matplotlib.image as photo

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_page():
    data = {'nameSchool':'Khoa hoc tu nhien',  
            'subject': 'Ma hoa mat ma', 
            'students': [
                {'name':'Phan Trung Hieu', 'id': '19127404'}, 
                {'name':'Le Tien Hung', 'id': '19127412'}, 
                {'name': 'Tran Huu Trong', 'id': '19127601'}
                
            ],
            'name_group': '010412'}
    return jsonify({"data":data, "statusCode": 401, 
                    "status":"success"})

@app.route('/sign-up', methods=['POST'])
def sign_up():

    user = request.form
    user = {'name': user['name'],
            'password': user['password'],
            'pub_keys': {
                'pubKey_e' : user['pubKey_e'],
                'pubKey_n' : user['pubKey_n']
            }
    }
    check_user = utils.check_user(user)
    if (check_user):
        auth_code = 'ma hoa mat ma 19MMT final project 2021'
        pub_keys = str(user['pub_keys']['pubKey_e']) + ' ' + \
                   str(user['pub_keys']['pubKey_n'])

        temp_str = RSA.encrypt(auth_code, pub_keys)


        temp_str = temp_str.encode('ascii')
        base64_bytes = base64.b64encode(temp_str)
        encoded_auth_code = base64_bytes.decode('ascii')
        
        

        return jsonify({"status":"success", "statusCode": 200,
                        'verified_code': encoded_auth_code})
    else :
        return jsonify({"status": "failed", "statusCode": 401})

@app.route('/sign-up-auth', methods=['POST'])
def sign_up_auth():
    user = request.form
    #print(user)
    temp_str = user['decoded_auth_code']
    user = {'name': user['name'],
            'password': user['password'],
            'pub_keys': {
                'pubKey_e' : user['pubKey_e'],
                'pubKey_n' : user['pubKey_n']
            }
    }
    
    if (temp_str == 'ma hoa mat ma 19MMT final project 2021'):
        id = utils.insert_user(user)
        return jsonify({"status":"success", "statusCode": 200,
                        'message': 'Sign-up process is completed successfully',
                        "id": id})
    else:
        return jsonify({"status":"failed", "statusCode": 401,
                        'message': 'Errors in sign-up process'})

@app.route('/sign-in', methods=['GET'])
def sign_in():
    user_info = request.args
    check_login = utils.sign_in(user_info)
    if check_login:
        list_info_img = utils.get_list_img(user_info)
        return jsonify({"status": "success", "statusCode": 200,
                        "message": "Log-in successfully",
                        "list_info_img": list_info_img})
    else:
        return jsonify({"status": "failed", "statusCode": 401,
                        "message": "Log-in failed"})

@app.route('/upload-img', methods=['POST'])
def upload_img():
    id_user = request.args.get('id')
    img = request.form
    
    check_upload_img = utils.upload_img(id_user, img)
    
    if check_upload_img:
        return jsonify({"status": "success", "statusCode": 200, 
                        "message": "Upload image successfully"})
    else:
        return jsonify({"status": "failed", "statusCode": 401,
                        "message": "Upload image failed"})

@app.route('/download-img', methods=['GET'])  
def download_img():
    info = request.args
    img = utils.download_img(info)

    if img:
        return jsonify({"status": "success", "statusCode":200,
                        "message": "Download image successfully",
                        "image": img})
    else:
        return jsonify({"status": "failed", "statusCode":401,
                        "message": "Download image failed"})

if __name__ == '__main__':
    app.run()

