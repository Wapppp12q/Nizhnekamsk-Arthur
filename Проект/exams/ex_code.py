from Проект.models.database import Session
from Проект.models.user_reg import Reg


session = Session()


def exam_code(code, email):
    exist = False
    for code_db in session.query(Reg.code_ver).filter(Reg.email == email):
        code_db = str(*code_db)
        if code == code_db:
            exist = True
            break

    return exist
