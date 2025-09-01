import pandas as pd
from dijkstar import Graph, find_path

graphData = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vR_TL-7HnI6h_oTnl2EbSp96cL1qa_M_p-ahLoEIGbGcwSnAT3f5irxyl93IBpHOta7Jr9VLWAzMKmt/pub?gid=1528367842&single=true&output=csv')

destinations = pd.DataFrame({'City':list(set([*graphData['Point A'],*graphData['Point B']]))})

graph = Graph()

for i,edge in graphData.iterrows():
    point_a = destinations[destinations['City'] == edge['Point A']].index.tolist()[0]
    point_b = destinations[destinations['City'] == edge['Point B']].index.tolist()[0]
    graph.add_edge(point_a,point_b,edge["Edge Length"])
    
shortestDF = pd.DataFrame(columns=["Point A","Point B","Name Path","Distance Path"])

def findpath(a,b,dataset):
    start,stop = list(map(lambda station: destinations.iloc[station]["City"],[a,b]))
    print(f"Finding path from [{start}]({a}) to [{stop}]({b})")
    path = find_path(graph,a,b)
    name_path = (list(map(lambda station: destinations.iloc[station]["City"],path[0])))
    
    
    shortestDF.loc[len(shortestDF)] = [start,stop,name_path,path[2]]
    
for a in range(len(graphData)):
    for b in range(len(graphData)-a-1):
        findpath(a,b+a+1,shortestDF)