#-*- codeing=utf-8 -*-
#@Time:2022/2/19 16:31
#@Author:lvguohao
#@File:getEssentialProtein.py
#@software:PyCharm

import networkx as nx
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import xlsxwriter

class GraphTraverser(object):
    """图遍历器，基于networks展示图
    """
    def __init__(self):
        return

    def gen_graph(self, node_list=[], edge_list=[()]):
        """生成图, 返回一个图词典，用来存储图
        :param node_list:
        :param edge_list:
        :return:
        """
        graph = nx.MultiDiGraph()
        graph.add_nodes_from(node_list)
        # graph.add_edges_from(edge_list)
        for item in edge_list:
            graph.add_edge(item[0], item[1], weight=item[2])
        nx.draw(graph, with_labels=True)
        # plt.show()
        graph_dict = {}
        for node in node_list:
            graph_dict[node] = [next_node[1] for next_node in edge_list if next_node[0] == node]
        return graph_dict


    def bfs_traverse(self, graph, start_node):
        """广度优先遍历, 队列实现 fifo
        :param graph:
        :param start_node:
        :return:
        """
        queue = [start_node]
        visited = set()  # 看是否访问过该结点
        visited.add(start_node)
        while len(queue) > 0:
            vertex = queue.pop(0)  # 保存第一结点，并弹出，方便把他下面的子节点接入
            nodes = graph[vertex]  # 子节点的数组
            for next_node in nodes:
                if next_node not in visited:  # 判断是否访问过
                    queue.append(next_node)
                    visited.add(next_node)
            # print(vertex)

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
            # print(vertex)

def getEssentialProteinNumber(parent_path,times):
    path = os.path.join(r'C:\Users\123\Desktop\lvguohao\data\dataset\finalPPIWeight.xlsx')
    data = pd.read_excel(path)
    proteinData = (np.array(data)).tolist()
    protein_arr = []
    edges = []

    sumWeight = 0
    edge = 0

    for item in proteinData:
        if item[0] not in protein_arr:
            protein_arr.append(item[0])
        if item[1] not in protein_arr:
            protein_arr.append(item[1])
        if item[2] != 0.0 and item[2] != 0:
            sumWeight += item[2]
            edge += 1
        tup1 = (item[0], item[1], item[2])
        edges.append(tup1)
    averageWeight = sumWeight / edge
    # print("averageWeight:", averageWeight)
    # print(edges)
    graph = GraphTraverser()
    graph_dict = graph.gen_graph(protein_arr, edges)
    # print(graph_dict)

    g = nx.Graph()
    for item in protein_arr:
        g.add_node(item)
    list = []
    for item in proteinData:
        tup = (item[0], item[1], item[2])
        list.append(tup)
    g.add_weighted_edges_from(list)

    # 读取酵母的关键蛋白质集合
    path1 = os.path.join(parent_path, r'C:\Users\123\Desktop\lvguohao\数据集\酵母的关键蛋白质集合.xlsx')
    data1 = pd.read_excel(path1)
    essentialProtein = (np.array(data1)).tolist()

    # 第n（n > 1）次读取蛋白质已有的得分
    path2 = os.path.join(parent_path, r'C:\Users\123\Desktop\lvguohao\data\dataset\lastProteinScore.xlsx')
    data2 = pd.read_excel(path2)
    exist_protein_score = (np.array(data2)).tolist()
    # print('exist_protein_score长度:', exist_protein_score.__len__())

    # 第1次读取蛋白质已有的得分
    path3 = os.path.join(parent_path, r'C:\Users\123\Desktop\lvguohao\data\dataset\eachProteinDomainWeight.xlsx')
    data3 = pd.read_excel(path3)
    first_domain_score = (np.array(data3)).tolist()
    # print('first_domain_score长度:', first_domain_score.__len__())
    # print('first_domain_score:', first_domain_score)
    # print(essentialProtein)
    essential_arr = []
    for item in essentialProtein:
        essential_arr.append(item[0])

    result_dict = []
    for key, val in graph_dict.items():
        n = 0  # 该蛋白质所有的相互作用边的条数
        m = 0  # 其中大于平均相互作用边的条数
        protein = "'" + key + "'"
        n = val.__len__()
        protein_score = 0
        for item in val:
            if g[key][item]['weight'] > averageWeight:
                m += 1

        if exist_protein_score.__len__() == 0:  # 第一次执行蛋白质评分
            if n == 0 or m == 0:
                # protein_score = 0
                for item2 in first_domain_score:
                    if item2[0] == key:
                        protein_score = item2[5]
                        break
            else:
                for item2 in first_domain_score:
                    if item2[0] == key:
                        protein_score = m / n + item2[5]
                        break
        else:
            if n == 0 or m == 0:
                # protein_score = 0
                for item1 in exist_protein_score:
                    if item1[0] == key:
                        protein_score = item1[1]
                        break
            else:
                for item1 in exist_protein_score:
                    if item1[0] == key:
                        protein_score = item1[1] + m / n
                        break

        obj = (key, protein_score)
        result_dict.append(obj)
        # print(protein_score)
    # print(result_dict)
    # print("result_dict:",result_dict.__len__())
    mid_dict = []
    for item in result_dict:
        # if item[1] != 0:
        mid_dict.append(item)
    mid_dict = sorted(mid_dict, key=lambda h: h[1], reverse=True)
    result_arr = []
    for i in range(0, 255):
        result_arr.append(mid_dict[i][0])

    #判断前三百条相互作用中有多少个蛋白质
    # test = []
    # for item in result_arr:
    #     if item[]
    print(result_arr)

    # 把上一阶段排序的蛋白质得分记录下来
    workbook = xlsxwriter.Workbook('C:\\Users\\123\Desktop\\lvguohao\\data\\dataset\\lastProteinScore.xlsx')
    worksheet = workbook.add_worksheet()
    bold_format = workbook.add_format({'bold': True})
    worksheet.set_column(1, 1, 15)
    worksheet.write('A1', 'protein', bold_format)
    worksheet.write('B1', 'score', bold_format)
    row = 1
    col = 0
    for item in (mid_dict):
        worksheet.write_string(row, col, str(item[0]))
        worksheet.write_string(row, col + 1, str(item[1]))
        row += 1
    workbook.close()
    share_arr = [] #最终识别出的关键蛋白质数量
    for item in result_arr:
        if item in essential_arr:
            share_arr.append(item)
    # print(share_arr)
    print('第',times,'次循环识别出的关键蛋白值数量：',share_arr.__len__())

if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)

    for times in range(0,100):
        getEssentialProteinNumber(parent_path,times)


    # 读取酵母的关键蛋白质集合
    path1 = os.path.join(parent_path, r'C:\Users\123\Desktop\lvguohao\数据集\酵母的关键蛋白质集合.xlsx')
    data1 = pd.read_excel(path1)
    essentialProtein = (np.array(data1)).tolist()

    essential_arr = []
    for item in essentialProtein:
        if item[0] not in essentialProtein:
            essential_arr.append(item[0])



   




