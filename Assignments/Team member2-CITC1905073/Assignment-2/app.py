from flask import Flask,render_template,request,session 
import ibm_db
import re 

app = Flask(__name__)
app.secret_key='a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=vjl29194;PWD=lPUoIHGoqZgeG88O;","","")

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/login",methods=["GET","POST"])
def login():
    global userid
    msg = " "
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM USERDATA WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin'] = True
            session['id'] = account ['USERNAME']
            userid = account["USERNAME"]
            session['username'] = account["USERNAME"]
            msg = "Logged IN successfully!"
            return render_template('dashboard.html',msg=msg,username = session['username'])
        else:
            msg = "Incorrect Username or Password"
    return render_template('login.html',msg=msg)

@app.route("/register",methods=["GET","POST"])
def register():
    msg = " "
    if request.method=="POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM USERDATA WHERE username =?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg="Account already exists!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg = "Invalid Email Address!"
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg = "name must contain only characters and numbers"
        else:
            insert_sql = "INSERT INTO USERDATA VALUES(?,?,?)"
            prep_stmt = ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,username)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt,3,password)
            ibm_db.execute(prep_stmt)
            msg = "You have successfully Logged In"
            return render_template('dashboard.html',msg=msg,username = username)
    elif request.method=="POST":
        msg = "Please fill out the form!"
    return render_template('register.html',msg=msg)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    return render_template('register.html')

if __name__=='__main__':
    app.run('0.0.0.0',debug=True)
