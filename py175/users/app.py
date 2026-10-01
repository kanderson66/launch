# https://launchschool.com/lessons/9904914e/assignments/74440a4e
from flask import Flask, render_template, g, redirect
import yaml

app = Flask(__name__)

@app.before_request
def load_users():
    with open("static/users.yaml", "r") as file:
        g.users_info = yaml.safe_load(file)
        g.usernames = list(g.users_info.keys())
        g.total_interests = total_interests()

def total_interests():
    total = 0
    for user in g.usernames:
        total += len(g.users_info[user]['interests'])
    return total


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/user/<username>')
def user(username):
    if username in g.usernames:
        return render_template('user.html', current_username=username)
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, port=5003)