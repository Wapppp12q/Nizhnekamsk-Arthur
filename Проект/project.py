import datetime

from flask import Flask, render_template, redirect
from flask import request, url_for, flash, send_from_directory, Request
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from random import randrange
from validate_email import validate_email
from sqlalchemy import and_

from exams.ex_code import exam_code
from exams.pass_exam import exam
from exams.entr_exam import entr_ex

from mail_sender import send_mail
from hashed_password import set_password, check_password

from forms.registerform import RegisterForm
from forms.verification import VerifForm
from forms.register_data import DataForm
from forms.page import PageForm
from forms.entrance import Entrance

from models.database import DATABASE_NAME, Session, create_db
import create_database as cd
from models.user_reg import Reg
from models.user_data import User

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fdgjj54569*FJ$84jgf@#_fdsgf897435hj89wq8*SRF89dsgkjs8g7*(&*(&%giodsg5ten0&r(9Br37h8'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

session = Session()


def create_code():
    return randrange(100000, 1000000)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''


@app.route('/', methods=['GET', 'POST'])
def register():
    global session

    code = create_code()

    error = ''
    form = RegisterForm()
    if form.entrance.data:
        return redirect('/entrance')
    if form.validate_on_submit():
        addr_to = form.email.data.strip()
        if validate_email(addr_to):
            valid = True
            for item in session.query(Reg.email).all():
                item = str(*item)
                if addr_to == item:
                    valid = False
                    break
            if valid:
                send_mail(addr_to, code)
                user_reg = Reg(email=addr_to, code_ver=code, created_date=datetime.datetime.now())
                session.add(user_reg)
                session.commit()
                session.close()
                return redirect("/verification")
            else:
                error = 'Такая почта уже зарегистрирована'
        else:
            error = "Такой почты не существует"
    return render_template('reg.html', title='Авторизация', form=form, error=error)


@app.route('/register_data', methods=['GET', 'POST'])
def register_data():
    error = ''
    form = DataForm()
    if form.validate_on_submit():
        #error = exam(form.password.data, form.pass_exam.data)
        if True:
            # type(error) == bool:
            hashed_password = set_password(form.password.data)
            name = form.name.data
            surname = form.surname.data
            user_data = User('dfgdfgdfgdfg', name, surname, hashed_password)
            session.add(user_data)
            session.commit()
            session.close()
            return redirect('/page')
    return render_template('register_data.html', title='Регистраци данных', form=form, error=error)


@app.route('/verification', methods=['GET', 'POST'])
def verification():
    error = ''
    form = VerifForm()
    if form.validate_on_submit():
        #bool_code = exam_code(form.code_str.data, email)
        if True:#bool_code:
            return redirect('/register_data')
        else:
            error = 'Неверный код'
    else:
        'Введите код'
    return render_template('verification.html', title='Подтверждение почты', form=form, error=error)


@app.route('/entrance', methods=['GET', 'POST'])
def entrance():
    error = ''
    truth_user = False
    form = Entrance()
    if form.validate_on_submit():
        truth_user = entr_ex(form.email.data, form.password.data)
        if True:
            return redirect('/page')
        else:
            error = 'Неверный логин или пароль'
    return render_template('entrance.html', title='Вход', form=form, truth_user=truth_user, error=error)


@app.route("/page", methods=['POST', 'GET'])
def page():
    form = PageForm()
    return render_template('page.html', title='Boot', form=form)


if __name__ == '__main__':
    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        cd.create_database()
    session = Session()
    app.run(host="127.0.0.1", port='8000', debug=True)