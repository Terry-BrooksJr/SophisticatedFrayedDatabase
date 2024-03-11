
from flask import Flask, render_template
import os
from utils  import sign_url
import time

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/")
    def index():
        return render_template('report.html', signed_url=sign_url(
    url=f"https://app.mode.com/solutionssandbox/reports/663318dbd45e/embed?access_key=10487a1c9fd81d6d97ecf5c3&run=now&timestamp={time.time()}/",key="10487a1c9fd81d6d97ecf5c3",secret="8b8ae202152c971a66980392"))

    return app