from flask import Flask, g, render_template, request, redirect
import sqlite3
app = Flask(__name__)
database_login = './DATABASES/login.db'

def get_db():
    db = getattr(g,'_database', None)
    if db is None:
        db = g._databsae = sqlite3.connect(database_login)
    return db
'''Routes'''

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def signin():
    return render_template('login.html')
    cursor = get_db().cursor
    sql = 'SELECT * FROM contents'
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('login.html', results=results)

@app.route('/signup', methods=['GET', 'POST'])
def new_user():
    return render_template('signup.html')
    if request.method == "POST":
        cursor = get_db().cursor()
        new_name = request.form["user_name"]
        new_description = request.form["user_password"]
        sql = "INSERT INTO contents(user_name, user_password) VALUES (?,?)"
        cursor.execute(sql,(new_name,new_description))
        get_db().commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)