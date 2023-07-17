import os
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import xlsxwriter
import gc
# DS<=>D(S)
# D(S,Vi)<=>DSVi
# NDT(S,Vi)<=>NDTSVi
# dj<=>dj
# fdj<=>f(dj)
# SFD(S,Vi)<=>SFDSVi
# NDT_NORM(S,Vi) <=>NDT_NORMSVi
# SFD_NORM(S,Vi)<=>SFD_NORMSVi

#PNi<=>PN(i)  i是亚细胞定位区室
#LSi<=>LS(i)  i是亚细胞定位区室
#SLOCUV <=> SLOC(u,v) 蛋白质u和蛋白质v的共享区室

#计算有相互作用蛋白质之间在蛋白质结构域上的加权信息
def getDomainWeight(result_List):
    dataPath = os.path.join(parent_path, r'data\dataset\yeastDomain.xlsx')
    list = pd.read_excel(dataPath)
    dataList = (np.array(list)).tolist()
    # originalDS = (np.array(list["domain"])).tolist()
    domainList = (np.array(list["domain"])).tolist()
    originalDS = []
    for domain in domainList:
        if domain not in originalDS:
            originalDS.append(domain)

    proteinList = []
    for item in result_List:
        if item[0] not in proteinList:
            proteinList.append(item[0])
        if item[1] not in proteinList:
            proteinList.append(item[1])
