from flask import session

def error_for_list_title(title, lists):
    if any(lst['title'] == title for lst in lists):
        return "The title must be unique."
    elif not 1 <= len(title) <= 100:
        return "The title must be between 1 and 100 characters"
    return None
        
def error_for_todo_name(title):
    if not 1 <= len(title) <= 100:
        return "The title must be between 1 and 100 characters"
    return None

def find_list_from_id(lst_id):
    # find the list that matches the id (only 1 match possible, so 'next' works)
    lst = next((lst for lst in session['lists'] if lst['id'] == lst_id), None)
    return lst

def find_item_from_list(lst, item_id):
    # find the item that matches the id (only 1 match possible, so 'next' works)
    item = next((item for item in lst if item['id'] == item_id), None)
    return item

def remove_item_by_id(lst, item_id):
    for idx, item in enumerate(lst['todos']):
        if item['id'] == item_id:
            lst['todos'].remove(item)

def items_remaining(lst):
    return sum([1 for item in lst['todos'] if not item['completed']])

def list_is_completed(lst):
    return items_remaining(lst) == 0 and len(lst['todos']) > 0

def item_is_completed(item):
    return item['completed']

def sort_items(items, function):
    sorted_items = sorted(items, key=lambda item: item['title'].lower())

    unfinished_items = [item for item in sorted_items if not function(item)]
    finished_items = [item for item in sorted_items if function(item)]

    return unfinished_items + finished_items
