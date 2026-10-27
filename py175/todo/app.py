# cd py175/todo
# poetry install
# poetry run python app.py
# help, see LSBot convo https://launchschool.com/lessons/daa88218/assignments/509639cf
from flask import Flask, render_template, redirect, url_for, session, request, flash
from werkzeug.exceptions import NotFound
from uuid import uuid4
from functools import wraps
import os
from todos.util import ( error_for_list_title, error_for_todo_name, 
                        find_list_from_id, find_item_from_list, 
                        remove_item_by_id, items_remaining, sort_items,
                        item_is_completed, list_is_completed)

app = Flask(__name__)
app.secret_key='secret1'

@app.before_request
def initialize_session():
    if 'lists' not in session:
        session['lists'] = []

@app.context_processor
def list_utilities_processor():
    return dict(
        list_is_completed=list_is_completed
    )

def require_list(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        lst_id = kwargs.get('lst_id')
        lst = find_list_from_id(lst_id)
        if not lst:
            raise NotFound(description="List not found")
        return f(desired_list=lst, *args, **kwargs)

    return decorated_function

def require_item(f):
    @wraps(f)
    @require_list
    def decorated_function(desired_list, *args, **kwargs):
        item_id = kwargs.get('item_id')
        item = find_item_from_list(desired_list['todos'], item_id)
        if not item:
            raise NotFound(description="Todo not found")
        return f(desired_list=desired_list, desired_item=item, *args, **kwargs)

    return decorated_function

@app.route("/")
def index():
    return redirect(url_for('get_lists'))

@app.route("/lists")
def get_lists():
    lists = sort_items(session['lists'], list_is_completed)
    return render_template('lists.html', 
                            lists=lists,
                            items_remaining=items_remaining)

@app.route("/lists", methods=["POST"])
def create_list():
    title = request.form["list_title"].strip()
    error_message = error_for_list_title(title, session['lists'])

    if error_message:
        flash(error_message, "error")
        return render_template('new_list.html', title=title)  

    session['lists'].append({
        'id': str(uuid4()),
        'title': title, 
        'todos': []
        })
    flash("The list has been created.", "success")
    session.modified = True
    return redirect(url_for('get_lists'))

@app.route("/lists/new")
def add_todo_list():
    return render_template('new_list.html')

@app.route("/lists/<lst_id>")
@require_list
def list_items(desired_list, lst_id):
    desired_list['todos'] = sort_items(desired_list['todos'], item_is_completed)

    return render_template('list.html', desired_list=desired_list)

@app.route("/lists/<lst_id>", methods=["POST"])
@require_list
def add_list_item(desired_list, lst_id):

    todo_name = request.form['todo_name'].strip()

    error_message = error_for_todo_name(todo_name)
    if error_message:
        flash(error_message, "error")
        return render_template('list.html', desired_list=desired_list)

    todo_item = {'id': str(uuid4()),
                'title': todo_name,
                'completed': False,
                }
    desired_list['todos'].append(todo_item)
    flash("The todo item has been added.", "success")
    session.modified = True

    return redirect(url_for('list_items', lst_id=lst_id))

@app.route("/lists/<lst_id>/todos/<item_id>/delete", methods=["POST"])
@require_item
def remove_list_item(desired_list, desired_item, lst_id, item_id):
    remove_item_by_id(desired_list, item_id)

    flash("The todo item has been removed.", "success")
    session.modified = True

    return redirect(url_for('list_items', lst_id=lst_id))

@app.route("/lists/<lst_id>/todos/<item_id>/toggle", methods=["POST"])
@require_item
def check_item(desired_list, desired_item, lst_id, item_id):
    desired_item['completed'] = not desired_item['completed']

    complete = 'completed' if desired_item['completed'] else 'de-completed'
    flash(f"The todo item has been {complete}.", "success")

    session.modified = True

    return redirect(url_for('list_items', lst_id=lst_id))

@app.route("/lists/<lst_id>/complete_all", methods=["POST"])
@require_list
def check_all(desired_list, lst_id):
    for item in desired_list['todos']:
        item['completed'] = True

    flash("All todos completed.", "success")
    session.modified = True

    return redirect(url_for('list_items', lst_id=lst_id))

@app.route("/lists/<lst_id>/edit")
@require_list
def edit_list(desired_list, lst_id):
    return render_template("edit_list.html", desired_list=desired_list)

@app.route("/lists/<lst_id>/delete", methods=["POST"])
@require_list
def delete_list(desired_list, lst_id):
    session['lists'] = [lst for lst in session['lists'] if lst['id'] != lst_id]
    session.modified = True

    flash("List deleted.", "success")
    return redirect(url_for('get_lists'))

@app.route("/lists/<lst_id>/rename", methods=["POST"])
@require_list
def rename_list(desired_list, lst_id):

    title = request.form["list_title"].strip()
    error_message = error_for_list_title(title, session['lists'])

    if error_message:
        flash(error_message, "error")
        return render_template("edit_list.html", desired_list=desired_list)  
    
    desired_list['title'] = title
    session.modified = True
    
    return redirect(url_for('list_items', lst_id=lst_id))

if __name__ == "__main__":
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(debug=False)
    else:
        app.run(debug=True, port=5003)
