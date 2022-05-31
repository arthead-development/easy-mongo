from copy import copy
import bson
from pymongo import MongoClient


db = None


class DatabaseInitError(Exception):
    pass


class DatabaseCollectionError(Exception):
    pass


def create_collection_class(class_name, collection_name=None):
    if collection_name is None:
        collection_name = class_name
    if db is None:
        raise DatabaseInitError('init_db function must be called before creation of collection classes')
    collection_class = type(class_name, (Document, ), {
        'collection': db[collection_name]
    })
    return collection_class


def init_db(connection_str, database):
    client = MongoClient(connection_str)
    global db
    db = client[database]


class ResultList(list):
    def first_or_none(self):
        return self[0] if len(self) > 0 else None

    def last_or_none(self):
        return self[-1] if len(self) > 0 else None


class Document(dict):
    collection = None

    def __init__(self, data):
        super().__init__()
        if '_id' not in data:
            self._id = None
        d = copy(data)
        for k, v in data.items():
            if isinstance(v, Document):
                d[k] = v.__dict__
        self.__dict__.update(d)

    def __repr__(self):
        return '\n'.join(f'{k} = {v}' for k, v in self.__dict__.items())

    def save(self):
        if not self._id:
            del (self.__dict__['_id'])
            print('*' * 80, '\n', self.collection.database, '\n', '*' * 80, flush=True)
            return self.collection.insert_one(self.__dict__)
        else:
            return self.collection.replace_one({'_id': self._id}, self.__dict__)

    def delete_field(self, field):
        self.collection.update_one({'_id': self._id}, {"$unset": {field: ""}})

    @classmethod
    def get_by_id(cls, _id):
        try:
            return cls(cls.collection.find_one({'_id': bson.ObjectId(_id)}))
        except bson.errors.InvalidId:
            raise DatabaseCollectionError(f'No document with _id {_id} found')

    @classmethod
    def insert_many(cls, items):
        for item in items:
            cls(item).save()

    @classmethod
    def all(cls):
        return [cls(item) for item in cls.collection.find({})]

    @classmethod
    def find(cls, **kwargs):
        return ResultList(cls(item) for item in cls.collection.find(kwargs))

    @classmethod
    def delete(cls, **kwargs):
        cls.collection.delete_many(kwargs)

    @classmethod
    def count(cls):
        return cls.collection.count
