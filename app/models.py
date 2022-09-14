from datetime import datetime

from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.database.database import base, session

"""All models used: EmployeeModel, RestaurantModel, MenuModel, VoteModel, RevokedTokenModel"""


class VoteModel(base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    menu_id = Column(Integer, ForeignKey('menus.id'))
    employee = relationship("EmployeeModel", back_populates='votes')
    menu = relationship("MenuModel", back_populates='votes')

    @classmethod
    def find_by_id(cls, id_, to_dict=True):
        """Method for finding selected vote by id"""
        vote = session.query(cls).filter_by(id=id_).first()
        if not vote:
            return {}
        if to_dict:
            return cls.to_dict(vote)
        else:
            return vote

    @classmethod
    def find_by_employee_id(cls, employee_id, offset, limit):
        """
            Method for finding selected votes by employee_id
            Returns list of dictionaries
        """
        votes = session.query(cls).filter_by(employee_id=employee_id) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(s) for s in votes]

    @classmethod
    def find_by_menu_id(cls, menu_id, offset, limit):
        """
            Method for finding selected votes by menu_id
            Returns list of dictionaries
        """
        votes = session.query(cls).filter_by(session_id=menu_id) \
            .order_by(cls.id).offset(offset).limit(limit).all()
        return [cls.to_dict(s) for s in votes]

    @classmethod
    def return_all(cls):
        """Method to return all votes"""
        votes = session.query(cls).order_by(cls.id).all()
        return [cls.to_dict(vote) for vote in votes]

    @classmethod
    def delete_by_id(cls, id_):
        """Method to delete vote by id"""
        vote = session.query(cls).filter_by(id=id_).first()
        if vote:
            session.delete(vote)
            session.commit()
            return 200
        else:
            return 404

    def save_to_db(self):
        """Method to save changes into DB"""
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(vote):
        """Method to get a dict with fields"""
        return {
            "id": vote.id,
            "employee_id": vote.employee_id,
            "menu_id": vote.menu_id
        }


