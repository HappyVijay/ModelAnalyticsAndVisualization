from flask import *
from werkzeug.utils import secure_filename
import pandas as pd
from stats import *
import sqlite3
from datetime import datetime


app = Flask(__name__)


@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        Model_name = request.form["Model_name"]
        Model_Description = request.form["Model_Desc"]
        Created_by = "User"
        f = request.files['myfile']
        f.save(secure_filename(f.filename))
        file = f.filename
        date = datetime.now()
        insertdata(Model_name, Model_Description, Created_by, file, date)
        
        return render_template("LandingPage.html", rows=get_all_rows())
    return render_template("LandingPage.html")


if __name__ == "__main__":
    app.run(debug = True)
