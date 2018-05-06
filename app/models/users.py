import re
import datetime
from app.models.base_models import *
from app.exceptions import *
from app import db
from app import mail
from app import login_manager
from flask_mail import Message
from flask_login import UserMixin as UserMixinLogin
from flask import current_app as app


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


class User(UserMixin, UserMixinLogin, db.Model):

    @staticmethod
    def get(user_id):
        # 　It should return None (not raise an exception) if the ID is not valid.
        # 　(In that case, the ID will manually be removed from the session and processing will continue.)
        user = User.query.filter_by(UUID=user_id).first()
        if user:
            return user
        else:
            return None

    def get_id(self):
        return self.UUID.encode("utf-8")

    def is_active(self):
        user = UserBackground.query.filter_by(UUID=self.UUID).first()
        if user.Activated:
            return True
        else:
            return False

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

    @staticmethod
    def reset_password(email, username):
        UserValidator.validate_email(email)
        UserValidator.validate_username(username)
        user = User.query.filter_by(UserName=username, Email=email).first()
        if user:
            msg = Message("Hello",
                          sender="os_project_api@yeah.net",
                          recipients=['%s' % email])
            msg.body = "你好 %s，跨越长城，走向世界。" % username
            mail.send(msg)
            data = {
                'message': '验证成功，密码重置链接已经发送到邮箱。如果收不到邮件，请在垃圾箱中查找。'
            }
        else:
            data = {
                'message': '验证失败，用户信息验证失败'
            }
        return data

    def add_search_record(self, search_record):
        time = datetime.now()
        self.UserSearchRecord.append(UserSearchRecord(UUID=self.UUID, search_record=search_record))
        try:
            db.session.commit()
        except:
            app.logger.error("")
            db.session.rollback()

    def add_follow_project(self, project_id):
        # 当项目存在时才需要在订阅列表内添加项目
        notice = PurchaseNotice.query.filter_by(ProjID=project_id).first()
        # 项目存在，而且不在关注列表内 将项目添加到关注列表
        if notice and \
                not ProjectFollow.query.filter_by(ProjID=project_id).first():
            project_follow = ProjectFollow(project_id=project_id, title=notice.ProjTitle)
            try:
                db.session.add(project_follow)
                db.session.commit()
            except Exception as e:
                app.logger.error("Insert follow project error" + str(e))
                db.session.rollback()
        # 项目不存在，而且不在关注列表内　错误
        elif not notice:
            app.logger.error("The project does not exists")
        # 添加项目关注
        elif notice:
            user_follow = UserFollow(UUID=self.UUID, ProjID=project_id)
            try:
                self.UserFollow.append(user_follow)
                db.session.commit()
            except Exception as e:
                app.logger.error("Insert user follow project error" + str(e))
                db.session.rollback()

    def del_follow_project(self, project_id):
        project_follow = ProjectFollow.query.filter_by(ProjID=project_id).all()
        # 若项目只被一个用户关注，直接在项目关注列表内删除
        if len(project_follow) == 1:
            try:
                db.session.delete(project_follow[0])
            except Exception as e:
                app.logger.error("Delete project in project follow  failed" + str(e))
                db.session.rollback()
        # 在用户关注列表内移除该项目
        user_follow = UserFollow.query.filter_by(ProjID=project_id, UUID=self.UUID).first()
        if user_follow:
            try:
                db.session.delete(user_follow)
            except Exception as e:
                app.logger.error("Delete project in user follow failed" + str(e))
                db.session.rollback()

    def get_follow_list(self, items_per_page, current_page):
        follow_list = UserFollow.query.filter_by(UUID=self.UUID).all()
        page_count = len(follow_list) // items_per_page
        # 分页
        follow_list = follow_list[items_per_page * (current_page - 1):items_per_page * (current_page)]
        project_info_list = []

        for project in follow_list:
            project_info = PurchaseNotice.query.filter_by(ProjID=project.ProjID).first()
            project_types = self.check_project_types(project_info.ProjID)
            project_info_list.append({
                "ProjID": project_info.ProjID,
                "ProjTitle": project_info.ProjTitle,
                "City": project_info.City,
                "PubDate": project_info.PubDate,
                "DDL": project_info.DDL,
                "Type": project_types,
            })
        return page_count, current_page, items_per_page, project_info_list

    def check_project_types(self, project_id):
        project_types = [PurchaseNotice, CorrectedNotice, BidNotice]
        types = []
        for ptype in project_types:
            if ptype.query.filter_by(ProjID=project_id).first():
                types.append(ptype.__tablename__)
        return types


"""
class UserFollowOp(UserFollow):
    @staticmethod
    def add_follow(project_id):
        project = PurchaseNotice.query.filter_by(ProjID=project_id).first_or_404()
        # TODO: Get current user
        # new_follow = UserFollow(project_id=project_id,uuid=)

    @staticmethod
    def del_follow(project_id):
        project = PurchaseNotice.query.filter_by(ProjID=project_id).first_or_404()
        # TODO: Get current user
"""


class UserValidator:
    @staticmethod
    def validate_username(username):
        is_letters_and_numbers = re.compile("^[A-Za-z0-9]")
        for ch in username:
            if not is_letters_and_numbers.match(ch):
                raise ValidationError("用户名仅允许数字和字母")
        return True

    @staticmethod
    def validate_email(email):
        if not re.match("^[a-z0-9](\.?[a-z0-9_-]){0,}@[a-z0-9-]+\.([a-z]{1,6}\.)?[a-z]{2,6}$", email):
            raise ValidationError("邮件地址错误")
        return True

    @staticmethod
    def validate_gender(gender):
        if not gender == "G" and not gender == "B":
            raise ValidationError("请选择性别")
        return True

    @staticmethod
    def validate_date(date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValidationError("日期格式错误")
        return True

    @staticmethod
    def validate_password(password_text):
        if len(password_text) < 8:
            raise ValidationError("密码太短，至少八位")
        return True

    @staticmethod
    def is_exist(username, email):
        if User.query.filter_by(UserName=username).first():
            raise ValidationError("用户名已存在，注册失败")
        if User.query.filter_by(Email=email).first():
            raise ValidationError("用户邮箱已存在，注册失败")
        return True
