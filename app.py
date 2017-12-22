from flask import Flask, request
from background.backgroundGen import generate
app = Flask(__name__)

@app.route('/')
def index():
    return generate()

if __name__ == '__main__':
    app.run(debug=True)
