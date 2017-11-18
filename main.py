from flask import Flask, Response, redirect, url_for, request, session, abort, render_template
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user 
app = Flask(__name__)

@app.route('/')
def render_home():
    return render_template('home.html')

@app.route('/map')
def render_map():
	return render_template('worldmap.html')

@app.route('/map-temp')
def render_map_temp():
	return render_template('worldMapPage.html')

@app.route('/upload')
def render_map_temporary():
	return render_template('upload.html')


#LOGIN_________________________________________________
#______________________________________________________


# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


# create some users with ids 1 to 20       
users = [User(id) for id in range(1, 21)]


# some protected url
@app.route('/')
@login_required
def home():
    return Response("Hello World!")

 
# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
        if password == username + "_secret":
            id = username.split('user')
            user = User(id)
            login_user(user)
            return redirect("/upload")
        else:
            return abort(401)
    else:
        return render_template('login.html')


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return render_template('login.html')
    
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)