#sum_arr:[{'Q0130': 'PF00137|'}, {'YBL099W': 'PF00006|PF00306|PF02874|'}, {'YJR121W': 'PF00006|PF00306|PF02874|'}, {'YAL005C': 'PF00012|'}, {'YLR310C': 'PF00018|PF00617|PF00618|'}, {'YLR335W': 'PF00638|'}, {'YLR347C': 'PF02985|PF03810|'}, {'YNL007C': 'PF00226|PF01556|'}, {'YNL064C': 'PF00226|PF00684|PF01556|'}, {'YNL077W': 'PF00226|PF00684|PF01556|'}, {'YOR151C': 'PF00562|PF04560|PF04561|PF04563|PF04565|PF04566|PF04567|'}, {'YOR160W': 'PF08389|'}, {'YPR010C': 'PF00562|PF04560|PF04561|PF04563|PF04565|PF04567|'}, {'YAL007C': 'PF01105|'}, {'YAR002C-A': 'PF01105|'}, {'YBR183W': 'PF05875|'}, {'YCL025C': 'PF00324|'}, {'YDL054C': 'PF07690|'}, {'YDR101C': 'PF00557|'}, {'YEL063C': 'PF00324|'}, {'YER110C': 'PF03810|'}, {'YGL200C': 'PF01105|'}, {'YGR060W': 'PF04116|'}, {'YHR026W': 'PF00137|'}, {'YHR110W': 'PF01105|'}, {'YLR342W': 'PF02364|PF14288|'}, {'YML012W': 'PF01105|'}, {'YMR290C': 'PF00270|PF00271|PF13959|'}, {'YNL130C': 'PF01066|'}, {'YAL012W': 'PF01053|'}, {'YJR091C': 'PF00076|PF00806|'}, {'YAL013W': 'PF08598|'}, {'YNL330C': 'PF00850|'}, {'YAL014C': 'PF05739|'}, {'YER133W': 'PF00149|'}, {'YAL015C': 'PF00730|'}, {'YBR127C': 'PF00006|PF00306|PF02874|'}, {'YCL018W': 'PF00180|'}, {'YCL064C': 'PF00291|'}, {'YDL029W': 'PF00022|'}, {'YDL059C': 'PF04098|'}, {'YEL030W': 'PF00012|'}, {'YEL060C': 'PF00082|PF05922|'}, {'YFL037W': 'PF00091|PF03953|'}, {'YFL039C': 'PF00022|'}, {'YGR282C': 'PF00332|'}, {'YJL088W': 'PF00185|PF02729|'}, {'YJR068W': 'PF00004|PF08542|'}, {'YJR077C': 'PF00153|'}, {'YML085C': 'PF00091|PF03953|'}, {'YMR058W': 'PF00394|PF07731|PF07732|'}, {'YMR214W': 'PF00226|PF00684|PF01556|'}, {'YNL037C': 'PF00180|'}, {'YPR110C': 'PF01000|PF01193|'}, {'YAL016W': 'PF02985|'}, {'YDL134C': 'PF00149|'}, {'YDL188C': 'PF00149|'}, {'YFR024C-A': 'PF00018|PF04366|'}, {'YGL190C': 'PF00400|'}, {'YGR281W': 'PF00005|PF00664|'}, {'YHR082C': 'PF00069|'}, {'YHR135C': 'PF00069|'}, {'YJL020C': 'PF00018|'}, {'YLR191W': 'PF00018|'}, {'YML109W': 'PF08632|'}, {'YMR109W': 'PF00018|PF00063|PF06017|'}, {'YNR032W': 'PF00149|'}, {'YOL113W': 'PF00069|PF00169|PF00786|'}, {'YAL019W': 'PF00176|PF00271|'}, {'YBL088C': 'PF00454|PF02260|'}, {'YBR084W': 'PF00763|PF01268|PF02882|'}, {'YBR160W': 'PF00069|'}, {'YJL124C': 'PF01423|'}, {'YOL045W': 'PF00069|'}, {'YAL021C': 'PF03372|PF12799|'}, {'YBR072W': 'PF00011|'}, {'YDL165W': 'PF04153|'}, {'YDR171W': 'PF00011|'}, {'YDR188W': 'PF00118|'}, {'YDR190C': 'PF06068|'}, {'YER068W': 'PF13893|'}, {'YFL028C': 'PF00005|'}, {'YGL048C': 'PF00004|'}, {'YGR086C': 'PF13805|'}, {'YGR092W': 'PF00069|PF00433|'}, {'YGR155W': 'PF00291|PF00571|'}, {'YJL130C': 'PF00117|PF00185|PF00289|PF00988|PF02142|PF02729|PF02786|PF02787|'}]
    sum_arr = []  # 存储所有蛋白质对应的域结构信息 [{'Q0045':'PF0015|'}....]
    tem1 = []
    for item1 in proteinList:
        if item1 not in tem1:
            obj = {}
            str1 = ""
            for item2 in dataList:
                if item1 == item2[0]:
                    str1 += item2[1] + "|"
            obj[item1] = str1
            sum_arr.append(obj)
            tem1.append(item1)
    print("sum_arr:",sum_arr)
    DS = []  # 酵母的所有蛋白质域集合
    for i in originalDS:
        if i not in DS:
            DS.append(i)
    # print(DS)
    result_dict = []
    max_SFD = 0
    min_SFD = 1
    max_NDT = 0
    min_NDT = 1
    for i in range(0, sum_arr.__len__()):
        obj = {}
        domainStr = sum_arr[i][tem1[i]]
        domainArr = domainStr.split("|")  # 每一个蛋白质的结构域列表
        SFDSVi = 0  # 蛋白质Vi中的蛋白质域信息存在于其他蛋白质个数中的倒数和
        NDTSVi = domainArr.__len__() - 1
        for item3 in domainArr:
            subSFDSVi = 0
            if item3 != "":
                for j in range(0, sum_arr.__len__()):
                    likePercent = fuzz.partial_ratio(item3, sum_arr[j][tem1[j]])
                    if likePercent == 100:
                        subSFDSVi += 1
                # print(item1,":::",subSFDSVi)
                if subSFDSVi == 1:
                    SFDSVi += 0
                else:
                    SFDSVi += (1 / (subSFDSVi-1))
        # print(tem1[i],"----",SFDSVi,"----",NDTSVi)
        if max_SFD < SFDSVi:
            max_SFD = SFDSVi
        if min_SFD > SFDSVi:
            min_SFD = SFDSVi
        if max_NDT < NDTSVi:
            max_NDT = NDTSVi
        if min_NDT > NDTSVi:
            min_NDT = NDTSVi
        obj["protein"] = tem1[i]
        obj["SFDSVi"] = SFDSVi
        obj["NDTSVi"] = NDTSVi
        result_dict.append(obj)
        # print(result_dict)
        # print("max_SFD:",max_SFD,"|","min_SFD:",min_SFD)
        # print("max_NDT:", max_NDT, "|", "min_NDT:", min_NDT)

        # 计算各个蛋白质归一化之后的NDT和SFD
    for item in result_dict:
        protein = item["protein"]
        SFDSVi = item["SFDSVi"]
        NDTSVi = item["NDTSVi"]
        SFD_NORMSVi = (SFDSVi - min_SFD) / (max_SFD - min_SFD)
        NDT_NORMSVi = (NDTSVi - min_NDT) / (max_NDT - min_NDT)
        item["SFD_NORMSVi"] = SFD_NORMSVi
        item["NDT_NORMSVi"] = NDT_NORMSVi
        # print("SFD_NORMSVi:",SFD_NORMSVi,"----","NDT_NORMSVi:",NDT_NORMSVi)
        # print(item)

        # 计算每个蛋白质最终在蛋白质结构域信息上的重要程度
    for item in result_dict:
        PVi = (item["NDT_NORMSVi"]+1) * (item["SFD_NORMSVi"]+1)
        item["PVi"] = PVi

    print(result_dict)
    return result_dict

