#-*- codeing=utf-8 -*-
#@Time:2022/1/11 9:09
#@Author:lvguohao
#@File:test2.py
#@software:PyCharm
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import xlsxwriter

if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    #根据官方数据构建网络
    path1 = os.path.join(parent_path,r'data\uploads\DIPYeastProteinData.xlsx')
    path2 = os.path.join(parent_path, r'data\uploads\DIPYeastInteraction.xlsx')
    data = pd.read_excel(path1)
    data2 = pd.read_excel(path2)
    proteinData = (np.array(data)).tolist()
    proteinEdges = (np.array(data2)).tolist()
    #根据蛋白质结构域信息构建网络
    path3 = os.path.join(parent_path, r'data\dataset\yeastDomain.xlsx')
    data3 = pd.read_excel(path3)
    proteinData3 = (np.array(data3)).tolist()
    G2 = nx.Graph()
    # for item in proteinData3:
    #     G2.add_node(item[0])
    # print(proteinEdges)
    # print("--------------------------------------")
    edge_list = []
    for item in proteinData3:
        for item1 in proteinData3:
            edge_array = []
            edge_array1 = []
            if item1[0] != item[0]:
                edge_array.append(item1[0])
                edge_array.append(item[0])
                edge_array1.append(item[0])
                edge_array1.append(item1[0])
                if edge_array in proteinEdges or edge_array1 in proteinEdges:
                    if edge_array1 not in edge_list and edge_array not in edge_list:
                        if edge_array in proteinEdges:
                            edge_list.append(edge_array)
                        if edge_array1 in proteinEdges:
                            edge_list.append(edge_array1)
    print(edge_list)
    print(edge_list.__len__())
    print("两个网络的分割线----------------------------------------------------------")
    workbook = xlsxwriter.Workbook('C:\\Users\\123\\Desktop\\lvguohao\\data\\dataset\\yeastDomain_List.xlsx')
    worksheet = workbook.add_worksheet()
    # 设定格式，等号左边格式名称自定义，字典中格式为指定选项
    # bold：加粗，num_format:数字格式
    bold_format = workbook.add_format({'bold': True})
    # 将二行二列设置宽度为15(从0开始)
    worksheet.set_column(1, 1, 15)
    # 用符号标记位置，例如：A列1行
    worksheet.write('A1', 'protein', bold_format)
    worksheet.write('B1', 'neighbor', bold_format)
    row = 1
    col = 0
    for item in (edge_list):
        worksheet.write_string(row, col, item[0])
        worksheet.write_string(row, col + 1, item[1])
        row += 1
    workbook.close()