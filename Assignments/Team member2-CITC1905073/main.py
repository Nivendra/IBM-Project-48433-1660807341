from flask import Flask, redirect,render_template, request, url_for

app = Flask(__name__)

userdata = {}

@app.route('/',methods=["GET","POST"])
def register():
    if request.method=="POST":
        userdata["username"] = request.form.get("username")
        userdata["email"] = request.form.get("email")
        userdata["phone"] = request.form.get("phone")
        return redirect(url_for("home"))
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("home.html",formdata = userdata)

if __name__=='__main__':
    app.run(debug=True)