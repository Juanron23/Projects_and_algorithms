from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Tree:
    db = "arbotrary"
    def __init__(self, data):
        self.tree_id =data['tree_id']
        self.species = data['species']
        self.location = data['location']
        self.reason = data['reason']
        self.date_planted = data['date_planted']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def create_tree(cls, form_data):
        query = "INSERT INTO trees(species,location,reason,date_planted,user_id) VALUES (%(species)s, %(location)s, %(reason)s, %(date_planted)s, %(user_id)s)"
        return connectToMySQL("arbotrary").query_db(query, form_data)

    @classmethod
    def get_all_trees(cls):
        query= "SELECT * FROM trees"
        results = connectToMySQL("arbotrary").query_db(query)
        trees = []
        for row in results:
            trees.append(cls(row))
        return trees

    @classmethod
    def get_tree(cls, data):
        query= "SELECT * FROM trees WHERE tree_id = %(id)s"
        results = connectToMySQL("arbotrary").query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])


#under you have WHERE id = %(id)s" becuase you are updating youre tree table with the
#  id of id with the actual id the tree created which is id
    @classmethod
    def update(cls, data):
        query = "UPDATE trees SET species=%(species)s, location=%(location)s, reason=%(reason)s, date_planted=%(date_planted)s WHERE tree_id = %(id)s"
        return connectToMySQL("arbotrary").query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM trees WHERE tree_id = %(id)s"
        return connectToMySQL("arbotrary").query_db(query, data)


    @staticmethod
    def validate_tree(data):
        is_valid = True
        if len(data['species']) < 5:
            flash("species name must be at least 5 characters", "error")
            is_valid = False
        if len(data['location']) < 2:
            flash("Location must be atleast 2 characters", "error")
            is_valid = False
        if len(data['reason']) > 50 :
            flash("reason must be maximum 50 charaters", "error")
            is_valid = False
        return is_valid

