#!/usr/bin/python3
"""Starts a Flask web app"""

from models import storage
from models.state import State
from flask import Flask, render_template
from sqlalchemy import desc

app = Flask(__name__)


@app.teardown_appcontext
def remove_storage_session(exc):
    """use storage for fetching data from the storage engine
    """
    storage.close()

    @app.route('/states_list', strict_slashes=False)
    def states_list():
        """Display a HTML page inside the tag BODY"""
        states = storage.all(State)
        render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
