#-*- codeing=utf-8 -*-
#@Time:2022/3/1 10:36
#@Author:lvguohao
#@File:constructOriginalNetwork_MBD.py
#@software:PyCharm

import datetime
import time
import xlwt #需要的模块
import os
import pandas as pd
import numpy as np
import xlsxwriter
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import xlsxwriter
import math
def txt2xls(filename,xlsname):  #文本转换成xls的函数，filename 表示一个要被转换的txt文本，xlsname 表示转换后的文件名
    print('converting xls ... ')
    f = open(filename)   #打开txt文本进行读取
    x = 0                #在excel开始写的位置（y）
    y = 0                #在excel开始写的位置（x）
    xls=xlwt.Workbook()
    sheet = xls.add_sheet('sheet1',cell_overwrite_ok=True) #生成excel的方法，声明excel
    while True:  #循环，读取文本里面的所有内容
        line = f.readline() #一行一行读取
        if not line:  #如果没有内容，则退出循环
            break
        for i in line.split('\t'):#读取出相应的内容写到x
            item=i.strip()
            sheet.write(x,y,item)
            y += 1 #另起一列
        x += 1 #另起一行
        y = 0  #初始成第一列
    f.close()
    xls.save(xlsname+'.xls') #保存

#根据蛋白质相互作用网络导出蛋白质文件
def getProteinData(parent_path):
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    path = os.path.join(r'C:\Users\123\Desktop\lvguohao\data\dataset\MBD数据库中酵母相互作用.xls')
    data = pd.read_excel(path)
    proteinData = (np.array(data)).tolist()

    protein_arr = []
    for item in proteinData:
        if item[0] not in protein_arr:
            protein_arr.append(item[0])
        if item[1] not in protein_arr:
            protein_arr.append(item[1])

    workbook = xlsxwriter.Workbook('C:\\Users\\123\\Desktop\\lvguohao\\data\\dataset\\MBD数据库中蛋白质数据.xlsx')
    worksheet = workbook.add_worksheet()
    # 设定格式，等号左边格式名称自定义，字典中格式为指定选项
    # bold：加粗，num_format:数字格式
    bold_format = workbook.add_format({'bold': True})
    # 将二行二列设置宽度为15(从0开始)
    worksheet.set_column(1, 1, 15)
    # 用符号标记位置，例如：A列1行
    worksheet.write('A1', 'protein', bold_format)
    # worksheet.write('B1', 'neigbor', bold_format)
    # worksheet.write('C1', 'weight', bold_format)
    # worksheet.write('D1', 'SFD_NORMSVi', bold_format)
    # worksheet.write('E1', 'NDT_NORMSVi', bold_format)
    # worksheet.write('F1', 'PVi', bold_format)
    row = 1
    col = 0
    for item in (protein_arr):
        # 使用write_string方法，指定数据格式写入数据
        worksheet.write_string(row, col, str(item))
        # worksheet.write_string(row, col + 1, str(item['neigbor']))
        # worksheet.write_string(row, col + 2, str(item['weight']))
        # worksheet.write_string(row, col + 3, str(item['SFD_NORMSVi']))
        # worksheet.write_string(row, col + 4, str(item['NDT_NORMSVi']))
        # worksheet.write_string(row, col + 5, str(item['PVi']))
        row += 1
    workbook.close()

