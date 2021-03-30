#!/usr/bin/env python3
"""The database part"""

from datetime import datetime
from peewee import (
    Model,
    AutoField,
    TextField,
    IntegerField,
    DateTimeField,
    CharField,
    SqliteDatabase,
    IntegrityError,
    BooleanField)
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin


db = SqliteDatabase('journal.db')

class User(UserMixin, Model):
    """Table for user info"""
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        """Configuration attributes"""
        database = db
        order_by = ('-joined_at',)

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        """Create user"""
        try:
            #transaction is to prevent a user from being half created.
            #Tries it out and if it doesn't work undoes everything
            with db.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")


class Journal(UserMixin, Model):
    """Define product categories"""
    entry_id = AutoField()
    date_updated = DateTimeField()
    title = CharField(max_length=255, unique=True)
    date  = CharField(max_length=55, unique=False)
    time_spent = IntegerField(default=0)
    what_you_learned = TextField(unique=False)
    resources_to_remember = TextField()
    tags = CharField(max_length=255, unique=False)
    owner = CharField(max_length=255, unique=False)

    class Meta:
        """Configuration attributes"""
        database = db

    @classmethod
    def add_entry(cls, title, date, time_spent, learned, remember, tags, owner):
        """Add an entry to database"""
        entry_dict = {}
        entry_dict['date_updated'] = datetime.strftime(datetime.now(),
        "%m.%d.%Y %H:%M:%S")
        entry_dict['title'] = title
        entry_dict['date'] = date
        entry_dict['time_spent'] = time_spent
        entry_dict['what_you_learned'] = learned
        entry_dict['resources_to_remember'] = remember
        entry_dict['tags'] = tags
        entry_dict['owner'] = owner
        try:
            cls.create(**entry_dict)
            print(f"\nA new entry was added to the database:\n"
                  f"title: {title} Date: {date} Time Spent: {time_spent}"
                  " Learned: {learned} Remember: {remember} tags: {tags}\n")
        except IntegrityError:
            pass


def initialize():
    """Create the database if it doesn't exist"""
    db.connect()
    db.create_tables([User, Journal], safe=True)
    db.close()
