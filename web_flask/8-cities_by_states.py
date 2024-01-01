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
    """Return list of states of states
    and related cities ordered by name
    display it on html page
    """
    states = storage.all("State")
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def teardown(exc):
    """
    remove the open sqlalchemy session.
    """


storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
