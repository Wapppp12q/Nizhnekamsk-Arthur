import datetime

from flask import Flask, render_template, redirect, Blueprint
from flask import request, url_for, flash, send_from_directory, Request
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
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

from models import database
from models.users_reg import Reg
from models.users_data import Data
from models.page_data import PData

from cr_code import create_code
from create_secret_email import cr_sec_email

UPLOAD_FOLDER = 'C:\\Users\\artur\\PycharmProjects\\Project\\Проект\\static\\image'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
DATABASE_NAME = 'db/users.sqlite'
PATH_DIC = r'C:\Users\artur\PycharmProjects\Project\Проект\static\image'

load_dotenv()

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'fdgjj54569*FJ$84jgf@#_fdsgf897435hj89wq8*SRF89dsgkjs8g7*(&*(&%giodsg5ten0&r(9Br37h8'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    if '.' in filename:
        fname = filename.rsplit('.', 1)[1].lower()
        if fname in ALLOWED_EXTENSIONS:
            return True

    return False


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    error = ''
    if request.method == 'POST':
        if 'file' not in request.files:
            error = "Нет файловой части"
        else:
            file = request.files['file']
        if file.filename == '':
            error = "Файл не выбран"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('upload.html', title='Загрузка фото', error=error)


# http://127.0.0.1:8000/register
# Пароль, чтобы не придумывать YUGDsdf12#%fdg
@app.route('/', methods=['GET', 'POST'])
def register():
    global PATH_DIC

    code = create_code()

    error = ''
    form = RegisterForm()
    if form.entrance.data:
        return redirect('/entrance')
    if form.validate_on_submit():
        addr_to = form.email.data.strip()
        if validate_email(addr_to):
            valid = True
            db_sess = database.create_session()
            for item in db_sess.query(Reg.email).all():
                item = str(*item)
                if addr_to == item:
                    valid = False
                    break
            if valid:
                send_mail(addr_to, code)
                email = addr_to
                code_ver = code
                user_reg = Reg(code_ver=code, email=email)
                db_sess.add(user_reg)
                db_sess.commit()
                id_ver = str(*db_sess.query(Reg.id).filter(Reg.email == addr_to)).replace(',', '')\
                    .replace('(', '').replace(')', '')
                db_sess.close()
                addr_to_sec = cr_sec_email(addr_to)
                return redirect(f"/verification/{id_ver}/{addr_to_sec}")
            else:
                error = 'Такая почта уже зарегистрирована'
            db_sess.close()
        else:
            error = "Такой почты не существует"

    elif form.submit.data:
        error = 'Введите почту'

    return render_template('reg.html', title='Регистрация', form=form, error=error)


@app.route('/register_data/<id_ver>/<sec_email>', methods=['GET', 'POST'])
def register_data(id_ver, sec_email):
    error = ''
    id_ver = int(id_ver)
    form = DataForm()
    if form.validate_on_submit():
        error = exam(form.password.data, form.pass_exam.data)
        if type(error) == bool:
            hashed_password = set_password(form.password.data)
            name = form.name.data
            surname = form.surname.data
            created_data = datetime.datetime.now()
            user_data = Data(name=name, surname=surname, created_date=created_data, user_id=id_ver,
                             hashed_password=hashed_password)
            avatar = '/static/image/avatar.jpeg'
            status = 'Я пользуюсь Boot'
            page_data = PData(status=status, avatar=avatar, page_id=id_ver)
            db_sess = database.create_session()
            email = str(*db_sess.query(Reg.email).filter(Reg.id == id_ver)).replace(',', '')\
                    .replace('(', '').replace(')', '')
            direc = PATH_DIC + '/' + email
            os.mkdir(direc)
            db_sess.add(user_data)
            db_sess.add(page_data)
            db_sess.commit()
            db_sess.close()
            return redirect(f'/page/{id_ver}')
    return render_template('register_data.html', title='Регистраци данных', form=form, error=error)


@app.route('/verification/<id_ver>/<sec_email>', methods=['GET', 'POST'])
def verification(id_ver, sec_email):
    error = ''
    id_ver = int(str(id_ver).strip().replace('(', '').replace(')', ''))
    form = VerifForm()
    if form.validate_on_submit():
        db_sess = database.create_session()
        code_db = str(*db_sess.query(Reg.code_ver).filter(Reg.id == id_ver)).replace(',', '')
        code_db = code_db.replace('(', '').replace(')', '')
        db_sess.close()
        bool_code = exam_code(form.code_str.data, code_db)
        if bool_code:
            return redirect(f'/register_data/{id_ver}/{sec_email}')
        else:
            error = 'Неверный код'
    elif form.submit.data:
        error = 'Введите код'
    return render_template('verification.html', title='Подтверждение почты', form=form, error=error,
                           sec_email=sec_email)


@app.route('/entrance', methods=['GET', 'POST'])
def entrance():
    error = ''
    truth_user = False
    form = Entrance()
    if form.validate_on_submit():
        truth_user = entr_ex(form.password.data.strip(), form.email.data.strip())
        db_sess = database.create_session()
        id = str(*db_sess.query(Reg.id).filter(Reg.email == form.email.data)).replace(',', '').replace('(', '')\
            .replace(')', '')
        db_sess.close()
        if truth_user:
            return redirect(f'/page/{id}')
        else:
            error = 'Неверный логин или пароль'
    elif form.submit.data:
        error = 'Введите данные'
    return render_template('entrance.html', title='Вход', form=form, truth_user=truth_user, error=error)


@app.route("/page/<id>", methods=['POST', 'GET'])
def page(id):
    id = int(str(id).replace('(', '').replace(')', ''))
    db_sess = database.create_session()
    src_res = str(*db_sess.query(PData.avatar).filter(PData.page_id == id))
    src = src_res.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
    name = str(*db_sess.query(Data.name).filter(Data.user_id == id))
    surname = str(*db_sess.query(Data.surname).filter(Data.user_id == id))
    name = name.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
    surname = surname.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
    form = PageForm()
    if form.submit.data:
        return redirect(f'/upload/{id}')
    return render_template('page.html', title='Boot', form=form, src=src, name=name, surname=surname)


if __name__ == '__main__':
    database.global_init(DATABASE_NAME)
    app.run(host="127.0.0.1", port='8000', debug=True)
