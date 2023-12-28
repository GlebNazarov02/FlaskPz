import flask
from flask import render_template

app = flask.Flask(__name__)

@app.route('/')
def base():
    return render_template('base.html')


@app.route("/", methods=["GET", "POST"])
def index():
    if flask.request.method == "POST":
        name = flask.request.form.get("name")
        email = flask.request.form.get("email")
        response = flask.make_response(flask.redirect("/welcome"))
        response.set_cookie("name", name)
        response.set_cookie("email", email)
        return response

@app.route("/welcome")
def welcome():
    name = flask.request.cookies.get("name")
    if name:
        return render_template('welcome.html', name=name)
    else:
        return flask.redirect("/")

@app.route("/logout")
def logout():
    response = flask.make_response(flask.redirect("/"))
    response.set_cookie("name", "", expires=0)
    response.set_cookie("email", "", expires=0)
    return response

if __name__ == "__main__":
    app.run()