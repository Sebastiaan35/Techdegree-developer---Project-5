#!/usr/bin/env python3
import models
import forms

from flask import (Flask, g, render_template, flash, redirect, url_for,
                  abort)

from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                             login_required, current_user)

DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

app = Flask(__name__)
app.secret_key = 'wtlejlp[y6uogdrHJKphplrpjh[rpjh[r]]]%$R^&Y(1013r9fjlfqefgklejm)'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(entryid):
    try:
        return Journal.get(Journal.entry_id == entryid)
    except DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.db
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# / - Known as the root page, homepage, landing page but will act as the Listing route.
# /entries - Also will act as the Listing route just like /
@app.route('/')
@app.route('/entries')
def index():
    stream = models.Journal.select().order_by(models.Journal.date_updated.desc())
    return render_template('index.html', stream=stream)


@app.route('/tag/<tag>')
def Retrieve_By_Tag(tag=None):
    stream = models.Journal.select().where(models.Journal.tags.contains(f"{tag}"))
    return render_template('index.html', stream=stream)


# /entries/new - The Create route
# @app.route('/new', methods=('GET', 'POST'))
@app.route('/entries/new', methods=('GET', 'POST'))
def Create_Entry():
    form = forms.neform()
    if form.validate_on_submit():
        flash("Yay, you made an entry!", "success")
        #
        models.Journal.add_entry(
        form.Title.data.strip(),
        form.date.data,
        form.Time_Spent.data,
        form.What_You_Learned.data.strip(),
        form.Resources_to_Remember.data.strip(),
        form.tags.data.strip(),
    )
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


# /entries/<id> - The Detail route
@app.route('/entries/<id>')
def detail(id=None):
    try:
        Detailed_Entry = models.Journal.select().where(models.Journal.entry_id == id)
    except models.DoesNotExist:
        abort(404)
    return render_template('detail.html', entry=Detailed_Entry[0])


# /entries/<id>/edit - The Edit or Update route
@app.route('/entries/<int:id>/edit', methods=('GET', 'POST'))
def edit(id=None):
    form = forms.neform()
    try:
        Detailed_Entry = models.Journal.select().where(models.Journal.entry_id == id)[0]
    except models.DoesNotExist:
        abort(404)
    # Fill form
    if form.validate_on_submit():
        # models.Journal.add_entry(
        Detailed_Entry.Title = form.Title.data.strip()
        Detailed_Entry.date = form.date.data
        Detailed_Entry.Time_Spent = form.Time_Spent.data
        Detailed_Entry.What_You_Learned = form.What_You_Learned.data.strip()
        Detailed_Entry.Resources_to_Remember = form.Resources_to_Remember.data.strip()
        Detailed_Entry.tags = form.tags.data.strip()
        Detailed_Entry.save()
        flash('Update successful', 'success')
        # Return to detail page
        return redirect(url_for('detail', id=id))
    else:
        form.Title.data = Detailed_Entry.Title
        form.date.data = Detailed_Entry.date
        form.Time_Spent.data = Detailed_Entry.Time_Spent
        form.What_You_Learned.data = Detailed_Entry.What_You_Learned
        form.Resources_to_Remember.data = Detailed_Entry.Resources_to_Remember
        form.tags.data = Detailed_Entry.tags
    return render_template('edit.html', form=form, id=id)


# /entries/<id>/delete - Delete route
@app.route('/entries/<id>/delete')
def delete(id=None):
    Detailed_Entry = models.Journal.get(models.Journal.entry_id == id)
    Detailed_Entry.delete_instance()
    # Detailed_Entry.save()
    flash('Entry deleted', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    models.initialize()
    models.Journal.add_entry("My muesli", "2021-03-18", 5, "Pineapple", "Healthy", "food, fruit")
    models.Journal.add_entry("My work", "2021-03-22", 240, "Car\nBikes\nBern", "Drive safely\nWatch Out\nGet up in time", "transportation, mobility")
    app.run(threaded=True, port=5000)
