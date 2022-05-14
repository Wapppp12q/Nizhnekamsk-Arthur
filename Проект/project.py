import datetime

from flask import Flask, render_template, redirect, request
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from validate_email import validate_email
import shutil

from exams.ex_code import exam_code
from exams.pass_exam import exam

from mail_sender import send_mail
from hashed_password import set_password, check_password
from replace import replacce

from forms.registerform import RegisterForm
from forms.verification import VerifForm
from forms.register_data import DataForm
from forms.page import PageForm
from forms.entrance import Entrance
from forms.recovery import Recovery
from forms.rec_data import RDataForm

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


def entr_ex(email, password):
    exam_email = False
    db_sess = database.create_session()
    for em in db_sess.query(Reg.email).all():
        em = replacce(str(*em))
        if str(email) == em:
            exam_email = True
            break

    if exam_email:
        pas = replacce(str(*db_sess.query(Data.hashed_password).filter(Reg.email == email)))
        db_sess.close()
        return check_password(pas, password)
    else:
        db_sess.close()
        return False


def allowed_file(filename):
    if '.' in filename:
        fname = filename.rsplit('.', 1)[1].lower()
        if fname in ALLOWED_EXTENSIONS:
            return True

    return False


@app.route('/upload/<id_ver>', methods=['GET', 'POST'])
def upload_file(id_ver):
    error = ''
    path_im = ''
    id_ver = int(id_ver)
    db_sess = database.create_session()
    email = replacce(str(*db_sess.query(Reg.email).filter(Reg.id == id_ver)))
    page_data = db_sess.query(PData).filter(PData.page_id == id_ver).first()

    if request.method == 'POST':
        if 'file' not in request.files:
            error = "Нет файловой части"
        else:
            file = request.files['file']
        if file.filename == '':
            error = "Файл не выбран"

        if file and allowed_file(file.filename):
            for photo in os.walk(f'static/image/{email}'):
                for elem in photo[2]:
                    if elem.split('.')[0] == 'avatar':
                        os.remove(f'static/image/{email}/{elem}')
                        break
                break
            file.filename = 'avatar.' + file.filename.split('.')[-1]
            filename = secure_filename(file.filename)
            path_im = '/static/image/' + email + '/' + filename
            page_data.avatar = path_im
            file.save(os.path.join(UPLOAD_FOLDER + '/' + email, filename))
            db_sess.commit()
            db_sess.close()
            return redirect(f'/page/{id_ver}')

        else:
            db_sess.close()
            error = 'Неверный формат фотографии'

    return render_template('upload.html', title='Загрузка фото', error=error, src=path_im)


