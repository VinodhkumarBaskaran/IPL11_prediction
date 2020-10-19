# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 14:06:10 2020

@author: vinodhkumarb
"""
from flask import Flask, request, jsonify, render_template
import os
import pandas as pd
import numpy as np
from  probable_11 import playing_11
from flask_cors import CORS, cross_origin
import warnings
warnings.filterwarnings("ignore")

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submitted", methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return render_template("index.html") 
    else:

        select = str(request.form.get('team'))
        
        if select=="CSK" :
        	team_list=pd.read_csv('csk.csv')
        elif select=="DC"  :
        	team_list=pd.read_csv('dc.csv')
        elif select=="KP"  :
        	team_list=pd.read_csv('kxip.csv')
        elif select=="KKR" :
        	team_list=pd.read_csv('kkr.csv')
        elif select=="MI"  :
        	team_list=pd.read_csv('mi.csv')
        elif select=="RR"  :
        	team_list=pd.read_csv('rr.csv')
        elif select=="RCB" :
        	team_list=pd.read_csv('rcb.csv')
        elif select=="SRH" :
        	team_list=pd.read_csv('srh.csv')

        else:
            return render_template("index.html") 
        try:
            player,role= playing_11(team_list)
        except:
            player,role= playing_11(team_list)
        _11={'Players':player,'Role':role}
        result=pd.DataFrame(_11)
        
        return render_template('index2.html', tables=[result.to_html(classes='data')], titles=result.columns.values) # just to see what select is


#port = int(os.getenv("PORT"))
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=port)
    app.run(port=5000, debug=False)





















