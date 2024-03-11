
from flask import Flask, render_template
import os
from reports.utils  import sign_url, current_time
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
    @app.route("/report")    
    @app.route("/home")
    @app.route("/index")    
    def index():
        return render_template('report.html', signed_url=sign_url(url=f'https://app.mode.com/solutionssandbox/reports/663318dbd45e/embed?access_key={os.getenv("ACCESS_KEY")}&max_age=2629800&timestamp={current_time}', key=os.getenv('ACCESS_KEY'), secret=os.getenv('ACCESS_SECRET')
                                                                  )
                               )
    return app
