from flask import Flask, request, render_template, Response
from generators.backgroundGen import generate, generate_parallax
from generators.ruler import rulerGenerator

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/a')
def normal():
    return generate()

@app.route('/b')
def parallax():
    return generate_parallax()

@app.route('/ruler')
def rulerRoot():
    return Response(response=rulerGenerator.generate_file(2), content_type='image/svg+xml')

@app.route('/lightSpeed.svg')
def lightSpeedBackground():
    return Response(response=generate_parallax(), content_type='image/svg+xml')

if __name__ == '__main__':
    app.run(debug=True)
