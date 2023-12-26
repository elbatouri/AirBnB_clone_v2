#!/usr/bin/python3
"""
script that starts a Flask web application
"""


from flask import Flask, url_for, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """return welcoming sentence"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hello_hbnb():
    """ return welcoming message"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """display 'C '+ text passed with to remove '_' sign"""
    return 'C ' + text.replace('_', ' ')


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def Python_cool(text='is_cool'):
    """display 'Python'+ text passed with to remove '_' sign"""
    return 'Python ' + text.replace('_', ' ')


@app.route('/number/<int:n>', strict_slashes=False)
def n_is_nubmber(n):
    """return  'n is number'if 'n' integer"""
    return "{:d} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def nubmer_html(n):
    """return an HTML generated from template if n integer"""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def even_or_odd(n):
    """Return an html only if number is int"""
    if n % 2 == 0:
        result = 'even'
    else:
        result = 'odd'
    return render_template('6-number_odd_or_even.html', n=n,
                           result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
