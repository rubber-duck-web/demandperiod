from flask import Flask, request, jsonify, abort
from demandperiodclass import demandperiod
import datetime

app = Flask(__name__)
a=demandperiod()
@app.route('/demandperiod/<date>')

def check_in(date):
    test,year=demandperiod.testdate(date)
    if test:
        a.generate(year)
    else:
        abort(500)
    if len(date)==4:
        return jsonify(a.returnyeardemanperiods())
    if len(date)==7:
        return jsonify(a.returnyearmonthdemanperiods(date[5:7]))
    if len(date)==10:
        return jsonify(a.returndaydemanperiods(date))
        
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)