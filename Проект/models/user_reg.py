from sqlalchemy import Column, INTEGER, String, ForeignKey, DateTime

from .database import Base


class Reg(Base):
    __tablename__ = 'users_reg'

    id = Column(INTEGER, primary_key=True)
    email = Column(String, ForeignKey('users_data.id'))
    code_ver = Column(INTEGER)
    created_date = Column(DateTime)

    def __repr__(self):
        info: str = f'Пользователь [ID: {self.id}, Почта: {self.email},' \
                    f' Код: {self.code_ver}, Время: {self.created_date}]'

        return info