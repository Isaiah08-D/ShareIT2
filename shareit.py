from flask import Flask, render_template, flash, redirect, session, url_for
import os 
from replit import db
from flask_bootstrap import Bootstrap
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
bootstrap = Bootstrap(app)
db['new'] = [os.getenv('SECRET_KEY'), [	['Testing', 'isaiah08', 'JUST TESTING!!hjfkhflajfsadkfjsdlfkdsfjsdkfjaldfjafshfhslafjlsahslfsjflsajfdlskjfsldkafjdasklfjaslfjaslkfjasdlkfjsalfjaslfasjflasjfalkdjfaksfsdfjaslfkajldkjalsfjdaslfjalfjasdkfljalkfjsflksdjfslkjfslfjsklfjsalkfdsjfaldjfldkjfaslkfjaklfjeirueifudsifujasdfjadsklfjasdlfkjlfjafasd!', 5] ] ]

class User():
	def __init__(self, username, password):
		self.username = username
		self.password = password
	def create_user(self):
		if self.username not in db:
			# db[username] = [password, posts, total likes]
			db[self.username] = [self.password, [], 0]
			return True
		else:
			return False
	def verify(self):
		try:
			return db[self.username][0] == self.password
		except:
			return False
	def delete_user(self):
		try:
			del db[self.username]
			return True
		except:
			return False

user = User('test', 'pass')
user.delete_user()
user.create_user()


@app.route('/')
def index():
	if session.get('login') == None or session.get('login') == False:
		return redirect(url_for('login'))

	return render_template('index.html')


@app.route('/join', methods=['GET', 'POST'])
def join():
	form = JoinForm()

	if session.get('login') != False and session.get('login') != None:
		flash('You are already logged in!')
		return render_template('index.html')
	if form.validate_on_submit:
		username = form.username.data
		password = form.password.data
		
		user = User(username, password)
		if user.create_user():
			session['login'] = username
			return render_template('index.html')
		else:
			return redirect(url_for('join'))
		
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	if session.get('login') != False and session.get('login') != None:
		flash('You are already logged in!')
		return redirect(url_for('index'))
	form = LoginForm()

	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		user = User(username, password)
		if user.verify():
			session['login'] = username
			return redirect(url_for('index'))
		else:
			session['login'] = False
			return redirect(url_for('login'))
	return render_template('login.html', form=form)

@app.route('/logout')
def logout():
	session['login'] = False
	flash('You have been logged out!')
	return render_template('logout.html')
@app.route('/post', methods=['GET', 'POST'])
def post():
	form = PostForm()
	if form.validate_on_submit():
		title = form.title.data
		post = form.post.data
		# [title, post, likes]
		db[session.get('login')][0].append([title, post, 0])
		# [title, username, post, likes]
		db['new'].insert(0, [title, session.get('login'), post, 0])
		return redirect(url_for('posts'))


	if session.get('login') == False or session.get('login') == None:
		return redirect('login')
	else:
		return render_template('post.html', form=form)

@app.route('/posts')
def posts():
	posts = db['new'][1]
	return render_template('posts.html', posts=posts)
	
@app.route('/@<username>')
def profile(username):
	if session.get('login') == False or session.get('login') == None:
		return redirect(url_for('login'))
	
	try:
		return render_template('profile.html', profile=db[username])
	except:
		return render_template('errors/user_not_found.html')
	
app.run('0.0.0.0')
