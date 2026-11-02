# https://launchschool.com/lessons/daa88218/assignments
# filepaths/directories, opening files, yaml, bcrypt password encryption, wraps, testing, markdown, 
from flask import Flask, render_template, send_from_directory, redirect, flash, url_for, request, session
import os
from markdown import markdown
from cms.util import valid_filename
from functools import wraps
import yaml # poetry add pyyaml
from bcrypt import hashpw, gensalt, checkpw # poetry add bcrypt
import re

app = Flask(__name__)
app.secret_key='secret1'

# DECORATORS
def require_login(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session.get('user'):
            return func(*args, **kwargs)
        else:
            flash("Login required")
            return redirect(url_for("sign_in_page"))
    return inner

# HELPERS
def get_file_path():
    if app.config['TESTING']:
        args = ('tests', 'data')
    else:
        args = ('cms', 'data')
    
    root = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(root, *args)

    return file_path

def get_contents(filename):
    path = get_file_path()

    with open(f"{path}/{filename}", 'r') as file:
        contents = file.read()
    return contents

def load_users():
    file_path = get_file_path()
    users = {}

    with open(f'{file_path}/users.yaml', 'r', encoding='utf-8') as file:
        users = yaml.safe_load(file)

    return users

# this can be improved by using more yaml built-in functionality
# see LSBot review https://launchschool.com/posts/95aed98d#:~:text=The%20update_users_contents-,Function,-This%20is%20the
def update_users_contents(contents):
    hashed_contents = ''
    lines = contents.split('\n')
    
    for line in lines:
        username, password = line.split()
        if not is_bcrypt_hash(password):
            password = hash_pw(password)
        hashed_contents += f'{username} {password}\n'

    file_path = get_file_path()

    with open(f"{os.path.join(file_path, 'users.yaml')}", 'w') as file:
        file.write(hashed_contents[:-1])    # -1 to remove last empty line

    return

def is_bcrypt_hash(password: str) -> bool:
    # Pattern explanation:
    # ^\$2[abxy]\$ -> Starts with $2a$, $2b$, $2x$, or $2y$
    # (?:0[4-9]|[12][0-9]|3[01])\$ -> Followed by a cost factor from 04 to 31 and a $
    # [./0-9a-zA-Z]{53}$ -> Ends with exactly 53 valid bcrypt-base64 characters
    bcrypt_regex = r"^\$2[abxy]\$(?:0[4-9]|[12][0-9]|3[01])\$[./0-9a-zA-Z]{53}$"

    return bool(re.match(bcrypt_regex, password))

def hash_pw(password):
    hashed = hashpw(password.encode(), gensalt())     # .encode() turns string into bytes (identical to b'{password}')
    password = hashed.decode('utf-8') # .decode() turns bytes into string (removes b'...')
    return password

# ROUTES
@app.route("/")
def index():
    file_path = get_file_path()
    files = os.listdir(file_path)
    
    return render_template('index.html', files=files)

@app.route("/<filename>")
def open_file(filename):
    file_path = get_file_path()
    files = os.listdir(file_path)

    if filename not in files:
        flash(f"{filename} does not exist.")
        return redirect( url_for("index")) 

    if filename.endswith("md"):
        with open(f"{os.path.join(file_path, filename)}", 'r') as markdown_page:
            content = markdown_page.read()
            return render_template('markdown.html', content=markdown(content))

    return send_from_directory(file_path, filename)

@app.route("/<filename>/edit")
@require_login
def edit_file(filename):
    contents = get_contents(filename)
    return render_template('edit.html', filename=filename, contents=contents)

@app.route("/<filename>/edit", methods=['POST'])
@require_login
def update_contents(filename):
    contents = request.form['file_contents']

    if filename == 'users.yaml':
        update_users_contents(contents)
    else:
        file_path = get_file_path()

        with open(f"{os.path.join(file_path, filename)}", 'w') as file:
            file.write(contents)

    flash(f'{filename} has been updated.')
    return redirect(url_for('index'))

@app.route("/create_doc")
@require_login
def new_doc():
    return render_template('create_doc.html')

@app.route("/create_doc", methods=['POST'])
@require_login
def create_doc():
    filename = request.form['filename']

    if not valid_filename(filename):
        flash("A name and valid extension are required")
        return render_template('create_doc.html'), 422
    
    file_path = get_file_path()
    with open(os.path.join(file_path, filename), 'w') as file:
        file.write('')

    flash(f"{filename} has been created.")
    return redirect(url_for("index"))

@app.route("/<filename>/delete", methods=['POST'])
@require_login
def delete(filename):
    file_path = get_file_path()
    files = os.listdir(file_path)

    if filename not in files:
        flash(f"{filename} does not exist.")
        return render_template("index.html"), 422
    
    os.remove(os.path.join(file_path, filename))
    flash(f"{filename} has been deleted.")
    
    return redirect(url_for('index'))

@app.route("/sign_in")
def sign_in_page():
    return render_template("sign_in_page.html")

@app.route("/sign_in", methods=['POST'])
def sign_in():
    username = request.form["username"]
    password = request.form["password"]
    users = load_users()

    # @todo
    for user, hashed in users.items():
        # if username == user and hashpw(password.encode(), hashed.encode()) == hashed.encode():
        if username == user and checkpw(password.encode(), hashed.encode()):
        # if username == user and password == passw:
            session['user'] = username
            flash("Welcome!")
            return redirect(url_for('index'))

    flash("Invalid credentials", "error")
    return render_template("sign_in_page.html", username=username), 422

@app.route("/sign_out", methods=['POST'])
def sign_out():
    session['user'] = None
    flash("You have been signed out.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5003)
