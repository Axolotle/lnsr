from flask import Flask, request, render_template, Response, send_file, after_this_request
from generators.backgroundGen import generate, generate_parallax
from generators.ruler import ruler
from generators.background import background
app = Flask(__name__)
from flask_weasyprint import HTML, render_pdf
from zipfile import ZipFile, ZIP_DEFLATED
import os

lnsr = 101

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/fileGen/')
def fileGeneration():
    global lnsr
    lnsr = lnsr + 1
    filename = '{f}light-nanosecond_ruler{n}{e}.{ext}'
    pdf = HTML(string=render_template('certificate.html',
                                      ruler=ruler.generateString(lnsr, 'pdf'),
                                      bg=background.generateString(),
                                      **ruler.getContentNumbers(lnsr)))

    with ZipFile(filename.format(f='output/', n=lnsr, e='', ext='zip'), 'w', ZIP_DEFLATED) as zip_file:
        zip_file.writestr(filename.format(f='', n=lnsr, e='-laser', ext='svg'),
                          ruler.generateString(lnsr, 'laser'))
        zip_file.writestr(filename.format(f='', n=lnsr, e='-certificate', ext='pdf'),
                          pdf.write_pdf())

    @after_this_request
    def remove_file(response):
        try:
            os.remove('output/test2.zip')
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response

    return send_file(filename.format(f='output/', n=lnsr, e='', ext='zip'),
        as_attachment=True)

@app.route('/bg')
def bg():
    return Response(response=background.generateString(), content_type='image/svg+xml')

@app.route('/pdf')
def pdf():
    pdf = HTML(string=render_template('certificate.html',
        ruler=ruler.generateString(lnsr),
        bg=background.generateString(),
        **ruler.getContentNumbers(lnsr)))
    with open('test2.pdf', 'wb') as output:
        output.write(pdf.write_pdf())


    return render_pdf(pdf)

@app.route('/ruler')
def rulerRoot():
    return Response(response=ruler.generateString(2), content_type='image/svg+xml')

@app.route('/lightSpeed.svg')
def lightSpeedBackground():
    return Response(response=generate_parallax(), content_type='image/svg+xml')

if __name__ == '__main__':
    app.run(debug=True)
