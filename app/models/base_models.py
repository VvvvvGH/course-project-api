import uuid
import hashlib
from datetime import datetime
from app import db


class Administrator(db.Model):
    __tablename__ = 'administrator'
    UUID = db.Column(db.String(40), primary_key=True)
    UserName = db.Column(db.String(40), nullable=False, unique=True)
    Password = db.Column(db.String(32), nullable=False)
    LoginState = db.Column(db.Boolean, default=0)
    RegistrationDate = db.Column(db.DateTime, nullable=False)
    LastLoginDate = db.Column(db.DateTime, nullable=False)
    Authorization = db.Column(db.INT, nullable=False)


class UserMixin(db.Model):
    __tablename__ = 'users'
    UUID = db.Column(db.String(40), primary_key=True)
    UserName = db.Column(db.String(40), nullable=False, unique=True)
    Password = db.Column(db.String(32), nullable=False)
    Gender = db.Column(db.String(2), nullable=False)
    Birthday = db.Column(db.Date, nullable=False)
    Email = db.Column(db.String(20), nullable=False, unique=True)
    TelePhone = db.Column(db.String(18), nullable=False)

    UserBackground = db.relationship('UserBackground')
    UserSearchRecord = db.relationship('UserSearchRecord', lazy=True)
    UserFollow = db.relationship('UserFollow', lazy=True)

    def __init__(self, username, password, gender, birthday, email, telephone):
        self.UserName = username
        self.UUID = uuid.uuid1()
        self.Password = hashlib.md5(password.encode('utf-8')).hexdigest()
        self.Gender = gender
        self.Birthday = birthday
        self.Email = email
        self.TelePhone = telephone
        self.UserBackground.append(UserBackground(self.UUID))

    def __repr__(self):
        return '<User %s>' % self.UserName


class UserBackground(db.Model):
    __tablename__ = 'userbackground'
    # 一对一关系
    UUID = db.Column(db.String(40), db.ForeignKey('users.UUID'), primary_key=True)
    LoginState = db.Column(db.Boolean, default=False, nullable=False)
    Activated = db.Column(db.Boolean, default=False, nullable=False)
    RegDate = db.Column(db.DateTime, nullable=False)
    LastLoginDate = db.Column(db.DateTime, nullable=False)

    def __init__(self, UUID):
        self.UUID = UUID,
        self.RegDate = datetime.now()
        self.LastLoginDate = datetime.now()

    def __repr__(self):
        return '<User %s>' % self.UUID


# Helper table 中间表

class UserFollow(db.Model):
    __tablename__ = 'userfollow'
    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    UUID = db.Column(db.String(40), db.ForeignKey('users.UUID'), nullable=False)
    ProjID = db.Column(db.String(100), db.ForeignKey('projectfollow.ProjID'), nullable=False)
    Time = db.Column(db.DateTime, nullable=False)

    def __init__(self, UUID, ProjID):
        self.UUID = UUID,
        self.ProjID = ProjID
        self.Time = datetime.now()

    def __repr__(self):
        return '<User %s>' % self.ProjID


class ProjectFollow(db.Model):
    __tablename__ = 'projectfollow'
    ProjID = db.Column(db.String(100), db.ForeignKey('procurementnotices.ProjID'), primary_key=True, nullable=False)
    Title = db.Column(db.String(100))

    def __init__(self, project_id, title):
        self.ProjID = project_id
        self.Title = title

    def __repr__(self):
        return '<Project %s>' % self.ProjID


class UserSearchRecord(db.Model):
    __tablename__ = 'usersearchrecord'
    # 一对多关系
    RecordID = db.Column(db.Integer, primary_key=True, nullable=False)
    UUID = db.Column(db.String(40), db.ForeignKey('users.UUID'))
    SearchRecord = db.Column(db.String(120))
    Time = db.Column(db.DateTime)

    def __init__(self, UUID, search_record):
        self.UUID = UUID
        self.SearchRecord = search_record
        self.Time = datetime.now()

    def __repr__(self):
        return '<User %s>' % self.UUID


class Bidders(db.Model):
    __tablename__ = 'bidders'
    ProjID = db.Column(db.String(100), db.ForeignKey('procurementnotices.ProjID'), primary_key=True, nullable=False)
    Biders = db.Column(db.String(25))
    FinalPrice = db.Column(db.String(10))
    IsQualified = db.Column(db.String(5))
    TechnicalScore = db.Column(db.String(5))
    BusinessScore = db.Column(db.String(5))
    PriceScore = db.Column(db.String(5))
    TotalScore = db.Column(db.String(5))
    Rank = db.Column(db.String(5))

    def __repr__(self):
        return '<Project %s>' % self.ProjID


