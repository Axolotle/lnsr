from flask import Flask, request
from generators.backgroundGen import generate, generate_parallax
from generators.lnsrGen import ruler

app = Flask(__name__)

@app.route('/a')
def normal():
    return generate()

@app.route('/b')
def parallax():
    return generate_parallax()

@app.route('/ruler')
def rulerRoot():
    return ruler.draw(125)

if __name__ == '__main__':
    app.run(debug=True)
