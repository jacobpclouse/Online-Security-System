from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
Cors = CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}},CORS_SUPPORTS_CREDENTIALS = True)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/message', methods=['POST'])
def receive_message():
    title = 'you should get this message back'
    message = request.json.get('message')
    print(message)
    #return jsonify(success=True)
    return title


if __name__ == '__main__':    
   app.run(debug=True)