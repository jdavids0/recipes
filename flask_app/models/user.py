from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import app
from flask_app.models import recipe

from flask import flash

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import re

EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "recipes"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # empty list to hold multiple cars
        # i.e. placeholder for 1:m (1 user has many recipes)
        self.recipes = []

    # use classmethod for queries, staticmethod for validations
    
    @staticmethod
    def validate_registration (form_data):
        is_valid = True

        if len(form_data['first_name']) < 2:
            flash('First name must be present', 'registration')
            is_valid = False

        if not form_data['first_name'].isalpha():
            flash('Name can only contain letters', 'registration')
            is_valid = False

        if len(form_data['last_name']) < 2:
            flash('Last name must be present', 'registration')
            is_valid = False

        if not form_data['last_name'].isalpha():
            flash('Name can only contain letters', 'registration')
            is_valid = False

        if len(form_data['email']) < 1:
            flash('Email must be present', 'registration')
            is_valid = False

        elif not EMAIL_REGEX.match(form_data['email']):
            flash('Email must have valid format', 'registration')
            is_valid = False

        if len(form_data['password']) < 8:
            flash('Password must be at least 8 characters long', 'registration')
            is_valid = False

        ### OPTIONAL ADDITIONAL PASSWORD REQUIREMENTS, NOT IMPLEMENTED

        # if not any(char.isdigit() for char in form_data['password']):
        #     flash('Password must contain at least one number')
        #     is_valid = False

        # if not any(char.isupper() for char in form_data['password']):
        #     flash('Password must contain at least one uppercase letter')
        #     is_valid = False

        if form_data['password'] != form_data['confirm_password']:
            flash('Password and confirmation password must match!','registration')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login (form_data):
        is_valid = True
        user_in_db = User.get_by_email(form_data)

        if not user_in_db:
            flash('Invalid Email or Password', 'login')
            is_valid = False
        
        elif not bcrypt.check_password_hash (user_in_db.password, form_data['password']):
            flash('Invalid Email or Password', 'login')
            is_valid = False
        
        return is_valid

    @classmethod
    def register_user (cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() )"

        results = connectToMySQL (cls.db).query_db(query, data)

        return results

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s"
        result = connectToMySQL(cls.db).query_db (query, data)

        if len (result) < 1:
            return False
        
        return cls (result[0])
    
    @classmethod
    def show_all_recipes(cls, data):
        query = "SELECT * FROM users LEFT JOIN recipes ON recipes.user_id = users.id WHERE users.id = %(user_id)s;"
        
        result = connectToMySQL(cls.db).query_db(query, data)

        user = []
        for row in result:
            recipe_data = {
                'id': row['recipes.id'],
                'name': row['name'],
                'time': row['time'],
                'date': row['date'],
                'instructions': row['instructions'],
                'description': row['description'],
                'created_at': row['recipes.created_at'],
                'updated_at': row['recipes.updated_at'],
                'user_id' : row['user_id']
            }
            recipe.user = recipe.Recipe(recipe_data)
            user.append(recipe_data)
    
    
        return user
        