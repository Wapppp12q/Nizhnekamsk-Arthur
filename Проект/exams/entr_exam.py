from Проект.models import database
from Проект.models.users_reg import Reg
from Проект.models.users_data import Data

from Проект.hashed_password import check_password


def entr_ex(email, password):
    exam_email = False
    db_sess = database.create_session()
    for em in db_sess.query(Reg.email).all():
        em = str(*em)
        if str(email) == em:
            exam_email = True
            break

    if exam_email:
        for pas in db_sess.query(Data.hashed_password).filter(Reg.email == email):
            return check_password(pas, password)
    else:
        return False
