#-*- codeing=utf-8 -*-
#@Time:2021/12/7 20:58
#@Author:lvguohao
#@File:getPPIData.py
#@software:PyCharm
from xml.dom import minidom
import re
import os

class get_xml():
  #加载获取xml的文档对象
  def __init__(self,address):
    #解析address文件，返回DOM对象，address为文件地址
    self.doc = minidom.parse(address)
    #DOM是树形结构，_get_documentElement()获得了树形结构的根节点
    self.root = self.doc._get_documentElement()
    #.getElementsByTagName()，根据name查找根目录下的子节点
    self.interactor = self.root.getElementsByTagName('interactor')


  def getxmldata(self):
    data_list=[]
    j = 0
    shortLabel = self.root.getElementsByTagName("shortLabel")
    organism = self.root.getElementsByTagName("organism")
    ex = {}
    for i in self.interactor:
      j = j+1
      if j % 2 == 0:
          ex = {}
      #getAttribute()，获取DOM节点的属性的值
      # ncbiTaxId = organism.getAttribute("ncbiTaxId")
      b = shortLabel[j].firstChild.data
      # print(j)
      if b is not None:
        if j % 2 == 1:
            ex['protein'] = b
            d = "protein:"+b
            # data_list.append({"protein:",b})
        else:
            d = "organism:"+b
            ex['organism'] = b
            data_list.append(ex)
    return data_list

#导出excel
import xlwt
import json
def importexcel(match,dest_filename):
    # 创建excel工作表
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')

    # 设置表头
    worksheet.write(0, 0, label='protein')
    worksheet.write(0, 1, label='organism')
    # worksheet.write(0, 2, label='ID')
    # worksheet.write(0, 3, label='OTHER')
    # 读取json文件
    # with open('test.json', 'r') as f:
    #     data = json.load(f)
    data = match
    # 将json字典写入excel
    # 变量用来循环时控制写入单元格，感觉有更好的表达方式
    val1 = 1
    val2 = 1
    for list_item in data:
        print(list_item)
        for key, value in list_item.items():
            print(key,"---",value)
            if key == "protein":
                worksheet.write(val1, 0, value)
                val1 += 1
            elif key == "organism":
                if value == 'Saccharomyces cerevisiae':
                    worksheet.write(val2, 1, value)
                    val2 += 1
            else:
                pass

    # 保存
    workbook.save("C:\\Users\\123\\Desktop\\lvguohao\\数据集\\protein.xlsx")

if __name__ == '__main__':
    obj = get_xml("C:\\Users\\123\\Downloads\\Scere20170205.mif25");
    list = obj.getxmldata();
    print(list)
    importexcel(list,"C:\\Users\\123\\Desktop\\lvguohao\\数据集\\protein.xlsx")
    # print(list.__len__())