#计算有相互作用蛋白质之间在亚细胞定位上的加权信息
def getSubcellularLocationWeight(result_List):
    dataPath = os.path.join(parent_path, r'data\dataset\yeastSubcellularLocalization.xls')
    # dataPath = os.path.join(parent_path, r'data\dataset\subcellularLocation_0302.xlsx')
    list = pd.read_excel(dataPath)
    PPIList = result_List  #蛋白质相互作用数据
    Subcellularlist = (np.array(list)).tolist()
    dataList = (np.array(list)).tolist() #蛋白质的亚细胞定位信息

    proteinList = []
    for item in result_List:
        if item[0] not in proteinList:
            proteinList.append(item[0])
        if item[1] not in proteinList:
            proteinList.append(item[1])

    subcellularLocalization = ['Endoplasmic', 'Cytoskeleton', 'Golgi', 'Cytosol', 'Vacuole', 'Mitochondrion',
                               'Endosome', 'Plasma', 'Nucleus', 'Peroxisome', 'Extracellular']  # 11个亚细胞定位区室

    # print("proteinList:",proteinList)
    LSiArr = [] #存储11个亚细胞定位区室的重要性 [{'subcellularName': 'Endoplasmic', 'subcellularImportance': 0.6809815950920245}, {'subcellularName': 'Cytoskeleton', 'subcellularImportance': 1.3872340425531915}, {'subcellularName': 'Golgi', 'subcellularImportance': 0.7418032786885246}..]
    for item in subcellularLocalization:
        proteinArr = []
        obj = {}
        obj["subcellularName"] = item
        LSi = 0  # 每一个亚细胞定位区室的重要性
        PIi = 0  # 该亚细胞定位区室中蛋白质相互作用的数量
        for i in range(0, dataList.__len__()):
            p = dataList[i][1].split("'")
            protein = dataList[i][0].split("'")[0]
            if item == p[0] and protein not in proteinArr:
                proteinArr.append(protein)
        # print(proteinArr)
        # print("该区室下对应的蛋白质数量为：",proteinArr.__len__())
        for item1 in PPIList:
            if item1[0] in proteinArr and item1[1] in proteinArr:
                PIi += 1
        PNi = proteinArr.__len__()
        LSi = PIi / PNi
        obj["subcellularImportance"] = LSi
        # print("亚细胞定位区室名：",item,"|||","相互作用数量：",PIi,"|||","该区室的重要性：",LSi)
        LSiArr.append(obj)
    # print(LSiArr)
    # print(proteinList)
    Location_List = []
    tem = []
    for i in proteinList:
        if i not in tem:
            tem.append(i)

    for protein in tem:
        obj = {}
        arr = ""
        for item in Subcellularlist:
            if protein == item[0]:
                obj["protein"] = protein.split("'")[0]
                arr += item[1].split("'")[0] + "|"
        obj["Location"] = arr
        Location_List.append(obj)
        # 把蛋白质及其对应的亚细胞定位信息存储
    # generate_excel(Location_List)
    # 读文件
    protein, Location, Location_List = readExcel(parent_path, 'data\\dataset\\Location_List.xlsx')

    SLOCList = []
    for i in range(0, Location_List.__len__()):
        for j in range(0, Location_List.__len__()):
            obj = {}
            if Location_List[i][0] != Location_List[j][0]:
                # 判断蛋白质1和蛋白质2在蛋白质相互作用网络中存在边，是则存储，否则不做操作
                temArr = []
                temArr.append(Location_List[i][0])
                temArr.append(Location_List[j][0])
                temArr1 = []
                temArr1.append(Location_List[j][0])
                temArr1.append(Location_List[i][0])
                if temArr in PPIList or temArr1 in PPIList:
                    del temArr1
                    del temArr
                    gc.collect()
                    obj["protein1"] = Location_List[i][0]
                    obj["protein2"] = Location_List[j][0]
                    tem1 = Location_List[i][1]
                    tem2 = Location_List[j][1]
                    if tem1.__len__() > tem2.__len__():
                        tem = tem1
                        tem1 = tem2
                        tem2 = tem
                        del tem
                        gc.collect()
                    LocationArr = tem1.split("|")
                    arr = ""
                    for k in range(0, LocationArr.__len__() - 1):
                        if LocationArr[k] in tem2:
                            # print("LocationArr的值", LocationArr[k])
                            arr += LocationArr[k] + "|"
                    del tem1
                    del tem2
                    del LocationArr
                    gc.collect()
                    obj["shareLocation"] = arr
                    if obj not in SLOCList:
                        SLOCList.append(obj)
        # print("SLOCList:", SLOCList)
        # print("SLOCList的长度为：",SLOCList.__len__())
        maxLSi = 0

    print("SLOCList:",SLOCList)

    # LSiArr = [{'subcellularName':'Endoplasmic','subcellularImportance':0.23232},{'subcellularName':'Cytoskeleton','subcellularImportance':0.12}]
    for item in SLOCList:
        shareLocation = item["shareLocation"].split("|")
        str1 = 0.01
        # if shareLocation.__len__() > 0:
        for item1 in shareLocation:
            for item2 in LSiArr:
                if item1 == item2["subcellularName"]:
                    str1 += item2["subcellularImportance"]
                    # if item2["subcellularImportance"] > str1:
                    #     str1 = item2["subcellularImportance"]
        # else: #共享区室为空，找该条相互作用两个蛋白质中 最小的区室分数
        #     protein1 = item["protein1"]
        #     protein2 = item["protein2"]
        #     cellLocation_str = ""
        #     for proteinItem in Location_List:
        #         if proteinItem[0] == protein2 or proteinItem[0] == protein1:
        #             cellLocation_str += proteinItem[1]
        #     cellLocation_arr = cellLocation_str.split("|")
        #     for ca in cellLocation_arr:
        #         for Ls in LSiArr:
        #             if ca == Ls["subcellularName"] and Ls["subcellularImportance"] < str1:
        #                 str1 = Ls["subcellularImportance"]
        item["weight"] = str1
    # print("最终的SLOCList:", SLOCList)
    # print("最终的SLOCList的长度:", SLOCList.__len__())
    return SLOCList


