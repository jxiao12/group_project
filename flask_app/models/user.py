from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    db_name = "group_project"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.password = data['password']
        self.create_at = data['create_at']
        self.upload_at = data['upload_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO user (first_name, last_name, email, address, city, state, password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(address)s,%(city)s,%(state)s,%(password)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE user SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, address=%(address)s, password=%(password)s, city=%(city)s, state=%(state)s,upload_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['first_name']) < 2:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
        return is_valid