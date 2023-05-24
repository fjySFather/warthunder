from flask import Flask, render_template, url_for, redirect, request
from flask_login import LoginManager, login_required, login_user, current_user, UserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

heads = {
    'content-type': 'application/x-www-form-urlencoded'
}
users = {'admin': {'password': '114514'}, 'test': {'password': '1919810'}}

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user
class Record:
    def __init__(self, id, title, author, content, time=None):
        self.id = id
        self.title = title
        self.author = author
        self.content = content
        self.time = time or datetime.now()

    def save(self):
        all_records.append({
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'content': self.content,
            'time': self.time
        })




admin = Admin(app, name='Admin', template_mode='bootstrap3')

all_records = []

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' or request.form.get('method') == 'POST':
        password = request.form['password']

        for username, user in users.items():
            if password == user.get('password'):
                user = User()
                user.id = username
                login_user(user)
                return redirect(url_for('dashboard'))
        
        return render_template('login.html')
    
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = current_user.id
        # get id from total number of posts
        post_id = len(all_records) + 1 
        record = Record(id=post_id, title=post_title, content=post_content, author=post_author)
        record.save()
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', username=current_user.id, records=all_records)


@app.route('/<int:id>')
@login_required
def detail(id):
    record = None
    for r in all_records:
        if r['id'] == id:
            record = r
            break
    if not record:
        return 'Record not found!'
    return render_template('detail.html', record=record)

if __name__ == '__main__':
    app.run(debug=True)
