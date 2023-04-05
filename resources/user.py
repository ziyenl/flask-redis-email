import flask
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import or_
from passlib.hash import pbkdf2_sha256
from db import db
from models.user import UserModel
from schema import UserSchema, UserRegisterSchema
from flask import current_app
from util.task import send_registration_email


blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register")
class UserRegistration(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        """
        Register new user to the system
        :param user_data: user data consisting of name and password
        :return: str
        """
        if UserModel.query.filter(or_(UserModel.name == user_data['name'],
                                      UserModel.email == user_data['email'])).first():
            abort(409, "A usre with username or email already exist.")
        user = UserModel(name=user_data['name'],
                        password=pbkdf2_sha256.hash(user_data['password']),
                        email = user_data['email']) # hash the password
        db.session.add(user)
        db.session.commit()
        #current_app.queue.enqueue(send_registration_email, user.email, user.username)

        return {"message": "User successfully created."}, 201


@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    Get a  User, Deleting User for testing purposes.
    """
    @blp.response(200, UserSchema)
    def get(self, user_id):
        """
        Get a user
        :param user_id: user id
        :return: user
        """
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        """
        Delete a user
        :param user_id: user id
        :return: str
        """
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200