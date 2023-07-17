#-*- codeing=utf-8 -*-
#@Time:2022/2/18 15:40
#@Author:lvguohao
#@File:getEssentialProteins.py
#@software:PyCharm
#获取关键蛋白质
import os
import pandas as pd
import numpy as np
import networkx as nx


#!/usr/bin/python
# -*- coding: UTF-8 -*-

class VertexNode(object):   #顶点表节点
    def __init__(self,vertexname,visited=False,p=None):
        self.vertexName =vertexname #节点名字
        self.Visited=visited        #此节点是否被访问过
        self.firstNode = p          #指向所连接的边表节点的指针（EdgeNode）

class EdgeNode(object):     #边表节点
    def __init__(self,index,weight,p=None):
        self.Index =index   #尾节点在边表中对应序号
        self.Weight=weight  #边的权值
        self.Next = p       #链接同一头节点的下一条边

class Adgraph(object):
    def __init__(self,vcount=0):
        self.vertexList = []   #用list链接边表
        self.vertexCount = vcount

    def initlist(self,data):    #初始化
        for da in data:
            A=VertexNode(da)
            self.vertexList.append(A)
        self.vertexCount=len(data)

    def GetIndex(self,data):    #获取指定名称的节点的序号
        for i in range(self.vertexCount):
            temp=self.vertexList[i].vertexName
            if (temp!=None)and(data == temp):
                return i
        return -1

    def AddEdge(self,startNode,endNode,weight): #添加边的信息
        i=self.GetIndex(startNode)
        j=self.GetIndex(endNode)
        if i==-1 or j==-1:
            print("不存在该边")
        else:
            weight=float(weight)
            temp=self.vertexList[i].firstNode
            if temp==None:  #若边表下无顶点信息
                self.vertexList[i].firstNode=EdgeNode(j,weight)
            else:   		#若边表下已有顶点信息
                while(temp.Next!=None):
                    temp=temp.Next
                temp.Next=EdgeNode(j,weight)



def getNetwork(parent_path):
    path = os.path.join(parent_path, r'data\dataset\finalPPIWeight.xlsx')
    data = pd.read_excel(path)
    proteinData = (np.array(data)).tolist()
    G = Adgraph()
    sumWeight = 0
    edge = 0
    protein_arr = []
    for item in proteinData:
        if item[0] not in protein_arr:
            # G.add_vertex(item[0])
            protein_arr.append(item[0])
        if item[1] not in protein_arr:
            # G.add_vertex(item[1])
            protein_arr.append(item[1])
        sumWeight += item[2]
        edge += 1
    averageWeight = sumWeight/edge
    G.initlist(protein_arr)#初始化所有节点
    G.AddEdge(item[0],item[1],averageWeight)
    # print(G.vert_list)

    # for item in proteinData:
    #     if item[0].__len__() > 1:
    #         G.add_edge(item[0],item[1],weight=item[2])
            # print(item)
    #根据网络图中每一个节点进行遍历（深度、广度）
    # elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > averageWeight]
    # print(elarge)
    # print(elarge.__len__())

    # G.add_nodes_from(protein_array)
    # G.add_edges_from(proteinEdges, weight=0)
    print("图已构成")
    return G

def DFS(self,i):    #深度优先搜索递归
    self.vertexList[i].Visited=True
    result=self.vertexList[i].vertexName+'\n'
    p=self.vertexList[i].firstNode
    while(p!=None):
        if self.vertexList[p.Index].Visited==True:
            p=p.Next
        else:
            result+=self.DFS(p.Index)
    return result

def DFStravel(self,start):  #深度优先搜索入口
    i=self.GetIndex(start)
    if i!=-1:
        for j in range(self.vertexCount):
            self.vertexList[j].Visited=False
        DFSresult=self.DFS(i)
    return DFSresult



if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    G = getNetwork(parent_path)
    DFStravel(G,'YKR024C')
