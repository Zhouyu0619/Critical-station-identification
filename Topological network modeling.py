from sklearn.datasets import make_blobs
from matplotlib import pyplot
import numpy as np
import pandas as pd
import random

#调色盘
import seaborn as sns
#current_pale=sns.color_palette()
#sns.palplot(current_pale)
## 可以显示配色

colors_use=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#bcbd22', '#17becf', '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#bec1d4', '#bb7784', '#0000ff', '#111010', '#FFFF00',   '#1f77b4', '#800080', '#959595', 
 '#7d87b9', '#bec1d4', '#d6bcc0', '#bb7784', '#8e063b', '#4a6fe3', '#8595e1', '#b5bbe3', '#e6afb9', '#e07b91', '#d33f6a', '#11c638', '#8dd593', '#c6dec7', '#ead3c6', '#f0b98d', '#ef9708', '#0fcfc0', '#9cded6', '#d5eae7', '#f3e1eb', '#f6c4e1', '#f79cd4']
sns.palplot(colors_use)
#sns.palplot([colors_use[0]])# 仅显示第一个颜色

#读取地铁站点信息
station = pd.read_csv('station.csv')
station.drop(['Unnamed: 0','起点纬度','起点经度','终点纬度','终点经度'],axis = 1,inplace = True)

#获取节点坐标信息
pos = {}
for i in range(len(set(station['地铁点']))):
    pos[i] = (station.iloc[list(station['点编号']).index(i)][4],station.iloc[list(station['点编号']).index(i)][3])

#无向图绘画dom
road = nw.Graph()
H = nw.path_graph(len(set(station['地铁点'])))
road.add_nodes_from(H)
#线路路段集合
edgelist = [[] for i in range(15)]
flg = 0#线路标记
for i in range(len(station)-1):
    if station.iloc[i][0]==station.iloc[i+1][0]:
        if i!=269 and i!=301:#两叉路去除
            edgelist[flg].append((station.iloc[i][1],station.iloc[i+1][1]))
            road.add_edge(station.iloc[i][1],station.iloc[i+1][1])
    else:
        if i == 112:#四号线环路连接首尾
            edgelist[flg].append((152,202))
            road.add_edge(152,202)
        flg += 1
plt.figure(figsize=(8, 6))
for i in range(14):
    nw.draw_networkx_edges(
        road,
        pos,
        edgelist=edgelist[i],
        width=3,
        alpha=1,
        edge_color=colors_use[i],
        label='line'+str(i+1),
    )
plt.legend(loc='upper right', handlelength=3, borderpad=0.5, labelspacing=0.01)   
nw.draw(road,pos, font_weight='bold',width=0.1,node_size = 1)
plt.tight_layout()
plt.show()