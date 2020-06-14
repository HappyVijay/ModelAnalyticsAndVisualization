from flask import *  
import sqlite3
from datetime import datetime
import os 
import pandas as pd
import sklearn 
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import seaborn as sn
import csv  
from flask import jsonify

#returns whole data of id from database
def get_data_by_id(id):
	con = sqlite3.connect("Model.db")
	c = con.cursor() 
	c.execute("SELECT * FROM Models WHERE id = ?", (id,))
	data = c.fetchall()[0]
	con.close()
	return(data)

#returns all the rows from database
def get_all_rows():#testing done
     with sqlite3.connect("Model.db") as con:
            cur = con.cursor()
            con.row_factory = sqlite3.Row
            cur.execute("select * from Models")
            rows = cur.fetchall()

            return(rows)

#Inserts data in the database with the autogenerated id and other values related to popup are none
#date is the date when the data has inserted
def insertdata(modelName,modelDesc,user,modelFile): #testing done
	con = sqlite3.connect("Model.db")
	c = con.cursor()
	c.execute("""INSERT INTO Models(modelName,modelDesc,user,modelFile,date) 
		VALUES
		(?,?,?,?,DATE('now'))""",(modelName,modelDesc,user,modelFile))
	con.commit()
	con.close()

#NOTE____________features shound be the in the  , seperated string without any excessive spaces
def updatedata(features,Score, status,alerts,bunessAction,escalation,id):#testing done
	con = sqlite3.connect("Model.db")
	c = con.cursor()

	#id = c.execute("select id from Models where id = (select max(id) from Models)").fetchall()[0][0] this will be useful if popup occurs at add model time
	c.execute("""UPDATE Models SET features = ?,
	Score = ?,
	status = ?,
	alerts = ?,
	bunessAction = ?,
	escalation =? WHERE id = ?""",(features,Score, status,alerts,bunessAction,escalation,id))
	con.commit()
	con.close()

#mean, Q1, median, Q3, interQuantileRange, min, max,STD = statistics_of_feature(df[columns[0]])//data for value of column
#and returns data in below order
#reurns mean, Q1, median, Q3, interQuantileRange, min, max,STD,MAD
def statistics_of_all_feature(id):
	data = get_data_by_id(id)
	features = data[6]
	file = data[4]
	features.replace(" ", "")
	features = features.split(',')
	up_feature = []
	for fat in features:
		if(fat != ""):
			up_feature.append(fat)
	features = up_feature
	statistics = []
	df = pd.read_csv(file)
	f= open("statistics_of_all_feature.csv","w+")
	f.write("mean, Q1, median, Q3, interQuantileRange, min, max,STD,MAD\n")
	for fname in features:
		data = df[fname]
		data = pd.DataFrame(data)
		mean = data.mean()
		q1 = data.quantile(0.25)

		median = data.quantile(0.5)
		q3 = data.quantile(0.75)
		interQuantileRange = q3 - q1
		min = data.min()
		max = data.max()
		STD = data.std()
		MAD = data.mad()

		#statistics.append((mean[0],q1[0],median[0], q3[0],interQuantileRange[0], min[0],max[0],STD[0],MAD[0]))
		statistics.append((mean[0],q1[0],median[0], q3[0],interQuantileRange[0], min[0],max[0],STD[0],MAD[0]))
		f.write(str(mean[0])+","+ str(q1[0]) + "," + str(median[0]) + "," +str(q3[0]) + "," + str(interQuantileRange[0]) + "," +str(min[0]) + "," + str(max[0]) + "," + str(STD[0]) + "," +str(MAD[0])+"\n")
	f.close()
	return(statistics)

#Number of total cases per surveillance scenario
#Number of Alerts per surveillance scenario
#non alerts per surveillance scenari
#Number of Escalations per surveillance scenario
#Number of Alerts vs Overall
def common_calculations(id):#testing done
	#total cases per surveillance
	data = get_data_by_id(id)
	alert_flag = data[9]
	escalation_flag= data[11]
	file = data[4]
	df = pd.read_csv(file)
	total_cases_surv = len(df.index)
	#alerts per surveillance scenario
	alert_per_surv =df[df[alert_flag] == 1].shape[0]
	#nonalerts per surveillance scenario
	nonalert_per_surv =df[df[alert_flag] == 0].shape[0]
	#escalations per surveillance scenario
	escalations_per_surv = df[df[escalation_flag] == 1].shape[0]
	return (total_cases_surv,alert_per_surv,nonalert_per_surv,escalations_per_surv)

