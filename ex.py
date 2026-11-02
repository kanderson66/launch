from pprint import pp
from uuid import uuid4

# Year, month, day, ID: [type, amount, category, account, desc]
data = {}

def add_item(date, item):
    d = go_to_layer(date)
    id = str(uuid4())
    fields = ["Type", "Amount", "Category", "Account", "Desc"]

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
    d = data
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

def sort_data(data):
    for year in data:
        for month in data[year]:
            data[year][month] = dict(sorted(data[year][month].items()))
        data[year] = dict(sorted(data[year].items()))
    data = dict(sorted(data.items()))
    # print(f"\n\nIn func:")
    # pp(data)
    # print("\n\nOut of func:\n")
    return data

def test_total_dates_and_filters():
    global data
    data = {}

    date = ["2026", "10", "30"]
    item1 = ["Expense", 20, "House", "Kurtis", "First test data"]
    item2 = ["Expense", 40, "House", "Kurtis", "Second test data"]

    add_item(date, item1)
    add_item(date, item2)

    date1 = ["2026", "10", "29"]
    item1 = ["Income", 20, "House", "Kurtis", "First test data"]
    item2 = ["Income", 40, "House", "Kurtis", "Second test data"]

    add_item(date1, item1)
    add_item(date1, item2)

    date2 = ["2026", "11", "29"]
    item1 = ["Income", 20, "House", "Kurtis", "First test data"]
    item2 = ["Income", 40, "Groc", "Kurtis", "Second test data"]

    add_item(date2, item1)
    add_item(date2, item2)

    assert calc_total(date1) == 60
    assert calc_total(date1[:-1]) == 120
    assert calc_total(date1[:-2]) == 180
    assert calc_total(date1[:-2], ["House"]) == 140
    assert calc_total(date1[:-1], ["House", "Income"]) == 60

def test_moving_items():
    global data
    data = {}

    date = ["2026", "10", "30"]
    item1 = ["Expense", 20, "House", "Kurtis", "First test data"]
    item2 = ["Expense", 40, "House", "Kurtis", "Second test data"]

    add_item(date, item1)
    add_item(date, item2)

    new_date = ["2021", "11", "31"]
    ids = [item_id for item_id in go_to_layer(date)]
    for item_id in ids:
        move_item(item_id, new_date)

    # ensure both items listed under date of new_date, and no empty dates exist
    # pp(data)
    
    # items exist under new year
    assert data.get(new_date[0], False) != False

    # no items exist under old year (all moved and date deleted)
    assert data.get(date[0], False) == False

def test_sort_data():
    global data
    data = {}

    date = ["2026", "10", "30"]
    item1 = ["Expense", 20, "House", "Kurtis", "First test data"]
    add_item(date, item1)

    date = ["2026", "09", "29"]
    item2 = ["Expense", 40, "House", "Kurtis", "Second test data"]

    add_item(date, item2)

    date = ["2026", "10", "29"]
    item2 = ["Expense", 40, "House", "Kurtis", "Second test data"]

    add_item(date, item2)

    date = ["2026", "09", "30"]
    item2 = ["Expense", 40, "House", "Kurtis", "Second test data"]

    add_item(date, item2)

    date = ["2025", "10", "29"]
    item2 = ["Expense", 40, "House", "Kurtis", "Second test data"]

    add_item(date, item2)
        
    # pp(data)
    data = sort_data(data)
    pp(data)

test_total_dates_and_filters()  # assert
test_moving_items()           # assert (print is better test)
test_sort_data()
