from flask import *  
import sqlite3    
con = sqlite3.connect("Model.db")  
print("Database opened successfully")  
con.execute("""CREATE TABLE IF NOT EXISTS Models (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	modelName TEXT NOT NULL,
	modelDesc TEXT ,
	user TEXT NOT NULL, 
	modelFile TEXT NOT NULL,
	date TEXT,
	features TEXT,
	Score TEXT,
	status TEXT,
	alerts TEXT,
	bunessAction TEXT,
	escalation TEXT)""")  
print("ModelTable created successfully")
con.commit()  
con.close()  



