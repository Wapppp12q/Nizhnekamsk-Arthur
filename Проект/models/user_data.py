import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users_data'

    id = Column(Integer, primary_key=True)
    email = relationship('Reg')
    name = Column(String)
    surname = Column(String)
    hashed_password = Column(String)

    def __repr__(self):
        info: str = f'Данные [ID: {self.id}, Почта: {self.email}, Имя: {self.name}, ' \
                    f'Фамилия: {self.surname}, Пароль: {self.hashed_password}]'

        return info