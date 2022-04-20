from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import app
from flask_app.models import user

from flask import flash

# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)

class Recipe:
    db = "recipes"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.time = data['time']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # empty dictionary to represent a single instance of User
        # i.e. 1:m (every recipe has only one user)
        # alternative would be to do recipe = cls(result[0]) in classmethod
        self.user = {}
        self.user_id = data['user_id']

    @staticmethod
    def validate_recipe(form_data):
        is_valid = True

        if len(form_data['name']) < 3:
            flash('Name must be at least 3 characters')
            is_valid = False

        if len(form_data['description']) < 3:
            flash('Description must be at least 3 characters')
            is_valid = False

        if len(form_data['instructions']) < 3:
            flash('Instructions must be at least 3 characters')
            is_valid = False

        return is_valid

    @classmethod
    def show_all_recipes(cls):
        query ="SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;"

        results = connectToMySQL(cls.db).query_db(query)
        
        all_recipes = []
        for row in results:
            recipe = cls(row)
            user_data = {
                'id' : row['users.id'],
            'first_name' :row['first_name'],
            'last_name' : row['last_name'],
            'email' : row['email'],
            'password' : row['password'],
            'created_at' : row['users.created_at'],
            'updated_at' : row['users.updated_at']
            }
            recipe.user = user.User(user_data)
            all_recipes.append(recipe)        
            
        return all_recipes
    
    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, time, description, instructions, date, created_at, updated_at, user_id) VALUES ( %(name)s, %(time)s, %(description)s, %(instructions)s, %(date)s, NOW(), NOW(), %(user_id)s );"

        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(recipe_id)s;"

        query = "SELECT * FROM users WHERE users.id = %(users_id)s"
        
        results = connectToMySQL(cls.db).query_db(query, data)

        # i.e. an instance of the class Recipe
        recipe = cls(results[0])

        # remember to differentiate any attributes that conflict with attributes (i.e. table columns) of another class
        user_data = {
            'id' : results[0]['users.id'],
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'email' : results[0]['email'],
            'password' : results[0]['password'],
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at']
        }
        print(user_data)
        # recipe.user = user.User(user_data)
        recipe.user = user.User(user_data)
        return recipe

    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date = %(date)s, time = %(time)s, updated_at = NOW() WHERE recipes.id = %(recipe_id)s;"

        # UPDATE queries don't return any data so don't actually need to declare a variable (i.e. results) or return anything
        results = connectToMySQL(cls.db).query_db(query, data)
        return


    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(recipe_id)s"

        return connectToMySQL(cls.db).query_db(query, data)

