#!/usr/bin/env python3
# import models

from datetime import date, datetime

from peewee import (
    Model,
    AutoField,
    TextField,
    IntegerField,
    DateTimeField,
    CharField,
    SqliteDatabase)


# --- database part ---
db = SqliteDatabase('journal.db')

class Journal(Model):
    """Define product categories"""
    entry_id = AutoField()
    date_updated = DateTimeField()
    Title = CharField(max_length=255, unique=False)
    date  = DateTimeField()
    Time_Spent = IntegerField(default=0)
    What_You_Learned = TextField()
    Resources_to_Remember = TextField()
    tags =  CharField(max_length=255, unique=False)


    class Meta:
        """Configuration attributes"""
        database = db


def initialize():
    """Create the database if it doesn't exist"""
    db.connect()
    db.create_tables([Journal], safe=True)

def add_entry(title, learned, remember, tags):
    """Add an entry to database"""
    entry_dict = {}
    entry_dict['date_updated'] = datetime.strftime(datetime.now(),"%m.%d.%Y %H:%M:%S")
    entry_dict['Title'] = title
    entry_dict['What_You_Learned'] = learned
    entry_dict['Resources_to_Remember'] = remember
    entry_dict['date'] = str(datetime.strftime(date.today(),"%m.%d.%Y"))
    entry_dict['tags'] = tags

    en_ex = entry_exists(learned)

    if not en_ex:
        ##product does not exist
        Journal.create(**entry_dict)
        print(f"\nA new entry was added to the database:\n"
              f"Title: {title} Learned: {learned} Remember: {remember}\n")
    else:
        ##product is newer or has same date_updated
        print(f"The following entry was already added to the database at {entry_exists(learned)}.\n"
        f"Title: {title} | Learned: {learned} | Remember: {remember}")
        # if entry_dict['date_updated'] >= en_ex:
        #     delete_entry(stringy)
        #     Journal.create(**entry_dict)
        #     print(f"\nAn entry was replaced in the database:\n"
        #           f"{stringy}\n")

def delete_entry(What_You_Learned):
    """Delete product from database"""
    entry = Journal.get(Journal.What_You_Learned == What_You_Learned)
    entry.delete_instance()


def entry_exists(What_You_Learned):
    """Check if entry already in database"""
    #Returns none if not in database; Returns date last updated if it is as datetime
    entries = Journal.select().order_by(Journal.date_updated.desc())
    entries = entries.where(Journal.What_You_Learned == What_You_Learned)

    if len(entries) > 0:
        return list(entries)[0].date_updated
    else:
        return None


def view_entries():
    entries = Journal.select().order_by(Journal.date_updated.desc())
    print("\nThe following entries are currently in the database:\n")
    for entry in entries:
        print(f"{entry.date_updated}: {entry.What_You_Learned} | Tags: {entry.tags}")


def retrieve_by_tag(tagy):
    # entries = Journal.select().order_by(Journal.tags)
    #Does not work either
    # entries = entries.where(tagy in Journal.tags)
    # Does not work:
    entries = Journal.select().where(Journal.tags.in_([tagy]))

    print(f"\nThe following entries have the tag '{tagy}':\n")
    for entry in entries:
        # listy = entry.tags.split(', ')
        # if tagy in listy:
        #     print(f"{entry.date_updated} - {entry.What_You_Learned} - {entry.tags}")
        print(f"{entry.date_updated} - {entry.What_You_Learned} - {entry.tags}")
# --- database part --- END ---


#Route
DEBUG = True
PORT = 8000
HOST = '127.0.0.1'


# # / - Known as the root page, homepage, landing page but will act as the Listing route.
# @app.route('/')
#
# # /entries - Also will act as the Listing route just like /
# @app.route('/entries')
#
# # /entries/new - The Create route
# @app.route('/entries/new')
#
# # /entries/<id> - The Detail route
# @app.route('/entries/<id>')
#
# # /entries/<id>/edit - The Edit or Update route
# @app.route('/entries/<id>/edit')
#
# # /entries/<id>/delete - Delete route
# @app.route('/entries/<id>/delete')


if __name__ == '__main__':
    initialize()
    add_entry("My muesli", "Pineapple", "Healthy", "food, fruit")
    add_entry("Breakfast", "Sausage", "soso", "food, fruit")
    add_entry("My work", "Car", "Drive safely", "transportation, mobility")
    print(55*"*")
    view_entries()
    print(55*"*")
    retrieve_by_tag("transportation")
