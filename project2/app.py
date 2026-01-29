from flask import Flask,render_template,request
app=Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/submit" , methods =["POST"])
def submit():
    username=request.form.get("username")
    password=request.form.get("password")
       
    data = {}
    with open("./project2/data.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line:
                u, p = line.split(",")
                data[u] = p
                
    if username in data and data[username]==(password):
        return render_template("welcome.html",name=username,sy="\n SUCCESFULLY LOGIN")
    else:
        return render_template("login.html", error="❌ Invalid username or password")

@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form.get("username")
    password = request.form.get("password")
    confirm = request.form.get("confirm_password")

    if password != confirm:
        return render_template("signup.html", error="❌ Passwords do not match")

    data = {}
    with open("./project2/data.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line:
                u, p = line.split(",")
                data[u] = p


    if username in data:
        return render_template("signup.html", error="❌ Username already exists")

    with open("./project2/data.txt", "a") as file:
        file.write(f"{username},{password}\n")

    return render_template("welcome.html",name=username,sy="\n SUCCESFULLY SIGN UP", error="✅ Account created!")

if __name__ == "__main__":
    app.run(debug=True)