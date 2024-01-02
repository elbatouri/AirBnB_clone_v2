#!/usr/bin/python3
"""Starts a flask app
    listens to 0.0.0.0:5000
"""

from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Return a ordred list of states to display it on html page """
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown(exc):
    """
    remove the open sqlalchemy session.
    """


storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