class MenuModel(base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(), default=datetime.utcnow)
    number_votes = Column(Integer, default=0)
    first = Column(String(30), nullable=False)
    second = Column(String(30), nullable=False)
    drink = Column(String(30), nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant = relationship("RestaurantModel", back_populates='menus')
    votes = relationship(VoteModel, lazy='dynamic',
                           cascade="all, delete-orphan",
                           foreign_keys="VoteModel.menu_id")

    @classmethod
    def find_by_id(cls, id_, to_dict=True):
        """Method for finding selected menu by id"""
        menu = session.query(cls).filter_by(id=id_).first()
        if not menu:
            return {}
        if to_dict:
            return cls.to_dict(menu)
        else:
            return menu

    # @classmethod
    # def find_by_restaurant_id(cls, restaurant_id, offset, limit):
    #     """
    #         Method for finding menus by restaurant_id
    #         Returns list of dictionaries
    #     """
    #     from_date = datetime(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day,
    #                          hour=datetime.now().hour, minute=datetime.now().minute, second=datetime.now().second)
    #     sessions = session.query(cls).filter(SessionModel.started_at >= from_date).filter_by(film_id=film_id) \
    #         .order_by(cls.id).offset(offset).limit(limit).all()
    #     return [cls.to_dict(s) for s in sessions]

    @classmethod
    def delete_by_id(cls, id_):
        """Method to delete menu by id"""
        menu = session.query(cls).filter_by(id=id_).first()
        if menu:
            session.delete(menu)
            session.commit()
            return 200
        else:
            return 404

    @classmethod
    def return_all(cls):
        """Method to return all menus"""
        from_date = datetime(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, )
        menus = session.query(cls).filter(MenuModel.date >= from_date).order_by(cls.id).all()
        return [cls.to_dict(menu) for menu in menus]


    @staticmethod
    def adjust_number_votes(menu_id):
        menu = MenuModel.find_by_id(menu_id, to_dict=False)
        menu.number_votes += 1
        menu.save_to_db()


    @classmethod
    def find_by_first(cls, first):
        """
            Method for finding menus by first dish
            Returns list of dictionaries
        """
        if first:
            menus = session.query(MenuModel).filter(MenuModel.first == first).all()
        else:
            menus = cls.return_all()
        return [cls.to_dict(menu) for menu in menus]

    @classmethod
    def find_by_name(cls, name):
        """
            Method for finding menu by restaurant name
            Returns list of dictionaries
        """
        from_date = datetime(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        if name:
            menus = session.query(cls).join(RestaurantModel).filter(RestaurantModel.name == name).filter(MenuModel.date >= from_date).all()
        else:
            menus = cls.return_all()
        return [cls.to_dict(menu) for menu in menus]

    @classmethod
    def find_by_second(cls, second):
        """
            Method for finding menus by second dish
            Returns list of dictionaries
        """
        if second:
            menus = session.query(MenuModel).filter(MenuModel.second == second).all()
        else:
            menus = cls.return_all()
        return [cls.to_dict(menu) for menu in menus]

    @classmethod
    def find_by_drink(cls, drink):
        """
            Method for finding menus by drink
            Returns list of dictionaries
        """
        if drink:
            menus = session.query(MenuModel).filter(MenuModel.drink == drink).all()
        else:
            menus = cls.return_all()
        return [cls.to_dict(menu) for menu in menus]

    def save_to_db(self):
        """Method to save changes into DB"""
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(menu):
        """Method to get a dict with fields"""
        return {
            "id": menu.id,
            "date": menu.date,
            "restaurant_id": menu.restaurant_id,
            "number_votes": menu.number_votes,
            "first": menu.first,
            "second": menu.second,
            "drink": menu.drink
        }


class RestaurantModel(base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    resp_username = Column(String(30), nullable=False)
    menus = relationship(MenuModel, lazy='dynamic',
                            cascade="all, delete-orphan",
                            foreign_keys="MenuModel.restaurant_id")

    @classmethod
    def find_by_id(cls, id_, to_dict=True):
        """Method for finding selected restaurant by id"""
        restaurant = session.query(cls).filter_by(id=id_).first()
        if not restaurant:
            return {}
        if to_dict:
            return cls.to_dict(restaurant)
        else:
            return restaurant

    @classmethod
    def return_all(cls):
        """Method to return all restaurants"""
        restaurants = session.query(cls).order_by(cls.id).all()
        return [cls.to_dict(restaurant) for restaurant in restaurants]

    @classmethod
    def delete_by_id(cls, id_):
        """Method to delete restaurant by id"""
        restaurant = session.query(cls).filter_by(id=id_).first()
        if restaurant:
            session.delete(restaurant)
            session.commit()
            return 200
        else:
            return 404

    def save_to_db(self):
        """Method to save changes into DB"""
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(restaurant):
        """Method to get a dict with fields"""
        return {
            "id": restaurant.id,
            "name": restaurant.name,
            "resp_username": restaurant.resp_username
        }


class EmployeeModel(base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    username = Column(String(30), nullable=False)
    email = Column(String(30), nullable=False)
    hashed_password = Column(String(50), nullable=False)
    is_admin = Column(Boolean(), default=False)
    votes = relationship(VoteModel, lazy='dynamic',
                           cascade="all, delete-orphan",
                           foreign_keys="VoteModel.employee_id")

    @classmethod
    def find_by_id(cls, id_, to_dict=True):
        """Method for finding selected employee by id"""
        employee = session.query(cls).filter_by(id=id_).first()
        if not employee:
            return {}
        if to_dict:
            return cls.to_dict(employee)
        else:
            return employee

    @classmethod
    def find_by_username(cls, username, to_dict=True):
        """Method for finding selected employee by username"""
        employee = session.query(cls).filter_by(username=username).first()
        if not employee:
            return {}
        if to_dict:
            return cls.to_dict(employee)
        else:
            return employee

    @classmethod
    def find_by_email(cls, email, to_dict=True):
        """Method for finding selected employee by email"""
        employee = session.query(cls).filter_by(email=email).first()
        if not employee:
            return {}
        if to_dict:
            return cls.to_dict(employee)
        else:
            return employee

    @classmethod
    def return_all(cls):
        """Method to return all employees"""
        employees = session.query(cls).order_by(cls.id).all()
        return [cls.to_dict(employee) for employee in employees]

    @classmethod
    def delete_by_id(cls, id_):
        """Method to delete employee by id"""
        employee = session.query(cls).filter_by(id=id_).first()
        if employee:
            session.delete(employee)
            session.commit()
            return 200
        else:
            return 404

    def save_to_db(self):
        """Method to save changes into DB"""
        session.add(self)
        session.commit()

    @staticmethod
    def to_dict(employee):
        """Method to get a dict with fields"""
        return {
            "id": employee.id,
            "name": employee.name,
            "username": employee.username,
            "email": employee.email,
            "is_admin": employee.is_admin,
        }

    @staticmethod
    def generate_hash(password):
        """Method for generating hashed password"""
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash_):
        """Method to verify password"""
        return sha256.verify(password, hash_)


class RevokedTokenModel(base):
    __tablename__ = 'revoked_tokens'
    id_ = Column(Integer, primary_key=True)
    jti = Column(String(120))
    blacklisted_on = Column(DateTime, default=datetime.utcnow)

    def add(self):
        """Method to save changes into DB"""
        session.add(self)
        session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        """Method to check if this unique identifier for token is in blacklist"""
        query = session.query(cls).filter_by(jti=jti).first()
        return bool(query)
