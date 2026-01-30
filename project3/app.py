from flask import Flask, render_template, request, redirect, session, flash
import csv
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"

USERS_FILE = "users.csv"
DATA_DIR = "data"

# ---------------- SETUP ----------------
os.makedirs(DATA_DIR, exist_ok=True)

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["username", "password"])


def user_csv():
    return os.path.join(DATA_DIR, f"{session['user']}.csv")


def login_required():
    return "user" not in session


# ---------------- LANDING PAGE ----------------
@app.route("/")
def welcome():
    return render_template("welcome.html")


# ---------------- SIGN UP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        # Check if user exists
        with open(USERS_FILE) as f:
            for row in csv.DictReader(f):
                if row["username"] == username:
                    flash("Username already exists ❌")
                    return redirect("/signup")

        # Save user
        with open(USERS_FILE, "a", newline="") as f:
            csv.writer(f).writerow([username, password])

        # Create personal student file
        with open(os.path.join(DATA_DIR, f"{username}.csv"), "w", newline="") as f:
            csv.writer(f).writerow(["Name", "Marks"])

        flash("Account created successfully ✅")
        return redirect("/login")

    return render_template("signup.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
         flash("Invalid form submission ❌")
         return redirect("/signup")


        with open(USERS_FILE) as f:
            for row in csv.DictReader(f):
                if row["username"] == username and row["password"] == password:
                    session["user"] = username
                    return redirect("/dashboard")

        flash("Invalid username or password ❌")

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if login_required():
        return redirect("/login")

    with open(user_csv()) as f:
        students = list(csv.DictReader(f))

    return render_template(
        "index.html",
        data=students,
        user=session["user"]
    )


# ---------------- ADD STUDENT ----------------
@app.route("/add", methods=["GET", "POST"])
def add():
    if login_required():
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"].strip()
        marks = request.form["marks"].strip()

        with open(user_csv()) as f:
            for row in csv.DictReader(f):
                if row["Name"].lower() == name.lower():
                    flash("Student already exists ❌")
                    return redirect("/add")

        with open(user_csv(), "a", newline="") as f:
            csv.writer(f).writerow([name, marks])

        flash("Student added successfully ✅")
        return redirect("/dashboard")

    return render_template("add.html")


# ---------------- EDIT STUDENT ----------------
@app.route("/edit/<name>", methods=["GET", "POST"])
def edit(name):
    if login_required():
        return redirect("/login")

    with open(user_csv()) as f:
        students = list(csv.DictReader(f))

    if request.method == "POST":
        new_marks = request.form["marks"]

        for s in students:
            if s["Name"] == name:
                s["Marks"] = new_marks

        with open(user_csv(), "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Name", "Marks"])
            writer.writeheader()
            writer.writerows(students)

        return redirect("/dashboard")

    student = next(s for s in students if s["Name"] == name)
    return render_template("edit.html", student=student)


# ---------------- DELETE STUDENT ----------------
@app.route("/delete/<name>")
def delete(name):
    if login_required():
        return redirect("/login")

    with open(user_csv()) as f:
        students = [s for s in csv.DictReader(f) if s["Name"] != name]

    with open(user_csv(), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Marks"])
        writer.writeheader()
        writer.writerows(students)

    return redirect("/dashboard")


# ---------------- REPRESENT DATA ----------------
@app.route("/represent")
def represent():
    if login_required():
        return redirect("/login")

    names, marks = [], []

    with open(user_csv()) as f:
        for row in csv.DictReader(f):
            names.append(row["Name"])
            marks.append(int(row["Marks"]))

    return render_template("represent.html", names=names, marks=marks)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
