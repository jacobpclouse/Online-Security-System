from flask import Flask, jsonify
from flask_cors import CORS

from Flask_Functions.generalFunctions import myLogo,defang_datetime,sanitize_filename,emptyFolder,createFolderIfNotExists

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from Quasar/Vue frontend

# Sample route for sending data to the frontend
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, request, jsonify
# from flask_cors import CORS, cross_origin

# app = Flask(__name__)
# Cors = CORS(app)
# CORS(app, resources={r'/*': {'origins': '*'}},CORS_SUPPORTS_CREDENTIALS = True)
# app.config['CORS_HEADERS'] = 'Content-Type'

# @app.route('/message', methods=['POST'])
# def receive_message():
#     title = 'you should get this message back'
#     message = request.json.get('message')
#     print(message)
#     #return jsonify(success=True)
#     return title


# if __name__ == '__main__':    
#    app.run(debug=True)