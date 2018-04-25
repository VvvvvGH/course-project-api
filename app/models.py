from app import db
import uuid
import hashlib
from datetime import datetime
from app.exceptions import *


class UserMixin(db.Model):
    __tablename__ = 'users'
    UUID = db.Column(db.String(40), primary_key=True)
    UserName = db.Column(db.String(40), nullable=False, unique=True)
    Password = db.Column(db.String(32), nullable=False)
    Gender = db.Column(db.String(2), nullable=False)
    Birthday = db.Column(db.Date, nullable=False)
    Email = db.Column(db.String(20), nullable=False, unique=True)
    TelePhone = db.Column(db.String(18), nullable=False)
    Activated = db.Column(db.BOOLEAN, nullable=False)
    RegDate = db.Column(db.Date, nullable=False)
    LastLogin = db.Column(db.Date)

    def __init__(self, username, password, gender, birthday, email, telephone):
        self.UserName = username
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        self.Password = md5.hexdigest()
        self.Gender = gender
        self.Birthday = birthday
        self.Email = email
        self.TelePhone = telephone
        self.Activated = False
        self.RegDate = datetime.now().strftime('%Y-%m-%d')
        self.UUID = uuid.uuid1()

    def __repr__(self):
        return '<User %s>' % self.UserName


class UserFocus(db.Model):
    __tablename__ = 'user_focusproject'
    UUID = db.Column(db.String(40), primary_key=True, nullable=False)
    ProjID = db.Column(db.String(200), nullable=False)

    def __init__(self, uuid, project_id):
        self.UUID = uuid
        self.ProjID = project_id

    def __repr__(self):
        return '<Project %s>' % self.ProjID


class Bidders(db.Model):
    __tablename__ = 'bidders'
    ProjID = db.Column(db.String(100), primary_key=True, nullable=False)
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
    ProjID = db.Column(db.String(100), primary_key=True, nullable=False)
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
    ReviewDate = db.Column(db.Date)
    ReviewAddr = db.Column(db.String(40))
    Attachment = db.Column(db.String(50))
    ReviewCommittee = db.Column(db.String(30))
    Manager = db.Column(db.String(25))
    ReviewComment = db.Column(db.String(250))
    AnnounceDDL = db.Column(db.Date)

    def __repr__(self):
        return '<Project %s>' % self.ProjID


class CorrectedNotice(db.Model):
    __tablename__ = 'correctionnotice'
    ProjID = db.Column(db.String(100), primary_key=True, nullable=False)
    Content = db.Column(db.String(1000))
    City = db.Column(db.String(10))

    def __repr__(self):
        return '<Project %s>' % self.ProjID


class ProjectFollow(db.Model):
    __tablename__ = 'focusproject'
    ProjID = db.Column(db.String(100), primary_key=True, nullable=False)
    Title = db.Column(db.String(100))
    Time = db.Column(db.Date)

    def __repr__(self):
        return '<Project %s>' % self.ProjID


class PurchaseNotice(db.Model):
    __tablename__ = 'procurementnotices'
    ProjID = db.Column(db.String(100), primary_key=True, nullable=False)
    ProjTitle = db.Column(db.String(100))
    City = db.Column(db.String(10))
    ProjBud = db.Column(db.String(10))
    PurQuantity = db.Column(db.String(5))
    ProjReqURL = db.Column(db.String(50))
    SupplierQuals = db.Column(db.String(50))
    DDL = db.Column(db.Date)
    AnnunceDDL = db.Column(db.Date)
    BidStartTime = db.Column(db.Date)
    PubDate = db.Column(db.Date)
    Addr = db.Column(db.String(40))
    BidStartAddr = db.Column(db.String(40))
    BidBond = db.Column(db.String(10))
    Publisher = db.Column(db.String(40))
    Attachment = db.Column(db.String(50))

    def __repr__(self):
        return '<Project %s>' % self.ProjID


class Purchaser(db.Model):
    __tablename__ = 'purchasers'

    ProjID = db.Column(db.String(100), primary_key=True, nullable=False)
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
    ProjID = db.Column(db.String(100), primary_key=True, nullable=False)
    Agency = db.Column(db.String(50))
    AgencyAddr = db.Column(db.String(50))
    Contacts = db.Column(db.String(50))
    ProjContacts = db.Column(db.String(10))
    ContactsPhone = db.Column(db.String(20))
    Fax = db.Column(db.String(20))
    ZipCode = db.Column(db.String(15))

    def __repr__(self):
        return '<Project %s>' % self.ProjID
