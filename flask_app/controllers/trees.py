from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.tree import Tree


@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    tree = Tree.get_all_trees()
    user = User.get_user(data)
    return render_template("dashboard.html", user=user, tree = tree)


@app.route("/users/create", methods=["POST"])
def create_tree():
    if "user_id" not in session:
        return redirect('/dashboard')
    valid = Tree.validate_tree(request.form)
    if valid:
        data = {
        'species': request.form['species'],
        'location': request.form['location'],
        'reason': request.form['reason'],
        'date_planted' : request.form['date_planted'],
        'user_id' : session['user_id']
        }
        trees = Tree.create_tree(data)
    return  redirect("/new/tree")

@app.route("/new/tree")
def new_tree():
    return render_template("new_tree.html")

@app.route("/trees/<int:tree_id>/update", methods=["POST"])
def update_tree(tree_id):
    if "user_id" not in session:
        return redirect('/dashboard')
    valid = Tree.validate_tree(request.form)
    if valid:
        data = {
        'species': request.form['species'],
        'location': request.form['location'],
        'reason': request.form['reason'],
        'date_planted' : request.form['date_planted'],
        'id' : tree_id
        }
        Tree.update(data)
    return redirect(f'/trees/{tree_id}/edit')


@app.route('/trees/<int:tree_id>/edit')
def edit_tree(tree_id):
    data = {
        'id': tree_id
    }
    return render_template('edit.html', tree = Tree.get_tree(data))


@app.route("/show/<int:tree_id>")
def view_tree(tree_id):
    data = {
        'id': tree_id
    }
    return render_template('show.html', tree = Tree.get_tree(data))

@app.route("/user/account")
def user_account():
    data = {
        "id": session["user_id"]
    }
    tree = Tree.get_all_trees()
    user = User.get_user(data)
    return render_template("my_tree.html", user=user, tree = tree)

@app.route("/trees/<int:tree_id>/delete")
def delete_tree(tree_id):
    data={
        "id": tree_id
    }
    Tree.delete(data)
    return redirect('/dashboard')
