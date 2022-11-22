from sqlalchemy import create_engine
from sqlalchemy import update, delete
from sqlalchemy.orm import sessionmaker

from utils.db_api.base import Base
from utils.db_api.models import Admin, Users

db_string = r"sqlite:///database.db"
db = create_engine(db_string)  

Session = sessionmaker(db)  
session = Session()

Base.metadata.create_all(db)

class Database:
    def reg_user(self, user_id, balance = 0):
        """Some docs"""
        session.merge(Users(user_id = user_id, 
                            balance = balance))
        session.commit()
    

    def get_user(self, user_id):
        """Some docs"""
        user = session.query(Users).filter(Users.user_id == user_id).first()
        return user       
    

    def get_user_balance(self, user_id):
        """Some docs"""
        user = session.query(Users).filter(Users.user_id == user_id).first()
        return user.balance
    

    def update_balance(self, user_id, new_balance):
        """Some docs"""
        session.execute(
            update(Users).filter(Users.user_id == user_id).
            values(balance = new_balance)
            )
        session.commit()
    

    # ----ADMIN----
    def get_status(self, name):
        """Some docs"""
        panel = session.query(Admin).filter(Admin.name == name).first()
        return panel.status


    def update_status(self, name):
        """Some docs"""
        d = {
            '🟢': '🔴',
            '🔴': '🟢'
        }
        current = self.get_status(name)

        session.execute(
            update(Admin).filter(Admin.name == name).
            values(status = d[current])
            )
        session.commit()

    
    def get_sum_balance(self):
        """Some docs"""
        users = session.query(Users).all()
        users_sum = sum([x.balance for x in users])

        return users_sum