from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect

from model import db, User
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

app.config['SECRET_KEY'] = b'ea959bc6bbd140100d66503aa6ac1242c6eb0e8d4c38b85c7ea9a9d2a8e60451'
csrf = CSRFProtect(app)



@app.cli.command("init-db")
def init_db():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    email = request.form.get('email')
    password = request.form.get('password')
    context = {}
    if request.method =='POST' and form.validate():    
        if (email, password) in db():
            context = {'alert_message': "Вы вошли "}
            return render_template('login.html',form = form, **context)
        context = {'alert_message': "Вход не выполнен "}
    return render_template('login.html',form = form, **context)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        surname = form.name.data
        email = form.email.data
        password = form.password.data

        existing_user = User.query.filter((User.name == name)| (User.surname == surname) | (User.email == email)).first()

        if existing_user:
            error_msg = 'Username or email already exists.'
            form.name.errors.append(error_msg)
            return render_template('register.html', form=form)

        user = User(name=name, surname=surname, email=email, password=password)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return 'Registered success!'
    return render_template('register.html', form = form)

with app.app_context(): 
    db.create_all() 

if __name__ == '__main__':
    app.run(debug=True)