from flask import flash, redirect, render_template, url_for
from flask_login import login_user, current_user, logout_user

from flaskblog import app, bcrypt, db
from flaskblog.forms import LoginForm, RegistrationForm
from flaskblog.models import Post, User

posts = [
    {
        'author': 'Someone',
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2019'
    },
    {
        'author': 'Someone 2',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2019'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='about')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        # Encrypt user password
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')

        # Create an user instance to pass all values to register
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        # Write user data in DB
        db.session.add(user)
        db.session.commit()

        flash(
            f'Your account has been created, now you\'re able to log in!',
            category='success'
        )
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash(f'Login unsucessful. Please check email and password',
                  category='danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
