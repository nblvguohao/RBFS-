#-*- codeing=utf-8 -*-
#@Time:2021/12/9 8:34
#@Author:lvguohao
#@File:xmlToJson.py
#@software:PyCharm

import os.path
import json
import xml.dom.minidom as xmldom

def readXml(parent_path):
    xmlfilepath = os.path.join(parent_path, r'data\uploads\Scere20170205.xml')
    print("xml文件路径：", xmlfilepath)

    # 得到文档对象
    domobj = xmldom.parse(xmlfilepath)

    # 得到元素对象
    elementobj = domobj.documentElement

    # 获得子标签
    subElementObj_interactor = elementobj.getElementsByTagName("interactor")
    subElementObj_interaction = elementobj.getElementsByTagName("interaction")

    dict = {}
    index = 0
    for content in subElementObj_interactor:
        id = "DIP-" + str(content.getAttribute("id")) + "N"
        child = content.childNodes
        data = [id]
        for i in range(len(child)-2, 0, -2):
            if child[i].nodeName == "organism":
                # if child[i].getAttribute("ncbiTaxId") == "9606":#人类蛋白质
                if child[i].getAttribute("ncbiTaxId") == "4932":#酵母蛋白质
                    continue
                else:
                    break
            if child[i].nodeName == "interactorType":
                nameNodes = child[i].childNodes[1].childNodes
                if nameNodes[1].firstChild.data == "protein":
                    dict[index] = data
                    index += 1
                    continue
                else:
                    break
            if child[i].nodeName == "names":
                nameNodes = child[i].childNodes
                for j in range(len(nameNodes)):
                    if nameNodes[j].firstChild != None:
                        shortName = nameNodes[j].firstChild.data
                        data.append(shortName)
            elif child[i].nodeName == "xref":
                nameNodes = child[i].childNodes
                for j in range(len(nameNodes)):
                    if nameNodes[j].nodeName == "secondaryRef":
                        if nameNodes[j].getAttribute("db") == "uniprot knowledge base":
                            dbid = nameNodes[j].getAttribute("id")
                            data.append(dbid)

    allprotein = {}
    for value in dict.values():
        if len(value) >=3:
            allprotein[value[0]] = [value[1], value[2]]
        else:
            print("error")
    print(len(allprotein))

    edgesDict = {}
    index = 0
    for content in subElementObj_interaction:
        child = content.childNodes
        for i in range(1, len(child), 2):
            if child[i].nodeName == "participantList":
                part_child = child[i].childNodes
                if len(part_child) == 5:
                    first = "DIP-" + part_child[1].childNodes[3].firstChild.data + "N"
                    second = "DIP-" + part_child[3].childNodes[3].firstChild.data + "N"
                    if first in allprotein.keys() and second in allprotein.keys():
                        edgesDict[index] = [first, second]
                        index += 1
                        break
                else:
                    break

    result_path = parent_path + r'\data\uploads\yeast.json' #存储对应的DIP编号、uniprot id、蛋白质名称
    with open(result_path, 'w') as fw:
        json.dump(allprotein, fw)

    edges_path = parent_path + r'\data\uploads\yeastEdges.json'  # 存储蛋白质对应的DIP编号的相互作用
    with open(edges_path, 'w') as fw:
        json.dump(edgesDict, fw)
    return allprotein, edgesDict

#存储文件
def readComplex(parent_path, allprotein, edgesDict):
    # complexfile = os.path.join(parent_path, r'data\uploads\allComplexes.json')
    # with open(complexfile, 'r', encoding='utf8')as fp:
    #     json_data = json.load(fp)
    allpro = {}
    for k, v in allprotein.items():
        allpro[k] = v[1]

    edges = {}
    for key, value in edgesDict.items():
        edges[key] = [allpro[value[0]], allpro[value[1]]]

    pro_path = parent_path + r'\data\uploads\yeastpro.json'  # 存储蛋白质名称和对应的DIP编号
    with open(pro_path, 'w') as fw:
        json.dump(allpro, fw)

    edge_path = parent_path + r'\data\uploads\yeastproEdges.json'  # 存储蛋白质名称的相互作用
    with open(edge_path, 'w') as fw:
        json.dump(edges, fw)

if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    allprotein, edgesDict = readXml(parent_path)
    readComplex(parent_path, allprotein, edgesDict)
