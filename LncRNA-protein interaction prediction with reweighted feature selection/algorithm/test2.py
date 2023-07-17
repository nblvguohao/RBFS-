#-*- codeing=utf-8 -*-
#@Time:2022/2/19 15:55
#@Author:lvghuohao
#@File:test2.py
#@software:PyCharm
import os
import pandas as pd
import numpy as np
# -*- coding: utf-8 -*-

class Vertex:
    def __init__(self, id):
        self.id = id
        self.connect_to = {}

    def add_neighbor(self, nbr_id, weight=0):
        self.connect_to[nbr_id] = weight

    def get_connections(self):
        return self.connect_to.keys()

    def get_id(self):
        return self.id

    def get_weight(self, nbr_id):
        return self.connect_to[nbr_id]

    def __str__(self):
        return str(self.id) + ' connect to ' + str([x.id for x in self.connect_to])


class Graph:
    def __init__(self):
        self.vert_list = {}
        self.num_vertices = 0

    def add_vertex(self, id):
        self.num_vertices += 1
        new_vert = Vertex(id)
        self.vert_list[id] = new_vert
        return new_vert

    def get_vertex(self, id):
        if id in self.vert_list:
            return self.vert_list[id]
        else:
            return None

    def add_edge(self, from_, to, weight=0):
        if from_ not in self.vert_list:
            new_vertex = self.add_vertex(from_)
        if to not in self.vert_list:
            new_vertex = self.add_vertex(to)

        self.vert_list[from_].add_neighbor(self.vert_list[to], weight)

    def get_all_vertices(self):
        return self.vert_list.keys()

    def __contains__(self, id):
        return id in self.vert_list

    def __iter__(self):
        return iter(self.vert_list.values())

    def dfs_traverse(self, graph, start_node):
        """深度优先访问 栈实现 filo, 回溯
        :param graph:
        :param start_node:
        :return:
        """
        stack = [start_node]
        visited = set()  # 看是否访问过
        visited.add(start_node)
        while len(stack) > 0:
            # 拿出邻接点
            vertex = stack.pop()  # 这里pop参数没有0了，最后一个元素
            nodes = graph[vertex]
            for next_node in nodes:
                if next_node not in visited:  # 如何判断是否访问过，使用一个数组
                    stack.append(next_node)
                    visited.add(next_node)
            print(vertex)




if __name__ == "__main__":
    path = os.path.join(r'C:\Users\123\Desktop\lvguohao\data\dataset\finalPPIWeight.xlsx')
    data = pd.read_excel(path)
    proteinData = (np.array(data)).tolist()
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
        if item[2] != 0.0 and item[2] != 0:
            sumWeight += item[2]
            edge += 1
    averageWeight = sumWeight / edge
    g = Graph()
    print(g)
    for i in range(protein_arr.__len__()):
        g.add_vertex(i)
    print(g.vert_list)
    for item in proteinData:
        if item[0].__len__() > 1:
            g.add_edge(item[0],item[1],weight=item[2])
    print(g.get_all_vertices())
    print(g.vert_list[0])
    g.dfs_traverse('YGL058W')
    # for i in range(6):
    #     print(g.vert_list[i])
    # for v in g:
    #     print('v=', v)
    #     for w in v.get_connections():
    #         print('w=', w)
    #         print("({},{})".format(v.get_id(), w.get_id()))

