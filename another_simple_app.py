from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Another Simple Flask Application is Running!"

if __name__ == '__main__':
    app.run(debug=True)