# Пароль, чтобы не придумывать YUGDsdf12#%fdg
@app.route('/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
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
                user_reg = Reg(code_ver=code, email=email)
                db_sess.add(user_reg)
                db_sess.commit()
                id_ver = int(replacce(str(*db_sess.query(Reg.id).filter(Reg.email == addr_to))))
                db_sess.close()
                addr_to_sec = cr_sec_email(addr_to)
                rec = False

                return redirect(f"/verification/{id_ver}/{addr_to_sec}/{rec}")

            else:
                error = 'Такая почта уже зарегистрирована'
            db_sess.close()
        else:
            error = "Такой почты не существует"

    elif form.submit.data:
        error = 'Введите почту'

    return render_template('reg.html', title='Регистрация', form=form, error=error)


@app.route('/register_data/<id_ver>', methods=['GET', 'POST'])
def register_data(id_ver):
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
            db_sess = database.create_session()
            email = replacce(str(*db_sess.query(Reg.email).filter(Reg.id == id_ver)))
            user_data = Data(name=name, surname=surname, created_date=created_data, user_id=id_ver,
                             hashed_password=hashed_password)
            avatar = f'/static/image/{email}/avatar.jpeg'
            status = 'Я пользуюсь Boot'
            page_data = PData(status=status, avatar=avatar, page_id=id_ver)
            direc = PATH_DIC + '/' + email
            os.mkdir(direc)
            shutil.copy('static/image/avatar.jpeg', f'static/image/{email}')
            db_sess.add(user_data)
            db_sess.add(page_data)
            db_sess.commit()
            db_sess.close()
            return redirect(f'/page/{id_ver}')

    elif form.submit.data:
        error = 'Введите данные'

    return render_template('register_data.html', title='Регистраци данных', form=form, error=error)


@app.route('/verification/<id_ver>/<sec_email>/<rec>', methods=['GET', 'POST'])
def verification(id_ver, sec_email, rec):
    error = ''
    form = VerifForm()
    id_ver = int(id_ver)

    if form.validate_on_submit():
        db_sess = database.create_session()
        code_db = replacce(str(*db_sess.query(Reg.code_ver).filter(Reg.id == id_ver)))
        db_sess.close()
        bool_code = exam_code(form.code_str.data, code_db)

        if bool_code:
            if rec == 'False':
                return redirect(f'/register_data/{id_ver}')
            else:
                return redirect(f'/recovery_data/{id_ver}/{sec_email}')
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

    if form.reg.data:
        return redirect('/register')

    if form.rec.data:
        return redirect('/recovery')

    if form.validate_on_submit():
        db_sess = database.create_session()
        truth_user = entr_ex(form.email.data.strip(), form.password.data.strip())
        id = replacce(str(*db_sess.query(Reg.id).filter(Reg.email == form.email.data)))
        db_sess.close()
        if truth_user:
            return redirect(f'/page/{id}')
        else:
            error = 'Неверный логин или пароль'

    elif form.submit.data:
        error = 'Введите данные'

    return render_template('entrance.html', title='Вход', form=form, truth_user=truth_user, error=error)


@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    exam_email = False
    form = Recovery()
    code = create_code()
    recov = True
    error = ''

    if form.validate_on_submit():
        db_sess = database.create_session()
        for em in db_sess.query(Reg.email).all():
            em = replacce(str(*em))
            if str(form.email.data).strip() == em:
                exam_email = True
                break
        if exam_email:
            sec_email = cr_sec_email(form.email.data)
            id_ver = int(replacce(str(*db_sess.query(Reg.id).filter(Reg.email == form.email.data.strip()))))
            send_mail(str(form.email.data).strip(), code)
            user_reg = db_sess.query(Reg).filter(Reg.id == id_ver).first()
            user_reg.code_ver = code
            db_sess.commit()
            db_sess.close()
            return redirect(f'/verification/{id_ver}/{sec_email}/{recov}')
        else:
            error = 'Аккаунта с такой почтой не существует'
    elif form.submit.data:
        error = 'Введите данные'
    return render_template('recovery.html', form=form, title='Восстановление пароля', error=error)


@app.route('/recovery_data/<id>/<sec_email>', methods=['GET', 'POST'])
def recovery_data(id, sec_email):
    form = RDataForm()
    error = ''
    id = int(id)

    if form.validate_on_submit():
        error = exam(form.password.data.strip(), form.pass_exam.data.strip())
        if type(error) == bool:
            db_sess = database.create_session()
            user_data = db_sess.query(Data).filter(Data.user_id == id).first()
            new_password = set_password(form.password.data.strip())
            user_data.hashed_password = new_password
            db_sess.commit()
            db_sess.close()
            return redirect(f'/page/{id}')
    elif form.submit.data:
        error = 'Введите пароли'

    return render_template('rec_data.html', form=form,
                           title='Новый пароль', error=error, sec_email=sec_email)


@app.route("/page/<id_ver>", methods=['POST', 'GET'])
def page(id_ver):
    id_ver = int(id_ver)
    db_sess = database.create_session()
    src_res = str(*db_sess.query(PData.avatar).filter(PData.page_id == id_ver))
    src = replacce(src_res)
    name = str(*db_sess.query(Data.name).filter(Data.user_id == id_ver))
    surname = str(*db_sess.query(Data.surname).filter(Data.user_id == id_ver))
    name = replacce(name)
    surname = replacce(surname)
    form = PageForm()


    if form.submit.data:
        return redirect(f'/upload/{id_ver}')

    return render_template('page.html', title='Boot', form=form, src=src, name=name, surname=surname)


if __name__ == '__main__':
    database.global_init(DATABASE_NAME)
    app.run(host="127.0.0.1", port='8000', debug=True)
