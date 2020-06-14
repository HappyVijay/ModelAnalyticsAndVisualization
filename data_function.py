from flask import Flask, request, redirect, url_for, render_template, jsonify
import json
import sqlite3
from werkzeug.utils import secure_filename
import pandas as pd


# app = Flask(__name__)


# @app.route("/get_data", methods=['POST', 'GET'])
#     a = request.args.get('a', type=dict)
#     b = request.args.get('b', type=dict)
a = {'All': False, 'non-alert': True, 'alert': False, 'escalations': False}
b = {'f0': False, 'f1': False, 'f2': True,
     'f3': False, 'f4': False, 'f5': False, 'f6': False}
df = pd.read_csv("EQWT_latest_data.csv")
column = list(df.columns)
new_columns = []
if b['f0'] == True:
    j = 0
    for k in range(0, len(b)):
        new_columns.append(column[j])
        j = j + 1
else:
    j = 1
    for keys in b:
        if b[keys] == True:
            new_columns.append(column[j])
        j = j + 1

df_alerts = df[df['has_alerted'] == 1]
df_nonalerts = df[df['has_alerted'] == 0]
df_escalations = df[df['has_escalated'] == 1]
result = {}
if a['All'] == True:
    for column in new_columns:
        result[column] = [list(df_nonalerts[column]), list(
            df_alerts[column]), list(df_escalations[column])]

else:
    for column in new_columns:
        result[column] = []
        for keys in a:
            if a[keys] == True:
                if keys == 'non-alert':
                    result[column].append(list(df_nonalerts[column]))
                if keys == 'alert':
                    result[column].append(list(df_alerts[column]))
                if keys == 'escalations':
                    result[column].append(list(df_escalations[column]))

            else:
                if keys == 'All':
                    continue()
                else:
                    result[column].append([])

print(result)
