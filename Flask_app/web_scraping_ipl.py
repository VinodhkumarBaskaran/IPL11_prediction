# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 14:20:33 2020

@author: vinodhkumarb
"""

import requests 
from bs4 import BeautifulSoup 
from timeit import timeit
import numpy as np
import random
import pandas as pd
# import numpy as np
# URL = "https://www.espncricinfo.com/ci/content/squad/index.html?object=1210595"
# r = requests.get(URL) 

# soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib 



def scraping_fun(URL):
    
    r = requests.get(URL) 

    soup = BeautifulSoup(r.content, 'html5lib')
    
    
    
    ipl_team=['Chennai Super Kings (2020/21)','Delhi Capitals Squad','Kings XI Punjab Squad','Kolkata Knight Riders Squad',
          'Mumbai Indians Squad','Rajasthan Royals Squad','Royal Challengers Bangalore Squad','Sunrisers Hyderabad Squad']
    
    a_tag=soup.find_all('a')
    
    dictx={}
    team=[]
    url=[]
    for a in a_tag:
        if a.text in ipl_team:
            team.append(a.text)
            url.append(a['href'])
    dictx={'team':team,'Squad':url}
    
    Ipl_squad_url=pd.DataFrame.from_dict(dictx)
    
    Ipl_squad_url['team']=np.where(Ipl_squad_url['team']=='Chennai Super Kings (2020/21)','Chennai Super Kings',Ipl_squad_url['team'])
    Ipl_squad_url['team']=np.where(Ipl_squad_url['team']=='Delhi Capitals Squad','Delhi Capitals',Ipl_squad_url['team'])
    Ipl_squad_url['team']=np.where(Ipl_squad_url['team']=='Kings XI Punjab Squad','Kings XI Punjab',Ipl_squad_url['team'])
    Ipl_squad_url['team']=np.where(Ipl_squad_url['team']=='Kolkata Knight Riders Squad','Kolkata Knight Riders',Ipl_squad_url['team'])
    Ipl_squad_url['team']=np.where(Ipl_squad_url['team']=='Mumbai Indians Squad','Mumbai Indians',Ipl_squad_url['team'])
    Ipl_squad_url['team']=np.where(Ipl_squad_url['team']=='Rajasthan Royals Squad','Rajasthan Royals',Ipl_squad_url['team'])
    Ipl_squad_url['team']=np.where(Ipl_squad_url['team']=='Royal Challengers Bangalore Squad','Royal Challengers Bangalore',Ipl_squad_url['team'])
    Ipl_squad_url['team']=np.where(Ipl_squad_url['team']=='Sunrisers Hyderabad Squad','Sunrisers Hyderabad ',Ipl_squad_url['team'])
    
    Ipl_squad_url['team']=Ipl_squad_url['team'].str.lower().str.strip()
    
    return Ipl_squad_url



def squad_looping(team,df):
    url=df[df['team'] == team.lower()]['Squad']
    return url.values[0]


def team_URL(team_name,df):
    URL = "https://www.espncricinfo.com/"+squad_looping(team_name,df)
    return URL



def team_details_scraping(URL):
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib') 
    
    player_name=soup.find_all('div',{"class": "large-13 medium-13 small-13 columns"})
    
    player_name_no_img=soup.find_all('div',{"class": "large-13 medium-13 small-20 columns"})
    
    name=[]
    player_status=[]
    player_stat=[]
    for player in player_name:
        name.append(player.a.text.strip()) #player.h3.text
        player_stat.append("https://www.espncricinfo.com/"+ player.h3.a['href'])
        try:
            player_status.append(player.h3.span.text)
        except:
            player_status.append('Indian player')
    for player in player_name_no_img:
        name.append(player.a.text.strip()) #player.h3.text
        player_stat.append("https://www.espncricinfo.com"+ player.h3.a['href'])
        try:
            player_status.append(player.h3.span.text)
        except:
            player_status.append('Indian player')
            
    team_list=pd.DataFrame({'name':name,'player_status':player_status,'player_stat':player_stat})
    
    country=[]
    age=[]
    Major_team_played=[]

    for i in team_list['player_stat']:
        URL = i
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib') 
        nation=soup.find_all('b')
        country.append(nation[0].text)

        ages=soup.find_all("p",{"class":"ciPlayerinformationtxt"})
        age.append(int(ages[2].span.text.split()[0]))

        Major_team_played.append(ages[3].span.text[:-1])


    #     print(nation[0].text)

    team_list['country']=country
    team_list['Age']=age
    team_list['Major_team']=Major_team_played
    
    
    team_list['uncapped']=np.where((team_list['Major_team']!='India') & (team_list['player_status']=='Indian player'), 'Yes','No')
    
    Specialist=[]
    Batting_style=[]
    Bowling_style=[]

    for i in team_list['player_stat']:
        URL = i
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib') 
        ages=soup.find_all("p",{"class":"ciPlayerinformationtxt"})

        if ages[4].span.text in ['Wicketkeeper batsman','Wicketkeeper','Top-order batsman','Batsman','Bowler','Allrounder','Batting allrounder','Bowling allrounder','Opening batsman','Middle-order batsman']:
    #         print (ages[0].span.text)
            Specialist.append(ages[4].span.text)
            Batting_style.append(ages[5].span.text)
            try:
                Bowling_style.append(ages[6].span.text)
            except:
                Bowling_style.append("No bowling")

        else :
            if ages[5].span.text in ['Wicketkeeper batsman','Wicketkeeper','Top-order batsman','Batsman','Bowler','Allrounder','Batting allrounder','Bowling allrounder','Opening batsman','Middle-order batsman']:
    #             print (ages[0].span.text)
                Specialist.append(ages[5].span.text)
                Batting_style.append(ages[6].span.text)
                try:
                    Bowling_style.append(ages[7].span.text)
                except:
                    Bowling_style.append("No bowling")
                    
    Mat_FC=[]
    Runs_FC=[]
    HS_FC=[]
    Bat_avg_FC=[]
    Bat_SR_FC=[]
    Wkts_FC=[]
    Bowl_Ave_FC=[]
    Econ_FC=[]
    Bowl_SR_FC=[]

    Mat_in=[]
    Runs_in=[]
    HS_in=[]
    Bat_avg_in=[]
    Bat_SR_in=[]
    Wkts_in=[]
    Bowl_Ave_in=[]
    Econ_in=[]
    Bowl_SR_in=[]
    Played_int=[]

    for i in team_list['player_stat']:

        try:
            print(i)
            perf=pd.read_html(i)

        except:

            Mat_FC.append(0)
            Runs_FC.append(0)
            HS_FC.append(0)
            Bat_avg_FC.append(0)
            Bat_SR_FC.append(0)
            Wkts_FC.append(0)
            Bowl_Ave_FC.append(0)
            Econ_FC.append(0)
            Bowl_SR_FC.append(0)

            Played_int.append('no')
            Mat_in.append(0)
            Runs_in.append(0)
            HS_in.append(0)
            Bat_avg_in.append(0)
            Bat_SR_in.append(0)
            Wkts_in.append(0)
            Bowl_Ave_in.append(0)
            Econ_in.append(0)
            Bowl_SR_in.append(0)

            continue

        Bat=perf[0][perf[0]['Unnamed: 0']=='T20s']
        Bowl=perf[1][perf[1]['Unnamed: 0']=='T20s']

        Bat_in=perf[0][perf[0]['Unnamed: 0']=='T20Is']
        Bowl_in=perf[1][perf[1]['Unnamed: 0']=='T20Is']

        if ((Bat.empty) & (Bat.empty) & (Bat.empty) & (Bat.empty)):
            Mat_FC.append(0)
            Runs_FC.append(0)
            HS_FC.append(0)
            Bat_avg_FC.append(0)
            Bat_SR_FC.append(0)
            Wkts_FC.append(0)
            Bowl_Ave_FC.append(0)
            Econ_FC.append(0)
            Bowl_SR_FC.append(0)

            Played_int.append('no')
            Mat_in.append(0)
            Runs_in.append(0)
            HS_in.append(0)
            Bat_avg_in.append(0)
            Bat_SR_in.append(0)
            Wkts_in.append(0)
            Bowl_Ave_in.append(0)
            Econ_in.append(0)
            Bowl_SR_in.append(0)


        else:
            Played_int.append('no')
            Mat_FC.append(Bat['Mat'].values[0])
            Runs_FC.append(Bat['Runs'].values[0])
            HS_FC.append(Bat['HS'].values[0])
            Bat_avg_FC.append(Bat['Ave'].values[0])
            Bat_SR_FC.append(Bat['SR'].values[0])
            Wkts_FC.append(Bowl['Wkts'].values[0])
            Bowl_Ave_FC.append(Bowl['Ave'].values[0])
            Econ_FC.append(Bowl['Econ'].values[0])
            Bowl_SR_FC.append(Bowl['SR'].values[0])

            try:
                Played_int.append('yes')
                Mat_in.append(Bat_in['Mat'].values[0])
                Runs_in.append(Bat_in['Runs'].values[0])
                HS_in.append(Bat_in['HS'].values[0])
                Bat_avg_in.append(Bat_in['Ave'].values[0])
                Bat_SR_in.append(Bat_in['SR'].values[0])
                Wkts_in.append(Bowl_in['Wkts'].values[0])
                Bowl_Ave_in.append(Bowl_in['Ave'].values[0])
                Econ_in.append(Bowl_in['Econ'].values[0])
                Bowl_SR_in.append(Bowl_in['SR'].values[0])

            except:
                Mat_in.append(0)
                Runs_in.append(0)
                HS_in.append(0)
                Bat_avg_in.append(0)
                Bat_SR_in.append(0)
                Wkts_in.append(0)
                Bowl_Ave_in.append(0)
                Econ_in.append(0)
                Bowl_SR_in.append(0)


    # team_list['Played_international']=Played_int
    team_list['Specialist']=Specialist
    team_list['Batting_style']=Batting_style
    team_list['Bowling_style']=Bowling_style

    # team_list['country']=country
    team_list['Mat_in']=Mat_in
    team_list['Runs_in']=Runs_in
    team_list['HS_in']=HS_in
    team_list['Bat_avg_in']=Bat_avg_in
    team_list['Bat_SR_in']=Bat_SR_in
    team_list['Wkts_in']=Wkts_in
    team_list['Bowl_Ave_in']=Bowl_Ave_in
    team_list['Econ_in']=Econ_in
    team_list['Bowl_SR_in']=Bowl_SR_in
    # team_list['Played_int']=Played_int
    team_list['Mat_FC']=Mat_FC
    team_list['Runs_FC']=Runs_FC
    team_list['HS_FC']=HS_FC
    team_list['Bat_avg_FC']=Bat_avg_FC
    team_list['Bat_SR_FC']=Bat_SR_FC
    team_list['Wkts_FC']=Wkts_FC
    team_list['Bowl_Ave_FC']=Bowl_Ave_FC
    team_list['Econ_FC']=Econ_FC
    team_list['Bowl_SR_FC']=Bowl_SR_FC

    team_list['Skill']=np.where(team_list['Specialist'].str.lower().str.contains('allrounder'),'Allrounder',team_list['Specialist'])
    team_list['Skill']=np.where((team_list['Specialist'].str.lower().str.contains('batsman')) & (~team_list['Specialist'].str.lower().str.contains('wicket')),'batsman',team_list['Skill'])

    team_list=team_list[team_list['player_status']!='withdrawn player']
    
    return team_list

#==================================
#Scraping initialization start here
#===================================

#### 
URL = "https://www.espncricinfo.com/ci/content/squad/index.html?object=1210595"
Ipl_squad_url=scraping_fun(URL)

'''
Please maintain the case sentivity and format as mentioned below while entering the input to team_URL()
========================================================================================================

#['chennai super kings', 'delhi capitals', 'kings xi punjab', 'kolkata knight riders', 'mumbai indians',
# 'rajasthan royals', 'royal challengers bangalore', 'sunrisers hyderabad']
'''


URL=team_URL('delhi capitals',Ipl_squad_url) ## 
team_list=team_details_scraping(URL)
#team_list.to_csv('dc.csv')

'''
Please maintain  the file naming style
=====================================

CSK ===> csk.csv
DC===> dc.csv
RCB===> rcb.csv
SRH===> srh.csv
RR===> rr.csv
KIXP===> kixp.csv
MI===> mi.csv
KKR===> kkr.csv

'''