# 生成excel文件
def generate_excel(expenses):
    workbook = xlsxwriter.Workbook('C:\\Users\\123\\Desktop\\lvguohao\\data\\dataset\\Location_List.xlsx')
    worksheet = workbook.add_worksheet()
    # 设定格式，等号左边格式名称自定义，字典中格式为指定选项
    # bold：加粗，num_format:数字格式
    bold_format = workbook.add_format({'bold': True})
    # money_format = workbook.add_format({'num_format': '$#,##0'})
    # date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})

    # 将二行二列设置宽度为15(从0开始)
    worksheet.set_column(1, 1, 15)

    # 用符号标记位置，例如：A列1行
    worksheet.write('A1', 'protein', bold_format)
    worksheet.write('B1', 'Location', bold_format)
    # worksheet.write('C1', 'id_1', bold_format)
    # worksheet.write('D1', 'id_1_doc', bold_format)
    # worksheet.write('E1', 'id_2_doc', bold_format)
    # worksheet.write('F1', 'id_2_doc', bold_format)
    row = 1
    col = 0
    for item in (expenses):
        print(item)
        # 使用write_string方法，指定数据格式写入数据
        worksheet.write_string(row, col, str(item['protein']))
        worksheet.write_string(row, col + 1, item['Location'])
        # worksheet.write_string(row, col + 2, str(item['id_1']))
        # worksheet.write_string(row, col + 3, item['id_1_doc'])
        # worksheet.write_string(row, col + 4, str(item['id_2']))
        # worksheet.write_string(row, col + 5, item['id_2_doc'])
        row += 1
    workbook.close()

