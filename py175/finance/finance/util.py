from pprint import pp
import json
from uuid import uuid4

# Year, month, day, ID: [type, amount, category, account, desc]
# data = {}
def load_data():
    with open('finance/data/entries.json', 'r') as file:
        data = json.load(file)
    return data

def add_item(date, item):
    d = go_to_layer(date)
    id = str(uuid4())
    fields = ["type", "amount", "category", "account", "desc"]

    d[id] = {field: item[idx] for idx, field in enumerate(fields)}

def move_item(item_id, new_date):
    old_date = find_date(item_id)
    transaction = go_to_layer([*old_date, item_id])
    
    add_item(new_date, list(transaction.values()))
    remove_item(old_date, item_id)
    
    remove_empty_layers(old_date)

def remove_item(date, item_id):
    d = go_to_layer(date)
    d.pop(item_id)

def remove_empty_layers(date):
    d = go_to_layer(date)
    loop_count = -1
    
    while not d:
        d = go_to_layer(date[:loop_count])
        d.pop(date[loop_count])
        loop_count -= 1

def find_date(item_id):
    for year, months in data.items():
        for month, days in months.items():
            for day, transactions in days.items():
                if item_id in transactions:
                    return [year, month, day]
    return None  # ID not found

def go_to_layer(date):
    d = load_data()
    for date_part in date:
        d = d.setdefault(date_part, {})
    return d

def calc_total(date, filters=[]):
    total = 0
    layer = go_to_layer(date)

    for key in layer:
        # date has year, month, and day.    Key is id
        if complete_date(date):
            transaction = list(layer[key].values())

            if matches_filters(transaction, filters):
                total += layer[key]["Amount"]
        else:
            # date missing month and/or day.    Key is month or day- add onto current date and redo
            total += calc_total([*date, key], filters)
    return total

def complete_date(date):
    return len(date) == 3

def matches_filters(transaction, filters):
    for filter in filters:
        if filter not in transaction:
            return False
    return True