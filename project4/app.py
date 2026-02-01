from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main():
  return render_template("base.html")
  
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    print("METHOD:", request.method)   # DEBUG

    if request.method == "POST":
        name = request.form.get("username")
        message = request.form.get("message")

        print("NAME:", name)           # DEBUG
        print("MESSAGE:", message)     # DEBUG

        return render_template(
            "thankyou.html",
            user=name,
            message=message
        )

    return render_template("feedback.html")

app.run(debug=True)
