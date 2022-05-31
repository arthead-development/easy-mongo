# easy-mongo
Easy to use package for MongoDB access in Python

This is a work in progress. 

The idea is to create a Python Package that will let users access a MongoDB database and perform the most common tasks as easy and simple as possible.

## The Concept
The concept is easy. The user of this package will need to create a class per colloection. This class needs to inherit a base class from this package called Document. he only thing the class needs to define is a class variable stating the name of the collection.

Before use, an init_db function must be called that will set up the database connection. 

The basic usecase is like this:

    from easy_mongo import Ducument, db, init_db


    class User(Document):
        collection = db.user
    
    
    init_db('mongodb://username:password@host:port')

    user = User(
        {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@email.com'
        })
    
    user.save()

    user = User.find(first_name='Alice').first_or_none()
    if user:
        user.first_name = 'Bob'
        user.save()
    
