from flask import Flask, render_template, g
from pprint import pp
import finance.util as util

app = Flask(__name__)

date = ["2026", "10", "29"]

@app.route('/')
def transactions():
    d = util.go_to_layer(date)
    pp(d)

    return render_template("transactions.html", date=date, transactions=d)

@app.route('/stats')
def stats():
    return render_template("stats.html")

if __name__ == '__main__':
    app.run(debug=True, port=5003) 