def constructNetwork(parent_path):
    #根据官方数据构建网络
    #根据DIP数据集构建的网络
    # path1 = os.path.join(parent_path,r'data\uploads\DIPYeastProteinData.xlsx')
    # path2 = os.path.join(parent_path, r'data\uploads\DIPYeastInteraction.xlsx')
    #根据MIPS数据集构建的网络
    # path1 = os.path.join(parent_path,r'data\dataset\MIPS数据库中蛋白质数据.xlsx')
    # path2 = os.path.join(parent_path, r'data\dataset\MIPS数据库中酵母相互作用.xls')
    # 根据MBD数据集构建的网络
    path1 = os.path.join(parent_path,r'data\dataset\MBD数据库中蛋白质数据.xlsx')
    path2 = os.path.join(parent_path, r'data\dataset\MBD数据库中酵母相互作用.xls')
    data = pd.read_excel(path1)
    data2 = pd.read_excel(path2)
    proteinData = (np.array(data)).tolist()
    proteinEdges = (np.array(data2)).tolist()
    # print(proteinEdges)
    # protein_array = []
    # for item in proteinData:
    #     if item[0].__len__() > 1:
    #         protein_array.append(item[0])
    #
    # G1 = nx.Graph()
    # G1.add_nodes_from(protein_array)
    # G1.add_edges_from(proteinEdges,weight = '0')
    # return G1

    #根据蛋白质结构域信息构建网络
    path3 = os.path.join(parent_path, r'data\dataset\yeastDomain.xlsx')
    data3 = pd.read_excel(path3)
    proteinData3 = (np.array(data3)).tolist()
    G2 = nx.Graph()
    for item in proteinData3:
        G2.add_node(item[0])
    print(proteinEdges)
    print("--------------------------------------")
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
    workbook = xlsxwriter.Workbook('C:\\Users\\123\\Desktop\\lvguohao\\data\\dataset\\yeastDomain_List_MBD.xlsx')
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

    #根据亚细胞定位信息构建网络
    path4 = os.path.join(parent_path, r'data\dataset\yeastSubcellularLocalization.xls')
    # path4 = os.path.join(parent_path, r'data\dataset\subcellularLocation_0302.xlsx')
    data4 = pd.read_excel(path4)
    proteinData4 = (np.array(data4)).tolist()
    G3 = nx.Graph()
    for item in proteinData4:
        G3.add_node(item[0])
    print(proteinEdges)
    print("--------------------------------------")
    edge_list2 = []
    for item in proteinData4:
        for item1 in proteinData4:
            edge_array = []
            edge_array1 = []
            if item1[0] != item[0]:
                item[0] = item[0].split("'")[0]
                item1[0] = item1[0].split("'")[0]
                edge_array.append(item1[0])
                edge_array.append(item[0])
                edge_array1.append(item[0])
                edge_array1.append(item1[0])
                if edge_array in proteinEdges or edge_array1 in proteinEdges:
                    if edge_array1 not in edge_list2 and edge_array not in edge_list2:
                        if edge_array in proteinEdges:
                            edge_list2.append(edge_array)
                        if edge_array1 in proteinEdges:
                            edge_list2.append(edge_array1)
    print(edge_list2)
    print(edge_list2.__len__())
    workbook = xlsxwriter.Workbook('C:\\Users\\123\\Desktop\\lvguohao\\data\\dataset\\yeastSubcellularLocalization_List_MBD.xlsx')
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
    for item in (edge_list2):
        worksheet.write_string(row, col, item[0])
        worksheet.write_string(row, col + 1, item[1])
        row += 1
    workbook.close()
    result_list = []
    for item in edge_list:
        if item in edge_list2:
            result_list.append(item)
    print("两个网络的交结果：",result_list)
    workbook = xlsxwriter.Workbook('C:\\Users\\123\\Desktop\\lvguohao\\data\\dataset\\result_List_MBD.xlsx')
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
    for item in (result_list):
        worksheet.write_string(row, col, item[0])
        worksheet.write_string(row, col + 1, item[1])
        row += 1
    workbook.close()

#根据所有节点构图
def getGraph(parent_path):
    # path1 = os.path.join(parent_path,r'data\uploads\DIPYeastProteinData.xlsx')
    # path2 = os.path.join(parent_path, r'data\uploads\DIPYeastInteraction.xlsx')
    # 根据MIPS数据集构建的网络
    path1 = os.path.join(parent_path, r'data\dataset\MBD数据库中蛋白质数据.xlsx')
    path2 = os.path.join(parent_path, r'data\dataset\MBD数据库中酵母相互作用.xls')
    data = pd.read_excel(path1)
    data2 = pd.read_excel(path2)
    proteinData = (np.array(data)).tolist()
    proteinEdges = (np.array(data2)).tolist()
    protein_array = []
    for item in proteinData:
        if item[0].__len__() > 1:
            protein_array.append(item[0])

    G = nx.Graph()
    G.add_nodes_from(protein_array)
    G.add_edges_from(proteinEdges,weight = 0)
    print("图已构成")
    return G

#读取亚细胞定位信息加权过后的相互作用
def getSubcellularLocationPPI(parent_path):
    path1 = os.path.join(parent_path, r'data\dataset\proteinSubcellularLocationWeight_MBD.xlsx')
    data1 = pd.read_excel(path1)
    SubcellularLocationPPI = (np.array(data1)).tolist()
    return SubcellularLocationPPI

#获取网络图中每个节点的一阶邻居节点
def get_neigbors(g, node, depth=1):
    layers = dict(nx.bfs_successors(g, source=node, depth_limit=depth))
    nodes = [node]
    list = []
    for i in range(1,depth+1):
        for x in nodes:
            list.append(layers.get(x))
    return list

#读取蛋白质结构域信息加权过后的相互作用
def getDomainPPI(parent_path):
    path1 = os.path.join(parent_path, r'data\dataset\proteinDomainWeight_MBD.xlsx')
    data1 = pd.read_excel(path1)
    DomainPPI = (np.array(data1)).tolist()
    return DomainPPI