#Number of Alerts per business reviews
#It returns business review and their frequncies respectively
def alerts_per_business_review(id):#testing done
	data = get_data_by_id(id)
	status = data[8]
	alert_flag = data[9]
	file = data[4]
	df = pd.read_csv(file)
	df = df[df[alert_flag] == 1]
	df[status] = df[status].fillna('BLANKS')
	business_reviews = df[status].unique() 
	alerts_per_business_review = [] 
	business_review = []
	frequency = []
	i = 0
	for review in business_reviews:

	    alerts_per_business_review.append([business_reviews[i],df[df[status] == business_reviews[i]].shape[0]])
	    business_review.append(business_reviews[i])
	    frequency.append(df[df[status] == business_reviews[i]].shape[0])
	    i = i+1
	records = zip(business_review,frequency)
	f= open("business_review.csv","w+")
	f.write("business_review,frequency\n")
	for i in records:
		abc,xyx =i
		f.write(str(abc)+","+str(xyx)+"\n")
	f.close()
	reviews = list(zip(business_review,frequency))
	return(reviews)

#this function returns the feature importance
#flag = 1 is has_alerted
#flag = 0 for escalations
def feature_imp(id,flag):#testing done
	data = get_data_by_id(id)
	status = data[8]
	if (flag == 1):
		y_flag = data[9]
	else:
		y_flag = data[11]
	file = data[4]
	features = data[6]
	features.replace(" ", "")
	features = features.split(',')

	up_feature = []
	for fat in features:
		if(fat != ""):
			up_feature.append(fat)
	features = up_feature

	dataset = df = pd.read_csv(file)
	X = df.loc[:, df.columns.isin(features)].values
	y = dataset.iloc[:, dataset.columns.get_loc(y_flag)].values #for the has alerted column 
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
	sc = StandardScaler()
	X_train = sc.fit_transform(X_train)
	X_test = sc.transform(X_test)
	model = RandomForestClassifier(n_estimators=20, random_state=0)
	model.fit(X_train, y_train)
	importances = model.feature_importances_
	feature_importances_matrix = list(zip(features,importances))
	return(feature_importances_matrix)
"""
	f= open("feature_imp_escalations.csv","w+")
	f.write("features,importances\n")
	for i in feature_importances_matrix:
		abc,xyx =i
		f.write(str(abc)+","+str(xyx)+"\n")
	f.close()
	
"""


#correlation matrix
#flag =1 is pearson 
#flag = 0 is spearman
def correlation_mat(id, flag): #testing done
	data = get_data_by_id(id)
	file = data[4]
	features = data[6]
	features.replace(" ", "")
	features = features.split(',')
	up_feature = []
	for fat in features:
		if(fat != ""):
			up_feature.append(fat)
	features = up_feature
	if (flag == 1):
		mthd = "pearson"
	else:
		mthd = "spearman"
	data = pd.read_csv(file)
	df = pd.DataFrame(data,columns = features)
	corrMatrix = df.corr(method=mthd)
	return corrMatrix


#returns confusion matrix,precision, recall, accuracy 
def confusion_metrix(id):#testing done
	data = get_data_by_id(id)
	file = data[4]
	alert_flag = data[9]
	escalation_flag = data[11]
	df = pd.read_csv(file)

	df = df[df[alert_flag] == 1]
	df = df[df[escalation_flag] == 1]
	tp = len(df.index)

	df = pd.read_csv(file)
	df = df[df[alert_flag] == 1]
	df = df[df[escalation_flag] == 0]
	fn = len(df.index)

	df = pd.read_csv(file)
	df = df[df[alert_flag] == 0]
	df = df[df[escalation_flag] == 1]
	fp = len(df.index)

	df = pd.read_csv(file)
	df = df[df[alert_flag] == 0]
	df = df[df[escalation_flag] == 0]
	tn = len(df.index)
	total = tp+fp+fn+tn
	matrix = [tp,fp,fn,tn]
	accuracy = (tp+tn) /total
	precision = (tp) /(tp+fp)
	recall = tp /(tp+fn)
	accuracy = accuracy*100
	precision = precision*100
	recall = recall*100
	return(matrix,accuracy,precision,recall)
	
#function to return alerts and non alerts depending upon cut-off
def alerts_non_alerts_cutoff(id, cut_off):#testing done
	data = get_data_by_id(id)
	score = data[7]
	file = data[4]
	df = pd.read_csv(file)
	alerts = df[df[score] >= cut_off]
	alerts = len(alerts.index)
	print(alerts)
	nonalerts = df[df[score] < cut_off]
	nonalerts = len(nonalerts.index)
	print(nonalerts)
	return(alerts,nonalerts)


