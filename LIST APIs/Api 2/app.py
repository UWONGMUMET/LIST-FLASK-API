from flask import Flask
from routes.DbRoutes import notes_bp

app = Flask(__name__)
app.register_blueprint(notes_bp)

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(port=5000, debug=True)