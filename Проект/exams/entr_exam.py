from Проект.models.database import Session
from Проект.models.user_data import User
from Проект.hashed_password import check_password


session = Session()


def entr_ex(email, password):
    global session
    exam_email = False
    for em in session.query(User.email).all():
        em = str(*em)
        if str(email) == em:
            exam_email = True
            break

    if exam_email:
        for pas in session.query(User.hashed_password).filter(User.email == email):
            return check_password(pas, password)
    else:
        return False
