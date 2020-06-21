import math
import os
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, jsonify
from stats import *
from werkzeug.utils import secure_filename
import json
import pandas as pd

import sqlite3

id = 0

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
    
@app.route('/send_data', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        received = request.get_json(force=True)
        a = received["a"]
        b = received["b"]
        score = a["score"]
        outcome = a["outcome"]
        alert = a["alert"]
        business_action = a["businessaction"]
        escalation = a["escalation"]
        features = ""
        cols = get_column_header(id)
        for col in cols:
            if b[col] == True:
                features += col + ","
        print(features)
        updatedata(features, score, outcome, alert, business_action, escalation, id)
        return "successful"
    return "unsuccessful"



@app.route('/visualizations')
def Visualizations():
    count = get_feature_count(id)
    return render_template('boxplotreal.html', count = count)

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
    #flag =1 is for alerted
    #flag =2 is for non-alerted
    #flag = 3 is for escalations
    statistics_of_all_feature(id,1, "static/js/statistics_of_alert_featurenew.csv")
    statistics_of_all_feature(id,2, "static/js/statistics_of_nonalert_feature.csv")
    statistics_of_all_feature(id,3, "static/js/statistics_of_escalated_feature.csv")
    total_cases_surv,alert_per_surv,nonalert_per_surv,escalations_per_surv = common_calculations(id)

    #file name static/js/statistics_of_alert_featurenew.csv
    return render_template('summary.html', total_case = total_cases_surv, alert_per_surv = alert_per_surv,nonalert_per_surv=nonalert_per_surv,escalations_per_surv= escalations_per_surv)

@app.route('/featureimp',  methods=['GET', 'POST'])
def featureimp():
    #### id is static for now need to change afterwards to make dashboard generic
    feature_imp(id,0,"static/js/feature_imp_escalations.csv")
    feature_imp(id,1,"static/js/feature_imp_alert.csv")
    return render_template('featureimp.html')

@app.route('/cfmatrix')
def cfmatrix():
    #### id is static for now need to change afterwards to make dashboard generic
    correlation_mat(id,1,"static/js/corrPearMappedNew2.csv")
    correlation_mat(id,0,"static/js/corrSpearMappedNew2.csv")
    return render_template('correlationmx.html')


@app.route('/confusionmatrix')
def confmatrix():
    tp,fp,fn,tn,accuracy,precision,recall = confusion_metrix(id)
    return render_template('confusionmatrix.html',tp = tp,fp = fp,fn = fn,tn = tn,accuracy = accuracy,precision = precision,recall = recall)


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
    
    model_data = get_data_by_id(id)
    file = model_data[4]
    df = pd.read_csv(file)
    alert_flag = model_data[9]
    escalation_flag= model_data[11]
    column = get_column_header(id)
    feature_count = get_feature_count(id)
    new_columns = []
    if b['f0'] == True:
        j = 0
        for k in range(0, len(b) - 1):
            new_columns.append(column[j])
        j = j + 1
    else:
        for i in range(1, feature_count + 1):
            name = "f" + str(i) 
            if b[name] == True:
                new_columns.append(column[i-1])

    df_alerts = df[df[alert_flag] == 1]
    df_nonalerts = df[df[alert_flag] == 0]
    df_escalations = df[df[escalation_flag] == 1]
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