from flask import Flask, request
from background.backgroundGen import generate, generate_parallax
app = Flask(__name__)

@app.route('/a')
def normal():
    return generate()

@app.route('/b')
def parallax():
    return generate_parallax()

if __name__ == '__main__':
    app.run(debug=True)
