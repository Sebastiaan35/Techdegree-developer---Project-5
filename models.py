#!/usr/bin/env python3
# from pymysql.err import IntegrityError
from datetime import datetime

from peewee import (
    Model,
    AutoField,
    TextField,
    IntegerField,
    DateTimeField,
    DateField,
    CharField,
    SqliteDatabase,
    IntegrityError)

from flask_bcrypt import generate_password_hash

from flask_login import UserMixin


# --- database part ---
db = SqliteDatabase('journal.db')

class Journal(UserMixin, Model):
    """Define product categories"""
    entry_id = AutoField()
    date_updated = DateTimeField()
    Title = CharField(max_length=255, unique=False)
    date  = DateField(unique=False)
    Time_Spent = IntegerField(default=0)
    What_You_Learned = TextField(unique=True)
    Resources_to_Remember = TextField()
    tags = CharField(max_length=255, unique=False)


    class Meta:
        """Configuration attributes"""
        database = db


    @classmethod
    def add_entry(cls, title, date, Time_Spent, learned, remember, tags):
        """Add an entry to database"""
        entry_dict = {}
        entry_dict['date_updated'] = datetime.strftime(datetime.now(),"%m.%d.%Y %H:%M:%S")
        entry_dict['Title'] = title
        entry_dict['date'] = date
        entry_dict['Time_Spent'] = Time_Spent
        entry_dict['What_You_Learned'] = learned
        entry_dict['Resources_to_Remember'] = remember
        entry_dict['tags'] = tags

        try:
            cls.create(**entry_dict)
            print(f"\nA new entry was added to the database:\n"
                  f"Title: {title} Date: {date} Time Spent: {Time_Spent} Learned: {learned} Remember: {remember} tags: {tags}\n")
        except IntegrityError:
            print("There was an IntegrityError")
            # entries = Journal.select().where(Journal.What_You_Learned == What_You_Learned.order_by(Journal.date_updated.desc())
            # en_ex = list(entries)[0].date_updated
            # print(f"The following entry was already added to the database at {en_ex}.\n"
            # f"Title: {title} | Date: {date} | Time Spent: {Time_Spent} | Learned: {learned} | Remember: {remember}")


def initialize():
    """Create the database if it doesn't exist"""
    db.connect()
    db.create_tables([Journal], safe=True)
    db.close()
