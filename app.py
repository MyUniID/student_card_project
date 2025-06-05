from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import random

app = Flask(__name__)


UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def generate_student_id():
    return ''.join([str(random.randint(0, 9)) for _ in range(9)])

@app.route('/')
def home():
    return redirect(url_for('form'))

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/preview', methods=['POST'])
def preview():
    if 'photo' not in request.files or request.files['photo'].filename == '':
        return "لم يتم رفع صورة"

    photo = request.files['photo']  # الحصول على الملف المُرسل من حقل "photo" في الفورم
    photo_filename = secure_filename(photo.filename)
    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))  # تصحيح المسار وتعديل المسافة البادئة

    faculty = request.form.get('faculty')
    if not faculty:
        return "خطأ: حقل الكلية مطلوب", 400

    student_id = generate_student_id()

    return render_template('preview.html',
                           first_name=request.form['first_name'],
                           last_name=request.form['last_name'],
                           passport_number=request.form['passport_number'],
                           birth_date=request.form['birth_date'],
                           birth_place=request.form['birth_place'],
                           academic_year=request.form['academic_year'],
                           highschool_type=request.form['highschool_type'],
                           highschool_year=request.form['highschool_year'],
                           faculty=request.form['faculty'],
                           student_id=student_id,
                           photo_filename=photo_filename)


@app.route('/generate_card', methods=['POST'])
def generate_card():
    return render_template('generated.html', name=request.form['first_name'])

@app.route("/note")
def Note():
    return render_template("Note.html")

if __name__ == '__main__':
    app.run(debug=True)
