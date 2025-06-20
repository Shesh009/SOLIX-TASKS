from flask import Flask, request, render_template
from backend_handler import BackendHandler

app = Flask(__name__)
@app.route('/', methods=['POST','GET'])
def home():
    answer = "Ask something above"
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if query:
            backend_handler = BackendHandler()
            response = backend_handler.send_query(query)
            if response:
                answer = response.get("answer", "No answer found.")
            else:
                answer = "Backend error or no response."
    return render_template('index.html', answer=answer)

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000, debug=True)
    except Exception as e:  
        print(f"Error starting the Flask app: {e}")