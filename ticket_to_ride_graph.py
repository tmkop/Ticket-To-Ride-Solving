import pandas as pd
from functools import reduce
import math


graphData = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vR_TL-7HnI6h_oTnl2EbSp96cL1qa_M_p-ahLoEIGbGcwSnAT3f5irxyl93IBpHOta7Jr9VLWAzMKmt/pub?gid=1528367842&single=true&output=csv')

destinations = pd.DataFrame({'City':list(set([*graphData['Point A'],*graphData['Point B']]))})

DOUBLE_TRACK = True

for i,edge in graphData.iterrows():
    point_a = destinations[destinations['City'] == edge['Point A']].index.tolist()[0]
    point_b = destinations[destinations['City'] == edge['Point B']].index.tolist()[0]
    
shortestDF = pd.DataFrame(columns=["Point A","Point B","Path"])

def findpath(a,b):
    dks = pd.DataFrame(index=destinations['City'],columns=['distance','connection'])
    dks['visited'] = False
    
    dks.at[destinations.at[a,'City'],'distance'] = 0
    dks.at[destinations.at[a,'City'],'connection'] = "START"
    #while at least one node is unvisited
    while not reduce(lambda acc, val: acc and val, list(dks['visited']),True):
        #finds the lowest distance non-visited city
        visiting_destination = dks[dks['visited'] == False].sort_values(by=['distance']).index[0]
        
        #iterate over the edges connecting to chosen city
        edges = graphData[(graphData["Point A"] == visiting_destination) | (graphData["Point B"] == visiting_destination)]
        for idx,edge in edges.iterrows():
            o_city = edge["Point B"] if edge["Point A"] == visiting_destination else edge["Point A"]
            if((dks.loc[o_city,'distance'] > dks.loc[visiting_destination,'distance']+edge['Edge Length']) or math.isnan(dks.loc[o_city,'distance'])):
                dks.loc[o_city,'distance'] = dks.loc[visiting_destination,'distance']+edge['Edge Length']
                dks.loc[o_city,'connection'] = visiting_destination

        dks.loc[visiting_destination,'visited'] = True
        pass
    
    
    del dks['visited']
    print(dks)
    
findpath(0,10)

for a in range(len(graphData)):
    for b in range(len(graphData)-a-1):
        # findpath(a,b+a+1)
        pass
    