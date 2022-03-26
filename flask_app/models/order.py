from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Order:
    db_name = "group_project"

    def __init__(self, data):
        self.id = data['id']
        self.method = data['method']
        self.size = data['size']
        self.crust = data['crust']
        self.qty = data['qty']
        self.topping = data['topping']
        self.create_at = data['create_at']
        self.upload_at = data['upload_at']
        self.user_id = data['user_id']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO orders (method, size, crust, qty, topping, user_id) VALUES(%(method)s,%(size)s,%(crust)s,%(qty)s, %(topping)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM orders;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM orders WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])