# 将最终结果写入excel
def result_excel(expenses):
    workbook = xlsxwriter.Workbook('C:\\Users\\123\\Desktop\\lvguohao\\data\\dataset\\PPIWeightResult.xlsx')
    worksheet = workbook.add_worksheet()
    # 设定格式，等号左边格式名称自定义，字典中格式为指定选项
    # bold：加粗，num_format:数字格式
    bold_format = workbook.add_format({'bold': True})
    # money_format = workbook.add_format({'num_format': '$#,##0'})
    # date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})

    # 将二行二列设置宽度为15(从0开始)
    worksheet.set_column(1, 1, 15)

    # 用符号标记位置，例如：A列1行
    worksheet.write('A1', 'protein1', bold_format)
    worksheet.write('B1', 'protein2', bold_format)
    worksheet.write('C1', 'weight', bold_format)
    # worksheet.write('D1', 'id_1_doc', bold_format)
    # worksheet.write('E1', 'id_2_doc', bold_format)
    # worksheet.write('F1', 'id_2_doc', bold_format)
    row = 1
    col = 0
    for item in (expenses):
        # 使用write_string方法，指定数据格式写入数据
        worksheet.write_string(row, col, item['protein1'])
        worksheet.write_string(row, col + 1, item['protein2'])
        worksheet.write_string(row, col + 2, str(item['weight']))
        # worksheet.write_string(row, col + 3, item['id_1_doc'])
        # worksheet.write_string(row, col + 4, str(item['id_2']))
        # worksheet.write_string(row, col + 5, item['id_2_doc'])
        row += 1
    workbook.close()

def readExcel(parent_path,path):
    file = os.path.join(parent_path, path)
    List = pd.read_excel(file)
    Location_List = (np.array(List)).tolist()
    protein = (np.array(List["protein"])).tolist()
    Location = (np.array(List["Location"])).tolist()
    return protein,Location,Location_List

