from app.models import UserMixin
from app import db
from app.exceptions import *
import re
import datetime


class User(UserMixin, db.Model):
    @staticmethod
    def from_json(json):
        UserValidator.validate_username(json['userName'])
        UserValidator.validate_email(json['email'])
        UserValidator.validate_date(json['birthday'])
        UserValidator.validate_gender(json['gender'])
        UserValidator.validate_password(json['password'])
        UserValidator.is_exist(json['userName'], json['email'])
        return User(username=json['userName'], email=json['email'],
                    birthday=json['birthday'],
                    gender=json['gender'], password=json['password'],
                    telephone=json['phone'])

    def to_json(self):
        json_data = {
            "activated": self.Activated,
            "last_login": self.LastLogin,
            "login_state": False,  # TODO: Login state
            "subscriptions": "/user/subs",
            "username": self.UserName,
            "uuid": self.UUID
        }
        return json_data


class UserValidator:
    @staticmethod
    def validate_username(username):
        is_letters_and_numbers = re.compile("^[A-Za-z0-9]")
        for ch in username:
            if not is_letters_and_numbers.match(ch):
                raise ValidationError("Only allow letters and numbers in username")
        return True

    @staticmethod
    def validate_email(email):
        if not re.match("^[a-z0-9](\.?[a-z0-9_-]){0,}@[a-z0-9-]+\.([a-z]{1,6}\.)?[a-z]{2,6}$", email):
            raise ValidationError("Email address error")
        return True

    @staticmethod
    def validate_gender(gender):
        if not gender == "G" and not gender == "B":
            raise ValidationError("Gender error")
        return True

    @staticmethod
    def validate_date(date):
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValidationError("Date format error")
        return True

    @staticmethod
    def validate_password(password_text):
        if len(password_text) < 8:
            raise ValidationError("Password too short. At least 8 letters")
        return True

    @staticmethod
    def is_exist(username, email):
        if User.query.filter_by(UserName=username).first():
            raise ValidationError("User name exist. Register failed")
        if User.query.filter_by(Email=email).first():
            raise ValidationError("User email exist. Register failed")
        return True
