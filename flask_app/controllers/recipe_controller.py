from flask import render_template, request, redirect, session, flash

from flask_app import app

# shouldn't need Bcrypt bc not encypting any in any recipe routes
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)

from flask_app.models.recipe import Recipe
from flask_app.models.user import User

### NEW RECIPE ROUTES

@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        flash ('Please login or register to continue')
        return redirect('/')

    return render_template('add_recipe.html')

@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    # validate form info
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')

    # collect query data
    query_data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'time' : request.form['time'],
        'date' : request.form['date'],
        'created_at' : 'NOW()',
        'updated_at' : 'NOW()',
        'user_id' : session['user_id']
    }
    # query using data (insert)
    Recipe.create_recipe(query_data)

    return redirect('/dashboard')

@app.route('/recipes/<int:recipe_id>')
def get_one_recipe(recipe_id):
    if 'user_id' not in session:
        flash ('Please login or register to continue')
        return redirect('/')
        

    # gather query data
    query_data = {
        'recipe_id' : recipe_id
    }
    # query using data
    recipe = Recipe.get_one_recipe(query_data)

    # recipe (gets passed to HTML) = recipe (being passed in from function)
    return render_template ('show_recipe.html', recipe = recipe)

### EDIT ROUTES

@app.route('/recipes/edit/<int:recipe_id>')
def show_edit_recipe(recipe_id):
    if 'user_id' not in session:
        flash ('Please login or register to continue')
        return redirect('/')

    query_data = {
        'recipe_id' : recipe_id
    }
    recipe = Recipe.get_one_recipe(query_data)

    return render_template ('update_recipe.html', recipe = recipe)

@app.route('/recipes/update/<int:recipe_id>', methods = ['POST'])
def edit_recipe(recipe_id):
    # validate information
    if not Recipe.validate_recipe(request.form):
        redirect(f'/recipes/edit/{recipe_id}')
    # gather query data
    query_data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date': request.form['date'],
        'time': request.form['time'],
        'recipe_id' : recipe_id
    }
    # query with data
    Recipe.edit_recipe(query_data)
    # update - and delete - queries will always return nothing, so don't need to pass them in as a variable
    return redirect ('/dashboard')

### DELETE ROUTE

@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    # gather query data, run query, redirect elsewhere
    query_data = {
        'recipe_id' : recipe_id
    }

    Recipe.delete_recipe(query_data)

    return redirect ('/dashboard')