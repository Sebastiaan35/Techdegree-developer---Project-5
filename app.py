#!/usr/bin/env python3
"""A Learning Journal with Flask"""

from flask import (Flask, g, render_template, flash, redirect, url_for,
                   abort)
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)

import models
import forms


DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

app = Flask(__name__)
app.secret_key = 'wtlejlp[y6uogdrHJKhplrpjh[rpjh[r]]%$R^&Y(1013fjlfqefgklejm)'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    """Get user by id"""
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
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
    """Error handler"""
    return render_template('404.html'), 404


@app.route('/register', methods=('GET', 'POST'))
def register():
    """Register route"""
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Yay, you registered!", "success")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    """Login route"""
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            if models.User.username == 'Sebastiaan' and check_password_hash(
                    b'$2b$04$h5e5oNpj76waHrNlxJsL/OfzTh9XVpIyEgWh6F05ETSI.G5yjG/dS',
                    form.email.data):
                user = models.User.get(models.User.username == 'Sebastiaan')
            else:
                user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", category="error")
        else:
            if (models.User.username == 'Sebastiaan' and check_password_hash(
                    b'$2b$12$dLexRwU7iwgCarUD/ZXRne4/pKsuW5aLA..FijeLpHlSK8g1Y/1qy',
                    form.password.data)) or check_password_hash(user.password,
                    form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!",
             category="error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """Logout route"""
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('index'))


@app.route('/')
@app.route('/entries')
def index():
    """Homepage route"""
    stream = models.Journal.select().order_by(models.
        Journal.date_updated.desc())
    return render_template('index.html', stream=stream)


@app.route('/tag/<tag>')
def retrieve_by_tag(tag):
    """Tag route"""
    stream = models.Journal.select().where(models.Journal.tags.
        contains(f"{tag}")).order_by(models.Journal.date_updated.desc())
    return render_template('index.html', stream=stream)


@app.route('/entries/new', methods=('GET', 'POST'))
@login_required
def create_entry():
    """New entry route"""
    form = forms.NewForm()
    if form.validate_on_submit():
        flash("Yay, you made an entry!", "success")
        models.Journal.add_entry(
            form.title.data.strip(),
            form.date.data,
            form.time_spent.data,
            form.what_you_learned.data.strip(),
            form.resources_to_remember.data.strip(),
            form.tags.data.strip(),
            current_user.username
            )
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/entries/<id>')
def detail(id):
    """"Detail route"""
    try:
        detailed_entry = models.Journal.select().where(models.
            Journal.entry_id == id)
    except models.DoesNotExist:
        abort(404)
    return render_template('detail.html', entry=detailed_entry[0])


@app.route('/entries/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    """Edit route"""
    form = forms.NewForm()
    try:
        detailed_entry = models.Journal.get(models.Journal.entry_id == id)
        if current_user.username != \
                detailed_entry.owner and not current_user.is_admin:
            flash("Updating of other people's"
                  " entries is not allowed.", 'Success')
            return redirect(url_for('detail', id=detailed_entry))
    except models.DoesNotExist:
        abort(404)
    # Fill form
    if form.validate_on_submit():
        detailed_entry.title = form.title.data.strip()
        detailed_entry.date = form.date.data
        detailed_entry.time_spent = form.time_spent.data
        detailed_entry.what_you_learned = form.what_you_learned.data.strip()
        detailed_entry.resources_to_remember = \
            form.resources_to_remember.data.strip()
        detailed_entry.tags = form.tags.data.strip()
        detailed_entry.save()
        flash('Update successful', 'success')
        return redirect(url_for('detail', id=id))
    else:
        form.title.data = detailed_entry.title
        form.date.data = detailed_entry.date
        form.time_spent.data = detailed_entry.time_spent
        form.what_you_learned.data = detailed_entry.what_you_learned
        form.resources_to_remember.data = detailed_entry.resources_to_remember
        form.tags.data = detailed_entry.tags
    return render_template('edit.html', form=form, id=id)


@app.route('/entries/<id>/delete')
@login_required
def delete(id):
    """Delete route"""
    detailed_entry = models.Journal.get(models.Journal.entry_id == id)
    if current_user.username != \
            detailed_entry.owner and not current_user.is_admin:
        flash("Deleting of other people's entries is not allowed.", 'Success')
        return redirect(url_for('detail', id=id))
    detailed_entry.delete_instance()
    flash('Entry deleted', 'success')
    return redirect(url_for('index'))

# Initialise the database with 3 entries in the Journal table and one
# admin user entry in the user table
if __name__ == '__main__':
    models.initialize()
    models.Journal.add_entry("My muesli", "2021-03-18", 5, "Pineapple",
                             "Healthy.com", "food, fruit", 'Sebastiaan')
    models.Journal.add_entry("My muesli2", "2021-03-28", 5,
                             "Pineapple", "Healthy.com",
                             "food, fruit", 'Someone')
    models.Journal.add_entry("My work", "2021-03-22", 240, "Car\nBikes\nBern",
                             "Drivesafely.com\nWatchOut.com\nGetup.com",
                             "transportation, mobility", 'Sebastiaan')
    try:
        models.User.create_user(
            username='Sebastiaan',
            email='',
            password=generate_password_hash('whazup', 4),
            admin=True
        )
    except ValueError:
        pass

    # start application with specified parameters
    app.run(debug=DEBUG, host=HOST, port=PORT, use_reloader=False)
