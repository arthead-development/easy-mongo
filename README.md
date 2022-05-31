# easy-mongo
Easy to use package for MongoDB access in Python

This is a work in progress. 

The idea is to create a Python Package that will let users access a MongoDB database and perform the most common tasks as easy and simple as possible.

## The Concept
The concept is easy. The user of this package will need to create a class per collection. The collection class is created by a call to the create_collection_class function.
Before use, an init_db function must be called that will set up the database connection. 

The basic use case is like this:
```python
from easy_mongo import init_db, create_collection_class


init_db('mongodb://username:password@host:port')

# Create a user class
User = create_collection_class('User', 'users')

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
```    
