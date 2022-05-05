from faker import Faker

from models.database import create_db, Session
from models.user_reg import Reg
from models.user_data import User


def create_database(load_fake_data: bool = True):
    create_db()
