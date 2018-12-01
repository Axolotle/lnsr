from os import remove as removeFile
from zipfile import ZipFile, ZIP_DEFLATED
from random import randint

from flask import Flask, request, render_template, Response, send_file, after_this_request, session, jsonify
from flask_weasyprint import HTML, render_pdf

from generators.ruler import ruler
from generators.background import get_background_anim, get_background_img
from generators.helpers import get_content_numbers

app = Flask(__name__)
app.secret_key = 'lel'

lnsr = 100

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/rulerRequest', methods=['POST'])
def ruler_request():
    if not 'number' in session:
        global lnsr
        lnsr = lnsr + 1
        session['number'] = lnsr
    return jsonify({
        'number': session['number'],
        **get_content_numbers(session['number'])
    })

@app.route('/download')
def file_generation():
    if not 'number' in session:
        return '404'
    else:
        number = session['number']
        session.clear()

    filename_zip = 'output/light-nanosecond_ruler{}.zip'.format(number)
    filename = 'light-nanosecond_ruler{}{}.{}'
    pdf = HTML(string=render_template(
        'certificate.html',
        ruler=ruler.generate_string(number, 'pdf'),
        bg=get_background_img(),
        **get_content_numbers(number)
    ))

    with ZipFile(filename_zip, 'w', ZIP_DEFLATED) as zip_file:
        zip_file.writestr(filename.format(number, '-laser', 'svg'),
                          ruler.generate_string(number, 'laser'))
        zip_file.writestr(filename.format(number, '-certificate', 'pdf'),
                          pdf.write_pdf())

    @after_this_request
    def remove_file(response):
        try:
            removeFile(filename_zip)
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response

    return send_file(filename_zip, as_attachment=True)

@app.route('/pdf')
def pdf():
    pdf = HTML(string=render_template(
        'certificate.html',
        ruler=ruler.generate_string(lnsr, 'pdf'),
        bg=get_background_img(),
        **get_content_numbers(lnsr)
    ))

    return render_pdf(pdf)

@app.route('/ruler')
def ruler_root():
    return Response(response=ruler.generate_string(2, 'laser'), content_type='image/svg+xml')

@app.route('/lightSpeed.svg')
def light_speed_background():
    return Response(response=get_background_anim(), content_type='image/svg+xml')

if __name__ == '__main__':
    app.run(debug=True)