if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    #把txt文件转成excel文件
    # txt2xls(r'C:\Users\123\Desktop\夏生荣论文\数据集\MBD酵母数据相互作用.txt',r'C:\Users\123\Desktop\lvguohao\data\dataset\MBD数据库中酵母相互作用')

    # constructNetwork(parent_path)

    G = getGraph(parent_path)
    DomainPPI = getDomainPPI(parent_path)#经过蛋白质结构域信息加权过后的PPI网络
    SubcellularLocationPPI = getSubcellularLocationPPI(parent_path)

    for edge in G.edges():
        sum_weight = 0 #该相互作用的最终加权值
        common_neigbor = 0 #两个节点之间的的共同一阶邻居节点个数
        protein = edge[0]
        neigbor = edge[1]
        protein_degree = G.degree(protein)
        neigbor_degree = G.degree(neigbor)
        DomainWeight = 0
        SubcellularLocationWeight = 0
        #在蛋白质结构域列表中找到匹配的边
        for edge1 in DomainPPI:
            if (edge1[0] == neigbor and edge1[1] == protein) or (edge1[1] == neigbor and edge1[0] == protein):
                DomainWeight = edge1[2]
        #在亚细胞定位列表中找到匹配的边
        for edge2 in SubcellularLocationPPI:
            if (edge2[0] == neigbor and edge2[1] == protein) or (edge2[1] == neigbor and edge2[0] == protein):
                SubcellularLocationWeight = edge2[2]
        protein_neigbor_list = get_neigbors(G,protein,1)
        protein_neigbor_list = protein_neigbor_list[0]
        neigbor_neigbor_list = get_neigbors(G, neigbor, 1)
        neigbor_neigbor_list = neigbor_neigbor_list[0]
        #求出两个蛋白质之间的共同一阶邻居节点
        common_list = list(set(protein_neigbor_list).intersection(set(neigbor_neigbor_list)))
        common_neigbor = common_list.__len__()
        ECC = 0 #边聚集系数
        min_degree = min(protein_degree-1,neigbor_degree-1)
        if min_degree == 0:
            ECC = 0
        else:
            # ECC = math.pow(common_neigbor,3) /min_degree
            ECC = math.pow(common_neigbor, 3) / min_degree
        # sum_weight = ((ECC+1) )*0.01
        # sum_weight = ((ECC + 1)* (DomainWeight+1)) * 0.01
        # sum_weight = ((DomainWeight + 1)) * 0.01
        sum_weight = ((ECC) * (DomainWeight)*(SubcellularLocationWeight)) * 0.01
        # sum_weight = ((ECC )+(DomainWeight)+(SubcellularLocationWeight ))
        # sum_weight = ((SubcellularLocationWeight + 1)) * 0.01
        # print(edge,"的边权值：",sum_weight)
        G[protein][neigbor]['weight'] = sum_weight
    # print(G.edges)
    # print("-------------------------------------")
    G1 = sorted(G.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
    List = []
    for item in G1:
        obj = {}
        obj["protein"] = item[0]
        obj["neigbor"] = item[1]
        obj["weight"] = item[2]["weight"]
        print(obj)
        List.append(obj)

    workbook = xlsxwriter.Workbook('C:\\Users\\123\\Desktop\\lvguohao\\data\\dataset\\finalPPIWeight_MBD.xlsx')
    worksheet = workbook.add_worksheet()
    # 设定格式，等号左边格式名称自定义，字典中格式为指定选项
    # bold：加粗，num_format:数字格式
    bold_format = workbook.add_format({'bold': True})
    # 将二行二列设置宽度为15(从0开始)
    worksheet.set_column(1, 1, 15)
    # 用符号标记位置，例如：A列1行
    worksheet.write('A1', 'protein', bold_format)
    worksheet.write('B1', 'neigbor', bold_format)
    worksheet.write('C1', 'weight', bold_format)
    # worksheet.write('D1', 'SFD_NORMSVi', bold_format)
    # worksheet.write('E1', 'NDT_NORMSVi', bold_format)
    # worksheet.write('F1', 'PVi', bold_format)
    row = 1
    col = 0
    for item in (List):
        # 使用write_string方法，指定数据格式写入数据
        worksheet.write_string(row, col, str(item['protein']))
        worksheet.write_string(row, col + 1, str(item['neigbor']))
        worksheet.write_string(row, col + 2, str(item['weight']))
        # worksheet.write_string(row, col + 3, str(item['SFD_NORMSVi']))
        # worksheet.write_string(row, col + 4, str(item['NDT_NORMSVi']))
        # worksheet.write_string(row, col + 5, str(item['PVi']))
        row += 1
    workbook.close()