class BidNotice(db.Model):
    __tablename__ = 'bidnotice'
    ProjID = db.Column(db.String(100), db.ForeignKey('procurementnotices.ProjID'), primary_key=True, nullable=False)
    ProjTitle = db.Column(db.String(100))
    ProjBud = db.Column(db.String(10))
    PurMethod = db.Column(db.String(10))
    City = db.Column(db.String(10))
    SBs = db.Column(db.String(40))
    QuoteDetail = db.Column(db.String(150))
    ServiceReq = db.Column(db.String(50))
    Quantity = db.Column(db.String(5))
    Currency = db.Column(db.String(5))
    UnitPrice = db.Column(db.String(10))
    FinalPrice = db.Column(db.String(10))
    ReviewDate = db.Column(db.DateTime)
    ReviewAddr = db.Column(db.String(40))
    Attachment = db.Column(db.String(50))
    ReviewCommittee = db.Column(db.String(30))
    Manager = db.Column(db.String(25))
    ReviewComment = db.Column(db.String(250))
    AnnounceDDL = db.Column(db.DateTime)
    ReleaseDate = db.Column(db.DateTime)

    def __repr__(self):
        return '<Project %s>' % self.ProjID


class CorrectedNotice(db.Model):
    __tablename__ = 'correctionnotice'
    ProjID = db.Column(db.String(100), db.ForeignKey('procurementnotices.ProjID'), primary_key=True, nullable=False)
    Content = db.Column(db.String(1000))
    City = db.Column(db.String(10))
    ReleaseDate = db.Column(db.DateTime)

    def __repr__(self):
        return '<Project %s>' % self.ProjID


class PurchaseNotice(db.Model):
    __tablename__ = 'procurementnotices'
    ProjID = db.Column(db.String(100), primary_key=True, nullable=False)
    ProjTitle = db.Column(db.String(100))
    City = db.Column(db.String(10))
    ProjBud = db.Column(db.String(50))
    PurQuantity = db.Column(db.String(50))
    ProjReq = db.Column(db.String(1800))
    SupplierQuals = db.Column(db.String(200))
    DDL = db.Column(db.DateTime)
    AnnunceDDL = db.Column(db.DateTime)
    BidStartTime = db.Column(db.DateTime)
    PubDate = db.Column(db.DateTime)
    Addr = db.Column(db.String(200))
    BidStartAddr = db.Column(db.String(200))
    BidBond = db.Column(db.String(200))
    Publisher = db.Column(db.String(200))
    Attachment = db.Column(db.String(200))
    ReleaseDate = db.Column(db.DateTime)

    def __repr__(self):
        return '<Project %s>' % self.ProjID


class Purchaser(db.Model):
    __tablename__ = 'purchasers'

    ProjID = db.Column(db.String(100), db.ForeignKey('procurementnotices.ProjID'), primary_key=True, nullable=False)
    Purchaser = db.Column(db.String(50))
    Contacts = db.Column(db.String(50))
    ProjContacts = db.Column(db.String(10))
    ProjTel = db.Column(db.String(20))
    Fax = db.Column(db.String(20))
    ZipCode = db.Column(db.String(15))

    def __repr__(self):
        return '<Project %s>' % self.ProjID


class PurchaseAgent(db.Model):
    __tablename__ = 'purchasingagents'
    ProjID = db.Column(db.String(100), db.ForeignKey('procurementnotices.ProjID'), primary_key=True, nullable=False)
    Agency = db.Column(db.String(50))
    AgencyAddr = db.Column(db.String(50))
    Contacts = db.Column(db.String(50))
    ProjContacts = db.Column(db.String(10))
    ContactsPhone = db.Column(db.String(20))
    Fax = db.Column(db.String(20))
    ZipCode = db.Column(db.String(15))

    def __repr__(self):
        return '<Project %s>' % self.ProjID


class CrawerURL(db.Model):
    __tablename__ = 'crawlerurl'
    URL = db.Column(db.String(100), primary_key=True)
    City = db.Column(db.String(10))
    Type = db.Column(db.String(20))
    UpdatedColumnNum = db.Column(db.INT)
    Success = db.Column(db.Boolean)
    Time = db.Column(db.DateTime)
    ErrorRecord = db.Column(db.String(200))

    def __repr__(self):
        return '<Project %s>' % self.URL
