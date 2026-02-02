from flask import Flask,render_template,request,redirect,flash,url_for
app=Flask(__name__)
app.secret_key="my-secret-key"


@app.route("/",methods=["GET","POST"])
def form():
    if request.method=="POST":
         name = request.form.get("username")
         if not(name):
             flash("NAME is required")
             return redirect(url_for("form"))
         flash(f"Thanks {name}, your feedback is saved")
         return redirect("/thanks")     
    return render_template("form.html") 

@app.route("/thanks")
def thankyou():
    return render_template("thanks.html")