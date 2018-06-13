from flask import Flask, render_template, request
import sqlite3 as sql
import pandas as pd
import time
app = Flask(__name__,template_folder="static")

#########################################################################################################################
@app.route('/')
def home():
   return render_template('home.html')
#=======================================================================================================================#

@app.route('/createtable', methods=['POST'])
def createtable():
   conn = sql.connect('Assign3.db')
   csvf = pd.read_csv("all_month.csv",encoding = "ISO-8859-1")
   start_time = time.time()
   # csvf[['date', 'time']] = csvf['time'].str.split('T', expand=True)
   # csvf['time'] = csvf['time'].str.split('.').str[0]
   csvf.to_sql('Census', conn, if_exists='replace', index=False)
   msg="Table created successfully"
   end_time = time.time()
   time_diff = end_time - start_time
   print(csvf)
   return render_template('home.html',msg=msg,timediff=time_diff)

#=======================================================================================================================#

@app.route('/Region', methods=['POST'])
def Region():
    Region = request.form['Region']
    con = sql.connect("Assign3.db")
    start_time = time.time()
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('SELECT REGION,DIVISION,STATE,STNAME,POPESTIMATE2001 FROM Census where REGION = ?', (Region,))
    rows = cur.fetchall()
    end_time = time.time()
    time_diff = end_time - start_time
    count = 0
    for row in rows:
        count = count + 1
        # magnitude.append("mag:" + row[0])

    return render_template('home.html', counter=count, rows=rows,timediff=time_diff)
#=======================================================================================================================#

if __name__ == '__main__':
   app.run(debug = True)