import math
import os
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, jsonify
from stats import *
from werkzeug.utils import secure_filename
import json
import pandas as pd

import sqlite3    

app = Flask(__name__)
app.secret_key = 'super-secret-key'



@app.route('/', methods = ['POST', 'GET'])
def Home():
    if request.method == 'POST':
        Model_name = request.form["Model_name"]
        Model_Description = request.form["Model_Desc"]
        Created_by = "User"
        f = request.files['myfile']
        f.save(secure_filename(f.filename))
        file = f.filename
        date = datetime.now()
        insertdata(Model_name, Model_Description, Created_by, file, date)    
        return render_template("home.html", rows=get_all_rows())
    return render_template("home.html", rows=get_all_rows() )
    

@app.route('/visualizations')
def Visualizations():
    return render_template('boxplotreal.html')

@app.route('/violinplot')
def violin():
    return render_template('violinplotreal.html')

@app.route('/stripplot')
def stripplot():
    return render_template('strip.html')

@app.route('/violinboxplot')
def violinbox():
    return render_template('violinandboxplot.html')




@app.route('/data', methods=['GET'])
def Data():
    return render_template('data.html')

@app.route('/faq')
def Faq():
    return render_template('faq.html')

@app.route('/aboutUs')
def AboutUs():
    return render_template('aboutus.html')

@app.route('/summarystatistics')
def SummaryStatistics():
    return render_template('summary.html')

@app.route('/featureimp',  methods=['GET', 'POST'])
def featureimp():
    return render_template('featureimp.html')

@app.route('/cfmatrix')
def cfmatrix():
    return render_template('correlationmx.html')

@app.route('/confusionmatrix')
def confmatrix():
    return render_template('confusionmatrix.html')


@app.route('/businessaction',  methods=['GET', 'POST'])
def businessaction():
    return render_template('BusRevBox.html')

@app.route('/BusRevViolin',  methods=['GET', 'POST'])
def businessviolin():
    return render_template('BusRevViolin.html')

@app.route('/BusRevStrip',  methods=['GET', 'POST'])
def businessstrip():
    return render_template('BusRevStrip .html')


@app.route('/cutoff',  methods=['GET', 'POST'])
def cutoff():
    return render_template('cutoff.html')

@app.route('/get_column_header', methods=['POST', 'GET'])
def get_columns():
    received_data = request.get_json(force=True)
    id = int(received_data)
    print(type(id))
    data = get_column_header(id)
    data = list(data)
    print(data)
    return jsonify(data)





@app.route("/get_data", methods=['POST', 'GET'])
def data():
    received_data = request.get_json(force=True)
    a = received_data["a"]
    b = received_data["b"]
    print(a, b)
    df = pd.read_csv("static/js/EQWT.csv")
    column = list(df.columns)
    new_columns = []
    if b['f0'] == True:
        j = 0
        for k in range(0, len(b) - 1):
            new_columns.append(column[j])
        j = j + 1
    else:
        if b['f1'] == True:
            new_columns.append(column[0])
        if b['f2'] == True:
            new_columns.append(column[1])
        if b['f3'] == True:
            new_columns.append(column[2])
        if b['f4'] == True:
            new_columns.append(column[3])
        if b['f5'] == True:
            new_columns.append(column[4])
        if b['f6'] == True:
            new_columns.append(column[5])


    df_alerts = df[df['has_alerted'] == 1]
    df_nonalerts = df[df['has_alerted'] == 0]
    df_escalations = df[df['has_escalated'] == 1]
    result = {}
    if a['all'] == True:
        for column in new_columns:
            result[column]['non-alerts'] = (list(df_nonalerts[column]))
            result[column]['alerts'] = (list(df_alerts[column]))
            result[column]['escalations'] = (list(df_escalations[column]))

    else:
        for column in new_columns:
            result[column] = {}
            for keys in a:
                if a[keys] == True:
                    if keys == 'non-alert':
                        result[column]['non-alerts'] = (list(df_nonalerts[column]))
                    if keys == 'alert':
                        result[column]['alerts'] = (list(df_alerts[column]))
                    if keys == 'escalations':
                        result[column]['escalations'] = (list(df_escalations[column]))
                    
                else:
                    if keys == 'All':
                        continue
                    else:
                        if keys == 'non-alert':
                            result[column]['non-alerts'] = []
                        if keys == 'alert':
                            result[column]['alerts'] = []
                        if keys == 'escalations':
                            result[column]['escalations'] = []


    return jsonify(result)

app.run(debug=True)
