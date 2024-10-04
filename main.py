from flask import Flask
from flask import render_template, redirect, request, url_for, flash, session
import confind
from datetime import timedelta
'''
TODO
social medialization
- account viewing page
- encrypt passwords
- comments
- voting system

later:
if user makes new entry of different equation that results in same answer, add it to the other one
expand DB to third level ops
idiotproofing, error msgs and whatever
number line viewer 
'''

app = Flask(__name__)
app.secret_key = "password"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=60)


@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop("user")
        flash("Logged out. Come back soon!", 'success')
    else:
        flash("You aren't logged in!", "usererror")
    return redirect(url_for('home'))

@app.route("/", methods=['POST', 'GET'])
def home():
    query = None
    if request.method == 'POST':
        if request.form['searchbar'] != None:
            results = confind.confind(request.form['searchbar'])
            if isinstance(results, str): # if confind returns an error msg
                flash(results, 'error')
                results = None
                redirect(url_for("home"))
            query = request.form['searchbar']
        else:
            results = None
    else:
        results = None
    return render_template('home.html', results=results, query=query)

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if request.form['passworb'] != request.form['password']:
            flash('Passwords do not match!', 'usererror')
            return redirect(url_for('register'))
        idk = confind.new_user(request.form['username'], request.form['password'], request.form['email'])
        if isinstance(idk, str):
            flash(idk, 'usererror')
            return redirect(url_for('register'))
        else:
            flash(f'Account successfully created, {idk.name}! Welcome!')
            return redirect(url_for('home'))
    return render_template('register.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login_user(request.form['username'], request.form['password'])
    return render_template('login.html')

# this aint a route
def login_user(name, pw):
    user = confind.verify_login(name, pw)
    if isinstance(user, str):
        flash(user, 'usererror') # returns error message as a string if somethings wrong
        return redirect(url_for('login'))
    else:
        flash("Logged in successfully.", 'success')
        session["user"] = user.name
    return True

@app.route("/newconst", methods=['POST', 'GET'])
def newconst():
    if 'user' not in session:
        flash('Please log in to submit a constant!', 'usererror')
        redirect(url_for(home))
    else:
        if request.method == 'POST':
            eq, usr, notes, cname = request.form['equation'], session["user"], request.form['notes'], request.form['constantname']
            if eq and usr and notes and cname:
                if isinstance(usr, str):
                    if isinstance(cname, str):
                        b = confind.add_user_const(usr, cname, eq, notes)
                        try:
                            a = int(b)
                        except TypeError:
                            flash(b, 'error')
                            return redirect(url_for("newconst"))
                        except ValueError:
                            flash(b, 'usererror')
                            return redirect(url_for("newconst"))

                        if isinstance(b, str):
                            flash(b, 'usererror')
                            return redirect(url_for("newconst"))
                        else:
                            flash('Constant successfully added!', 'success')
                            return redirect(url_for("home")) # should be changed to constant viewing page when that works
                    else:
                        flash('Constant name must contain letter characters!', 'usererror')
                        return redirect(url_for("newconst"))
                else:
                    flash('Username must contain letter characters!', 'usererror')
                    return redirect(url_for("newconst"))
            else:
                flash('Please fill in all fields to submit this form.', 'usererror')
                return redirect(url_for("newconst"))
    return render_template('newconst.html')

@app.route("/viewconst/<id>", methods=['POST', 'GET'])
def viewconst(id):
    constdata = confind.confind(False, False, False, False, id)
    if not constdata:
        flash('No constant with that ID exists!', 'usererror')
        return redirect(url_for("home"))
    soldata = confind.solfind(id)
    return render_template('viewconst.html', constdata = constdata, soldata = soldata)


if __name__ == "__main__":
    with app.app_context():
        confind.db.init_app(app)
        confind.db.create_all() # set up the stuff
        confind.does_table_exists() # does the data inside the table exist? if not, make it
        confind.db.session.commit # lock in

    app.run(debug=True, host= '0.0.0.0')