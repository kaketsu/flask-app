from datetime import datetime
from argus import db
from werkzeug.security import generate_password_hash, check_password_hash

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'data': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            # '_links': {
            #     'self': url_for(endpoint, page=page, per_page=per_page,
            #                     **kwargs),
            #     'next': url_for(endpoint, page=page + 1, per_page=per_page,
            #                     **kwargs) if resources.has_next else None,
            #     'prev': url_for(endpoint, page=page - 1, per_page=per_page,
            #                     **kwargs) if resources.has_prev else None
            # }
        }
        return data


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total



# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     password_hash = db.Column(db.String(128))
#     posts = db.relationship('Post', backref='author', lazy='dynamic')

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
    
#     def __repr__(self):
#         return '<User {}>'.format(self.username)    

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.Date, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __repr__(self):
#         return '<Post {}>'.format(self.body)

# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))


class Replay(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True, unique=True)
    limitUp = db.Column(db.Integer)
    limitDown = db.Column(db.Integer)
    marketFever = db.Column(db.Integer)
    summary = db.Column(db.String(120))

    def __init__(self, date=None, summary=None):
        self.date = date
        self.summary = summary

    def from_dict(self, data):
        for field in ['date', 'summary', 'limitUp', 'limitDown', 'marketFever']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'id': self.id,
            'date': self.date,
            'summary': self.summary,
            'limitUp': self.limitUp,
            'limitDown': self.limitDown,
            'marketFever': self.marketFever,
        }
        return data


    # def from_dict(self, data, new_user=False):
    #     for field in ['username', 'email', 'about_me']:
    #         if field in data:
    #             setattr(self, field, data[field])
    #     if new_user and 'password' in data:
    #         self.set_password(data['password']

    def __repr__(self):
        return '<Replay {}>'.format(self.date)    


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True, unique=True)
    stockName = db.Column(db.String(60))
    stockProce = db.Column(db.Float)
    remark = db.Column(db.String(140))

    def __init__(self, date=None, stockName=None, stockPrice=None, remark=None):
        self.date = date
        self.stockName = stockName
        self.stockProce = stockPrice
        self.remark = remark

    def from_dict(self, data):
        for field in ['date', 'stockName', 'stockPrice', 'remark']:
            if field in data:
                setattr(self, field, data[field])

class Sector(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sectorName = db.Column(db.String(60), index=True, unique=True)
    stocks = db.Column(db.String(240))
    description = db.Column(db.String(240))

    def __init__(self,sectorName=None, stocks=None, description=None):
        self.sectorName = sectorName
        self.stocks = stocks
        self.description = description

    def from_dict(self, data):
        for field in ['sectorName', 'stocks', 'description']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'id': self.id,
            'sectorName': self.sectorName,
            'stocks': self.stocks,
            'description': self.description,
        }
        return data


class ReplaySectorFever(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)
    sectorId = db.Column(db.Integer)
    sectorName = db.Column(db.String(60))
    fever = db.Column(db.Integer)
    remark = db.Column(db.String(140))

    def __init__(self,date=None, sectorId=None, sectorName=None, fever=None, remark=None):
        self.date = date
        self.sectorId = sectorId
        self.sectorName = sectorName
        self.fever = fever
        self.remark = remark

    def from_dict(self, data):
        for field in ['date', 'sectorId', 'sectorName', 'fever', 'remark']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'id': self.id,
            'date': self.date,
            'sectorId': self.sectorId,
            'sectorName': self.sectorName,
            'fever': self.fever,
            'remark': self.remark,
        }
        return data

class Predict(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)
    sectorId = db.Column(db.Integer)
    sectorName = db.Column(db.String(60))
    fever = db.Column(db.Integer)
    remark = db.Column(db.String(140))


class StockRecall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    createDate = db.Column(db.Date, index=True)
    stockName = db.Column(db.Integer)
    stockPrice = db.Column(db.String(60))
    remark = db.Column(db.String(140))
    recallDate = db.Column(db.String(200))

class SelectModel(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelName = db.Column(db.String(60))
    modelDescription = db.Column(db.String(1200))
    createTime = db.Column(db.DateTime, default=datetime.utcnow)
    updateTime = db.Column(db.DateTime, default=datetime.utcnow)

    def from_dict(self, data):
        for field in ['modelName', 'modelDescription']:
            if field in data:
                setattr(self, field, data[field])
    
    def to_dict(self):
        data = {
            'id': self.id,
            'modelName': self.modelName,
            'modelDescription': self.modelDescription,
            'createTime': self.createTime,
            'updateTime': self.updateTime,
        }
        return data
