from flask import Flask, request, redirect, render_template, flash, url_for
from form import RegistrationForm

app = Flask(__name__)
app.secret_key = "my-secret-key"

@app.route("/", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        flash(f"Welcome, {name}! You registered successfully.", "success")
        return redirect(url_for("sucess"))
    return render_template("register.html", form=form)

@app.route("/success")
def sucess():
    return render_template("success.html")