if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    parent_path = os.path.dirname(ROOT_DIR)
    dataPath = os.path.join(parent_path, r'data\dataset\result_List.xlsx')
    list = pd.read_excel(dataPath)
    result_List = (np.array(list)).tolist()
    result_dict = getDomainWeight(result_List) #蛋白质结构域
    SLOCList = getSubcellularLocationWeight(result_List) #亚细胞定位

    workbook = xlsxwriter.Workbook('C:\\Users\\123\\Desktop\\lvguohao\\\data\\dataset\\eachProteinDomainWeight.xlsx')
    worksheet = workbook.add_worksheet()
    # 设定格式，等号左边格式名称自定义，字典中格式为指定选项
    # bold：加粗，num_format:数字格式
    bold_format = workbook.add_format({'bold': True})
    # 将二行二列设置宽度为15(从0开始)
    worksheet.set_column(1, 1, 15)
    # 用符号标记位置，例如：A列1行
    worksheet.write('A1', 'protein', bold_format)
    worksheet.write('B1', 'SFDSVi', bold_format)
    worksheet.write('C1', 'NDTSVi', bold_format)
    worksheet.write('D1', 'SFD_NORMSVi', bold_format)
    worksheet.write('E1', 'NDT_NORMSVi', bold_format)
    worksheet.write('F1', 'PVi', bold_format)
    row = 1
    col = 0
    for item in (result_dict):
        # 使用write_string方法，指定数据格式写入数据
        worksheet.write_string(row, col, str(item['protein']))
        worksheet.write_string(row, col + 1, str(item['SFDSVi']))
        worksheet.write_string(row, col + 2, str(item['NDTSVi']))
        worksheet.write_string(row, col + 3, str(item['SFD_NORMSVi']))
        worksheet.write_string(row, col + 4, str(item['NDT_NORMSVi']))
        worksheet.write_string(row, col + 5, str(item['PVi']))
        row += 1
    workbook.close()

    # 根据 已有的蛋白质结构域信息中的相互作用计算权重
    weightPPI = []
    for item in result_List:
        obj = {}
        protein = item[0]
        PVi1 = 0
        neighbor = item[1]
        PVi2 = 0
        obj["protein"] = protein
        obj["neighbor"] = neighbor
        for item1 in result_dict:
            if item1['protein'] == protein:
                PVi1 = item1["PVi"]
            if item1['protein'] == neighbor:
                PVi2 = item1["PVi"]
        obj["weight"] = (PVi1+PVi2)/2
        if obj not in weightPPI:
            weightPPI.append(obj)
    print(weightPPI)

    workbook = xlsxwriter.Workbook('C:\\Users\\123\\Desktop\\lvguohao\\data\\dataset\\proteinDomainWeight.xlsx')
    worksheet = workbook.add_worksheet()
    # 设定格式，等号左边格式名称自定义，字典中格式为指定选项
    # bold：加粗，num_format:数字格式
    bold_format = workbook.add_format({'bold': True})
    # 将二行二列设置宽度为15(从0开始)
    worksheet.set_column(1, 1, 15)
    # 用符号标记位置，例如：A列1行
    worksheet.write('A1', 'protein', bold_format)
    worksheet.write('B1', 'neighbor', bold_format)
    worksheet.write('C1', 'weight', bold_format)
    # worksheet.write('D1', 'SFD_NORMSVi', bold_format)
    # worksheet.write('E1', 'NDT_NORMSVi', bold_format)
    # worksheet.write('F1', 'PVi', bold_format)
    row = 1
    col = 0
    for item in (weightPPI):
        # 使用write_string方法，指定数据格式写入数据
        worksheet.write_string(row, col, str(item['protein']))
        worksheet.write_string(row, col + 1, str(item['neighbor']))
        worksheet.write_string(row, col + 2, str(item['weight']))
        # worksheet.write_string(row, col + 3, str(item['SFD_NORMSVi']))
        # worksheet.write_string(row, col + 4, str(item['NDT_NORMSVi']))
        # worksheet.write_string(row, col + 5, str(item['PVi']))
        row += 1
    workbook.close()

    workbook = xlsxwriter.Workbook('C:\\Users\\123\\Desktop\\lvguohao\\data\\dataset\\proteinSubcellularLocationWeight.xlsx')
    worksheet = workbook.add_worksheet()
    bold_format = workbook.add_format({'bold': True})
    # 将二行二列设置宽度为15(从0开始)
    worksheet.set_column(1, 1, 15)
    # 用符号标记位置，例如：A列1行
    worksheet.write('A1', 'protein1', bold_format)
    worksheet.write('B1', 'protein2', bold_format)
    worksheet.write('C1', 'weight', bold_format)
    row = 1
    col = 0
    for item in (SLOCList):
        # 使用write_string方法，指定数据格式写入数据
        worksheet.write_string(row, col, str(item['protein1']))
        worksheet.write_string(row, col + 1, str(item['protein2']))
        worksheet.write_string(row, col + 2, str(item['weight']))
        row += 1
    workbook.close()


