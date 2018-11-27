from flask import Flask, request, render_template, Response, send_file, after_this_request, session, jsonify
from generators.backgroundGen import generate, generate_parallax
from generators.ruler import ruler
from generators.background import background
from flask_weasyprint import HTML, render_pdf
from zipfile import ZipFile, ZIP_DEFLATED
import os

app = Flask(__name__)
app.secret_key = 'lel'

lnsr = 100

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/rulerRequest', methods=['POST'])
def rulerRequest():
    if not 'number' in session:
        global lnsr
        lnsr = lnsr + 1
        session['number'] = lnsr
    return jsonify({
        'number': session['number'],
        **ruler.getContentNumbers(session['number'])
    })


@app.route('/download')
def fileGeneration():
    if not 'number' in session:
        return '404'
    else:
        number = session['number']
        session.clear()

    filename = '{}light-nanosecond_ruler{}{}.{}'
    pdf = HTML(string=render_template('certificate.html',
                                      ruler=ruler.generateString(number, 'pdf'),
                                      bg=background.generateString(),
                                      **ruler.getContentNumbers(number)))

    with ZipFile(filename.format('output/', number, '', 'zip'), 'w', ZIP_DEFLATED) as zip_file:
        zip_file.writestr(filename.format('', number, '-laser', 'svg'),
                          ruler.generateString(number, 'laser'))
        zip_file.writestr(filename.format('', number, '-certificate', 'pdf'),
                          pdf.write_pdf())

    @after_this_request
    def remove_file(response):
        try:
            os.remove(filename.format('output/', number, '', 'zip'))
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response

    return send_file(filename.format('output/', number, '', 'zip'),
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
