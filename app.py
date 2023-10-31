from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
import requests
import secrets
from db import db
import base64
app = Flask(__name__)
CORS(app)

# Replace 'mysql://username:password@localhost/dbname' with your MySQL configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://aavani:aavani123@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']="181161201564774075125354654742806578788"


db = SQLAlchemy(app)

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)



class RequestData(db.Model):
    ___tablename__="request_data"
    
    id=db.Column(db.Integer,primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    verb_type = db.Column(db.String(10), nullable=False)
    json_data = db.Column(db.String(255))
    basic_auth_key = db.Column(db.String(255))




# Function to set Basic Auth Key
def set_basic_auth_key(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return user.id
    else:
        return None


# def set_basic_auth_key(username, password):
#     # Print the SQL query to debug
#     print(f"SELECT id FROM users WHERE username = {username} AND password = {password}")

#     cur = mysql.connection.cursor()
#     cur.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
#     user_id = cur.fetchone()
#     cur.close()

#     print(f"User ID from the database: {user_id}")

#     return user_id




# Route for authentication
# @app.route('/authentication', methods=['POST'])
# def authentication():
#     username = request.args.get('username')
#     password = request.args.get('password')

#     user_id = set_basic_auth_key(username, password)

#     if user_id:
#         return jsonify({"base64EncodedAuthenticationKey": f"User{user_id}EncodedKey"})
#     else:
#         return jsonify({"message": "Invalid credentials"}, 401)


# @app.route('/authentication', methods=['POST'])
# def authentication():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     print(f"Received credentials: username={username}, password={password}")

#     user_id = set_basic_auth_key(username, password)

#     print(f"User ID after authentication: {user_id}")

#     if user_id:
#         return jsonify({"base64EncodedAuthenticationKey": f"User{user_id}EncodedKey"})
#     else:
#         return jsonify({"message": "Invalid credentials"}, 401)

@app.route('/authentication', methods=['POST'])
def authentication():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        # Perform authentication logic (replace this with your actual authentication logic)
        # For simplicity, just encode the username and password in base64
        auth_key = base64.b64encode(f"{username}:{password}".encode()).decode()

        return jsonify({'base64EncodedAuthenticationKey': auth_key}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @app.route('/executeAjaxRequest', methods=['POST'])
# def execute_ajax_request():
#     try:
#         data = request.get_json()
#         url = data.get('url')
#         verb_type = data.get('verbType')
#         json_data = data.get('jsonData')
#         basic_auth_key = data.get('basicAuthKey')
        

#         headers = {"Authorization": "Basic " + basic_auth_key}

#         if basic_auth_key is not None:
#             headers = {"Authorization": "Basic " + basic_auth_key}
#         else:
#             headers = {}  # Provide a default value for headers if basic_auth_key is None

#         response = requests.request(verb_type, url, data=json_data, headers=headers)
        

#         if verb_type == 'POST':
#             response = requests.post(url, json=json_data)
#         elif verb_type == 'GET':
#             response = requests.get(url)
#         elif verb_type == 'PUT':
#             response = requests.put(url, json=json_data)
#         elif verb_type == 'DELETE':
#             response = requests.delete(url)

#         if response is not None:
#             response.raise_for_status()
#             return jsonify({"response": response.json()})
#         else:
#             return jsonify({"error": "Request failed with no response"}), 500
        
#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": str(e)}), 500


#         return jsonify({"error": str(e)}), 500
import json

@app.route('/execute-request', methods=['POST'])
def execute_api_request():
    data = request.get_json()
    if 'verb_type' not in data:
        return jsonify({'error': 'Missing "verbType" in JSON data'}), 400

    verb_type = data['verb_type']
    print(verb_type)
    url = data['url']
    json_data = json.dumps(data.get('json_data', {}))
    
    # Extract the Basic Auth Key from the request (You should implement authentication logic here)
    basic_auth_key = data['basic_auth_key']

    # Make the HTTP request to the external API using the 'requests' library
    headers = {'Authorization': 'Basic ' + basic_auth_key}
    response = requests.request(verb_type, url, json=json_data, headers=headers)

    # Store the response data in the database
    api_response = RequestData(url=url, verb_type=verb_type,json_data=json_data,basic_auth_key=basic_auth_key)
    db.session.add(api_response)
    db.session.commit()

    return jsonify({'message': 'Request completed successfully'})


if __name__=="__main__":
    app.debug(True)