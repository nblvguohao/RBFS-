#-*- codeing=utf-8 -*-
#@Time:2021/12/21 10:21
#@Author:lvguohao
#@File:jsonToExcel.py
#@software:PyCharm
import xlsxwriter
import xlwt, json
def readJsonfile(path):
    jsobj = json.load(open(path))
    return jsobj

# #将yeastpro.json文件转换成excel文件，
def jsonToexcel():
    jsonfile = readJsonfile('C:\\Users\\123\\Desktop\\lvguohao\\data\\uploads\\yeastpro.json')
    # print(jsonfile)
    # print("----------------------------------------------")
    workbook = xlsxwriter.Workbook('C:\\Users\\123\\Desktop\\lvguohao\\data\\uploads\\yeastProtein.xls')
    sheet1 = workbook.add_worksheet('sheet1')
    headings = ["dip-id","id","protein"]
    allKeys = list(jsonfile.keys())
    # print(allKeys)
    # print("--------------------------------------------------")
    sheet1.write_row('A1',headings)
    # print("总键值数：",len(allKeys))
    for i in range(0, len(allKeys)):
        # print("每一个键：",allKeys[i])
        # print("该键对应的值：",jsonfile[allKeys[i]])
        sheet1.write(i+1,0, allKeys[i])#i+1行，0列，allkeys[i]是写入的值
        sheet1.write(i + 1, 1, i+1)
        sheet1.write(i + 1, 2, jsonfile[allKeys[i]])
    workbook.close()

def bubbleSort(arr):
    for i in range(1, len(arr)):
        for j in range(0, len(arr)-i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# #yeastproEdges.json文件转换成excel文件，
def EdgeJsonToexcel():
    jsonfile = readJsonfile('C:\\Users\\123\\Desktop\\lvguohao\\data\\uploads\\yeastproEdges.json')
    workbook = xlsxwriter.Workbook('C:\\Users\\123\\Desktop\\lvguohao\\data\\uploads\\yeastEdgesProtein.xls')
    sheet1 = workbook.add_worksheet('sheet1')
    headings = ["protein",  "neighborProtein"]
    sheet1.write_row('A1', headings)
    allKeys = jsonfile.keys()#json的所有键
    allKeys = sorted(allKeys)
    j = 0
    for i in allKeys:
        j += 1
        # print(jsonfile[i][0],jsonfile[i][1])
        sheet1.write(j,0,jsonfile[i][0])
        sheet1.write(j, 1, jsonfile[i][1])
    workbook.close()





if __name__ == '__main__':
    jsonToexcel()
    EdgeJsonToexcel()