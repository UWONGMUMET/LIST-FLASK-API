from flask import Flask
from routes.PokeRoutes import pokemon_bp

app = Flask(__name__)
app.register_blueprint(pokemon_bp)

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(port=5000, debug=True)