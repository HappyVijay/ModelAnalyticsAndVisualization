
from flask import Flask, jsonify, render_template, request
from stats import *
app = Flask(__name__)
# POST to get data from frontend to backend
# GET to send data from backend to frontend


@app.route('/getallrows')
def getallrows():
    rows = get_all_rows()
    return jsonify(rows)

# each list contains mean, Q1, median, Q3, interQuantileRange, min, max,STD for respective features


@app.route('/statistics_of_feature')  # ,methods =['POST', 'GET'])
def statisticsoffalleature():
    statistics = statistics_of_feature(1)
    return jsonify(statistics)


# Number of total cases per surveillance scenario
# Number of Alerts per surveillance scenario
# non alerts per surveillance scenari
# Number of Escalations per surveillance scenario
# Number of Alerts vs Overall is the ratio of first two so not calculated

@app.route('/common_calculations')  # ,methods =['POST', 'GET'])
def commoncalculations():
    data = common_calculations(1)
    return jsonify(data)


#returns (business_review, alerts_for_respective_review)
@app.route('/alerts_per_business_review')  # ,methods =['POST', 'GET'])
def alertsperbusinessreview():
    data = alerts_per_business_review(1)
    return jsonify(data)


# returns feature importance related to alerts and escalations respectively
# feature importance is in form of (feature, relative importance)
@app.route('/feature_importance')  # ,methods =['POST', 'GET'])
def featureimp():
    alert_related = feature_imp(1, 1)  # flag = 1 is has_alerted
    escalation_related = feature_imp(1, 0)
    return jsonify(alert_related, escalation_related)

# returns pearson and spearman matrix respectively and matrix are json file
# please make efforts to use returned data before use


@app.route('/correlation_mat')  # ,methods =['POST', 'GET'])
def correlationmat():
    pearsonmat = correlation_mat(1, 1)  # 1 for
    spearmanmat = correlation_mat(1, 0)  # 0 for
    pearsonmat = pearsonmat.to_json()
    spearmanmat = spearmanmat.to_json()

    return jsonify(pearsonmat, spearmanmat)

# returns matrix = [tp,fp,fn,tn], accuracy,precision,recall)


@app.route('/confusion_metrix')  # ,methods =['POST', 'GET'])
def confusionmetrix():
    data = confusion_metrix(1)  # flag = 1 is has_alerted
    return jsonify(data)

# alerts and non alerts respectively


@app.route('/alerts_non_alerts_cutoff')  # ,methods =['POST', 'GET'])
def alertsnonalertscutoff():
    data = alerts_non_alerts_cutoff(1, 50)  # flag = 1 is has_alerted
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
