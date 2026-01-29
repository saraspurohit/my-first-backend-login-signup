from flask import Flask,request,redirect,url_for,session,Response

app=Flask(__name__)
app.secret_key="supersecret"

#homepage login page
@app.route("/",methods=['GET','POST'])
def  login():
 if request.method=='POST':
     username =request.form.get("username")
     password=request.form.get("password")
     with open('data.txt','a') as k:
         k.write(f"{username},{password}\n") 
     if username =="admin" and password=="123":
      session["user"] = username#store in session               
      return redirect(url_for("welcome"))
     else:
         return Response("In valid credentials. Try again",mimetype="text/plain")
    
 return '''
    <h2>Login Page</h2>
    <form method="POST"><br>
    <b>Username</b>:<input type="text" name ="username"><br>
    <b>Password</b>:<input type="password" name="password"><br>
    <input type ="submit" value="Login"><hr>
    </form>

'''

@app.route("/welcome")
def welcome():
    if "user" in session:
        return f'''
        <h2>Welcome,{session["user"]}!</h2>
        <a href="{url_for('logout')}">Logout</a>
    
    '''
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user",None)#session[user]="sagar"
    return redirect(url_for("login"))