from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Pie:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.filling = data['filling']
        self.crust = data['crust']
        self.creator = data['first_name']
        
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = (
            "INSERT INTO pies (name, filling, crust, creator_id, created_at, updated_at) "
            "VALUES ( %(name)s, %(filling)s, %(crust)s, %(creator_id)s, NOW(), NOW() );"
        )
        return connectToMySQL('pies_schema').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = (
            "UPDATE pies "
            "SET name=%(name)s, filling=%(filling)s, crust=%(crust)s, updated_at=NOW() "
            "WHERE id = %(pie_id)s;"
        )
        connectToMySQL('pies_schema').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = (
            "DELETE FROM pies WHERE id = %(pie_id)s;"
        )
        connectToMySQL('pies_schema').query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = (
            "SELECT * FROM pies "
            "JOIN users ON pies.creator_id = users.id "
            "WHERE pies.id = %(pie_id)s;"
        )
        pie = connectToMySQL('pies_schema').query_db(query, data)
        # print(cls(pie[0]))
        # return pie
        return cls(pie[0])

    

    @classmethod
    def get_all_from_user(cls, data):
        query = (
            "SELECT * FROM pies "
            "JOIN users ON pies.creator_id = users.id "
            "WHERE pies.creator_id = %(creator_id)s;"
        )
        # query = "SELECT * FROM pies WHERE pies.creator_id = %(creator_id)s;"
        results =  connectToMySQL('pies_schema').query_db(query, data)
        pies = []
        for pie in results:
            print(pie)
            pies.append( cls(pie) )
        return pies

    @classmethod
    def get_all(cls):
        query = (
            "SELECT * FROM pies "
            "JOIN users ON pies.creator_id = users.id; "
        )
        results =  connectToMySQL('pies_schema').query_db(query)
        pies = []

        for pie in results:
            pies.append( cls(pie) )
        return pies

    @classmethod
    def get_pies_with_votes(cls):
        query = (
            "SELECT users.first_name AS creator, pies.name, pies.id, COUNT(pies.id) AS total_votes "
            "FROM users "
            "JOIN pies ON users.id = pies.creator_id "
            "LEFT JOIN votes ON pies.id = votes.pie_id "
            "GROUP BY pies.id "
            "ORDER BY total_votes DESC; "
        )
        results = connectToMySQL('pies_schema').query_db(query)
        return results

    @classmethod
    def check_vote(cls, data):
        query = "SELECT EXISTS(SELECT * FROM votes WHERE pie_id = %(pie_id)s AND user_id = %(user_id)s );"
        result = connectToMySQL('pies_schema').query_db(query, data)
        # final = result[0].values()
        # print(final)
        # print("-------------------------------------------------------------------------")
        for value in result[0].values():
            return value

    @classmethod
    def like(cls, data):
        query = (
            "INSERT INTO votes (user_id, pie_id) "
            "VALUES (%(user_id)s, %(pie_id)s) ;"
        )
        connectToMySQL('pies_schema').query_db(query, data)
    
    @classmethod
    def dislike(cls, data):
        query = (
            "DELETE FROM votes "
            "WHERE pie_id=%(pie_id)s "
            "AND user_id=%(user_id)s ;"
        )
        connectToMySQL('pies_schema').query_db(query, data)


    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['name']) < 3:
            flash("Name must be longer than 3 chars")
            is_valid = False
        if len(data['filling']) < 3:
            flash("Filling must be longer than 3 chars")
            is_valid = False
        if len(data['crust']) < 3:
            flash("Crust must be longer than 3 chars")
            is_valid = False
        return is_valid