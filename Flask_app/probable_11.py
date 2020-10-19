# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 14:19:10 2020

@author: vinodhkumarb
"""

import pandas as pd
import numpy as np

def playing_11(team_list):
    
    
    player=[]
    role=[]


    batsman=0
    wk=0
    bowler=0
    allrounder=0



# segmenting 

    captain=team_list[team_list['player_status'].str.contains('captain')==True]
    uncapped=team_list[team_list['uncapped']=='Yes'].sample(n=1)
    
    print(captain['name'].values[0])
    if captain['country'].values[0]!='India':
        oversea=team_list[(team_list['country']!='India') & (team_list['name']!=captain['name'].values[0])].sample(n=3)
    else:
        oversea=team_list[team_list['country']!='India'].sample(n=4)

# Mandatory Captain select

    if "batsman" in captain['Specialist'].values[0].lower() and "wicketkeeper" not in captain['Specialist'].values[0].lower() and "allrounder" not in captain['Specialist'].values[0]:
        batsman+=1
        player.append(captain['name'].values[0] + " (c)")
        role.append(captain['Skill'].values[0])
        
    elif "wicketkeeper" in captain['Specialist'].values[0].lower():
        wk+=1
        player.append(captain['name'].values[0]+ " (c) & (wk)")
        role.append(captain['Skill'].values[0])
        
    elif "bowler" in captain['Specialist'].values[0].lower() and "allrounder" not in captain['Specialist'].values[0].lower():
        bowler+=1
        player.append(captain['name'].values[0] + " (c)")
        role.append(captain['Skill'].values[0])
        
    elif "allrounder" in captain['Specialist'].values[0].lower():
        allrounder+=1
        player.append(captain['name'].values[0] + " (c)")
        role.append(captain['Skill'].values[0])
        

# Selecting Uncap players

    if "batsman" in uncapped['Specialist'].values[0].lower() and "wicketkeeper" not in uncapped['Specialist'].values[0].lower() and "allrounder" not in uncapped['Specialist'].values[0].lower():
        batsman+=1
        player.append(uncapped['name'].values[0])
        role.append(uncapped['Skill'].values[0])
    elif "wicketkeeper" in uncapped['Specialist'].values[0].lower():
        wk+=1
        player.append(uncapped['name'].values[0])
        role.append(uncapped['Skill'].values[0])
    elif "bowler" in uncapped['Specialist'].values[0].lower() and "allrounder" not in uncapped['Specialist'].values[0].lower():
        bowler+=1
        player.append(uncapped['name'].values[0])
        role.append(uncapped['Skill'].values[0])
    elif "allrounder" in uncapped['Specialist'].values[0].lower():
        allrounder+=1
        player.append(uncapped['name'].values[0])
        role.append(uncapped['Skill'].values[0])

    for oversea_player in oversea['name'].to_list():
        temp=oversea[oversea['name']==oversea_player]

        if "batsman" in temp['Specialist'].values[0].lower() and "wicketkeeper" not in temp['Specialist'].values[0].lower() and "allrounder" not in temp['Specialist'].values[0].lower():
            batsman+=1
            player.append(temp['name'].values[0])
            role.append(temp['Skill'].values[0])
        elif "wicketkeeper" in temp['Specialist'].values[0].lower():
            wk+=1
            player.append(temp['name'].values[0])
            role.append(temp['Skill'].values[0])
        elif "bowler" in temp['Specialist'].values[0].lower() and "allrounder" not in temp['Specialist'].values[0].lower():
            bowler+=1
            player.append(temp['name'].values[0])
            role.append(temp['Skill'].values[0])
        elif "allrounder" in temp['Specialist'].values[0].lower():
            allrounder+=1
            player.append(temp['name'].values[0])
            role.append(temp['Skill'].values[0])
            
### Criteria for IPL team 
            
    constrain_batsman=4-batsman
    constrain_Allrounder=2-allrounder
    constrain_Bowler=4-bowler
    constrain_Wicketkeeper=1-wk

    if constrain_batsman<0:
        constrain_Allrounder=constrain_Allrounder-abs(constrain_batsman)
        constrain_batsman=0
    if constrain_Bowler<0:
        constrain_Allrounder=constrain_Allrounder-abs(constrain_Bowler)
        constrain_Bowler=0
    if constrain_Wicketkeeper<0:
        if constrain_batsman>0:
            constrain_batsman=constrain_batsman-abs(constrain_Wicketkeeper)
        else:
            constrain_Allrounder=constrain_Allrounder-abs(constrain_Wicketkeeper)
        constrain_Wicketkeeper=0   
    if constrain_Allrounder<0:
        constrain_Bowler=constrain_Bowler-abs(constrain_Allrounder)
        constrain_Allrounder
    
    
#### Batsman selection

    remaining_selection=team_list[(team_list['name'] != uncapped['name'].values[0]) & (team_list['name'] != captain['name'].values[0]) & (team_list['country'] == 'India')]
    batsman_selection=remaining_selection[remaining_selection['Skill'].str.lower()=='batsman']
    dictionary={'-':0}
    batsman_selection.replace(dictionary, regex=True, inplace=True)
    batsman_selection['Weighted_bat_score']=0.28 * batsman_selection['Bat_avg_in'].astype(float) + 0.42 * batsman_selection['Bat_SR_in'].astype(float) + 0.12 * batsman_selection['Bat_avg_FC'].astype(float) + 0.18 * batsman_selection['Bat_SR_FC'].astype(float)
    
    from itertools import combinations

    #Getting all combination of a particular length.
    combo = combinations(batsman_selection['Weighted_bat_score'].sort_values(ascending=False).to_list(),constrain_batsman)

    for x in combo:
        bat_player=[]
        bat_skills=[]
        print(x)
        for i in x:
            temp=batsman_selection[batsman_selection['Weighted_bat_score']==i]

            bat_player.append(temp['name'].values[0])
            bat_skills.append(temp['Skill'].values[0])
        if len(bat_player)==constrain_batsman:
            break

#     print(bat_player)
    player.extend(bat_player)
    role.extend(bat_skills)
    
    
### Allrounder 

    Allrounder_selection=remaining_selection[remaining_selection['Skill'].str.lower()=='allrounder']
    dictionary={'-':0}
    Allrounder_selection.replace(dictionary, regex=True, inplace=True)
    Allrounder_selection['Weighted_allrounder_score']= (50-(0.15 * Allrounder_selection['Econ_in'].astype(float) + 0.20 * Allrounder_selection['Bowl_SR_in'].astype(float) + 0.045 * Allrounder_selection['Econ_FC'].astype(float) + 0.105 * Allrounder_selection['Bowl_SR_FC'] .astype(float))) + 0.14 * Allrounder_selection['Bat_avg_in'].astype(float) + 0.21 * Allrounder_selection['Bat_SR_in'].astype(float) + 0.06 * Allrounder_selection['Bat_avg_FC'].astype(float) + 0.09 * Allrounder_selection['Bat_SR_FC'].astype(float)
    
    
    from itertools import combinations

    #Getting all combination of a particular length.
    combo = combinations(Allrounder_selection['Weighted_allrounder_score'].sort_values(ascending=False).to_list(),constrain_Allrounder)

    for x in combo:
        allr_player=[]
        allr_skills=[]
        print(x)
        for i in x:
            temp=Allrounder_selection[Allrounder_selection['Weighted_allrounder_score']==i]

            allr_player.append(temp['name'].values[0])
            allr_skills.append(temp['Skill'].values[0])
        if len(allr_player)==constrain_Allrounder:
            break
#     print(len(allr_player))
    player.extend(allr_player)
    role.extend(allr_skills)
    

### keeper

    wk_selection=remaining_selection[remaining_selection['Skill'].str.lower().str.contains('wicket')]
    dictionary={'-':0}
    wk_selection.replace(dictionary, regex=True, inplace=True)
    wk_selection['Weighted_bat_score']=0.28 * wk_selection['Bat_avg_in'].astype(float) + 0.42 * wk_selection['Bat_SR_in'].astype(float) + 0.12 * wk_selection['Bat_avg_FC'].astype(float) + 0.18 * wk_selection['Bat_SR_FC'].astype(float)

    
    from itertools import combinations

    #Getting all combination of a particular length.
    combo = combinations(wk_selection['Weighted_bat_score'].sort_values(ascending=False).to_list(),constrain_Wicketkeeper)

    for x in combo:
        wk_player=[]
        wk_skills=[]
        print(x)
        for i in x:
            temp=wk_selection[wk_selection['Weighted_bat_score']==i]

            wk_player.append(temp['name'].values[0])
            wk_skills.append(temp['Skill'].values[0])
        if len(allr_player)==constrain_Wicketkeeper:
            break
#     print(len(wk_player))
    player.extend(wk_player)
    role.extend(wk_skills)
    
    

### Bowler

    bowler_selection=remaining_selection[remaining_selection['Skill'].str.lower()=='bowler']
    dictionary={'-':0}
    bowler_selection.replace(dictionary, regex=True, inplace=True)
    bowler_selection['Weighted_bowl_score']= 100- (0.30 * bowler_selection['Econ_in'].astype(float) + 0.40 * bowler_selection['Bowl_SR_in'].astype(float).astype(float) + 0.09 * bowler_selection['Econ_FC'].astype(float) + 0.21 * bowler_selection['Bowl_SR_FC'] .astype(float))

    
    from itertools import combinations

    #Getting all combination of a particular length.
    combo = combinations(bowler_selection['Weighted_bowl_score'].sort_values(ascending=False).to_list(),constrain_Bowler)

    for x in combo:
        bowl_player=[]
        bowl_skills=[]
        for i in x:
            temp=bowler_selection[bowler_selection['Weighted_bowl_score']==i]

            bowl_player.append(temp['name'].values[0])
            bowl_skills.append(temp['Skill'].values[0])
        if len(bowl_player)==constrain_Bowler:
            break

    player.extend(bowl_player)
    role.extend(bowl_skills)
    
    

    return player,role