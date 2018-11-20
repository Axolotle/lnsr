from flask import Flask, request, render_template, Response
from generators.backgroundGen import generate, generate_parallax
from generators.ruler import rulerGenerator
from generators.background import backgroundGenerator
from flask_weasyprint import HTML, render_pdf
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

@app.route('/bg')
def bg():
    return Response(response=backgroundGenerator.generate_file(), content_type='image/svg+xml')

@app.route('/pdf')
def pdf():
    pdf = HTML(string=render_template('certificate.html',
        ruler=rulerGenerator.generate_file(1346),
        bg=backgroundGenerator.generate_file(),
        **rulerGenerator.getContentNumbers(1346)))
    with open('test2.pdf', 'wb') as output:
        output.write(pdf.write_pdf())
    return render_pdf(pdf)

@app.route('/ruler')
def rulerRoot():
    return Response(response=rulerGenerator.generate_file(2), content_type='image/svg+xml')

@app.route('/lightSpeed.svg')
def lightSpeedBackground():
    return Response(response=generate_parallax(), content_type='image/svg+xml')

if __name__ == '__main__':
    app.run(debug=True)
