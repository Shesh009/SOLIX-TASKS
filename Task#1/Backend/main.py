from flask import Flask, request, jsonify
from response import ResponseHandler
from db_handler import DBHandler

app = Flask(__name__)
@app.route('/', methods=['POST'])
def home():
    responsehandler = ResponseHandler()
    dbhandler = DBHandler()
    dbhandler.create_table()
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    query = data.get('query',"").strip()
    if not query:
        return jsonify({"message": "Query cannot be empty"}), 400
    
    try:
        result = responsehandler.handle_user_query(query)
        dbhandler.insert_data(query, result.get('answer', ''))
        return jsonify(result), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "An error occurred while processing your request."}), 500
    
if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5001, debug=True)
    except Exception as e:
        print(e)