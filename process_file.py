#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os
import time
import sys
import csv
import codecs
import ticket_infofield as tf
# import xml.etree.ElementTree as ET
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET



path = os.getcwd()#获取当前路径
# print(path)
tickket_name = []
t_list = []

def get_file(str1, j):
    '''
    函数功能:首先将目录下的所有XML文件名存入列表，
    然后通过参数的方式遍历每个文件，与配置文件的字段进行比对
    函数参数:
    path: 当前路径
    str1: 目录名称
    j:    XML文件列表的下标,用于后续对目录下所有XML文件的访问
    返回值: 
    all_files[j]: XML文件名
    root：        XML文件根节点
    start_time:   解析XMl文件起始时间
    '''
    all_files = [f for f in os.listdir(str1)]     #输出根path下的所有文件名到一个列表中
                                                                
    tree = ET.ElementTree()             #实例化
    # print(all_files)                  #'xml2019081210-1'
    # print(len(all_files))
    all_files.sort(key=lambda x: int(x.split('-')[1][:]))       #文件排序
    
    xml_file = './cp02_input/' + all_files[j]
    # print("xml_file:", xml_file)
    
    tree.parse(xml_file)                #解释文档
    root = tree.getroot()               #获取所有节点
    # print(root.tag)                   #获取第一个标签 
    for i in root[1][1]:
        # print(i.text)
        tickket_name.append(i.text)
    # print(tickket_name)
    if set(tf.tickket_infofield) <= set(tickket_name):          #集合比较
        print("可以解析")
        start_time = time.asctime()
        return all_files[j], root, start_time
        # print(start_time)   
    else:
        print("无法解析,当前文件错误")
        return
    



 
def get_FileSize(filePath):
    '''
    函数功能:提取XML文件大小
    函数参数:
    filePath:   XML文件名 
    返回值: fsize 保留小数点后两位
    '''
 
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024)
 
    return round(fsize, 2)





def open_csv(path,root):
    '''
    函数功能:写入标题, 写入XML数据
    函数参数:
    path: 写入csv文件的路径
    root: XML根节点
    返回值:
    return: 成功返回 0, 失败返回1
    end_time: 写入XML文档的结束时间
    '''
    with open(path, 'w+', encoding='gbk') as f:


        title = ','.join(tf.tickket_infofield)
        tic_name = title + '\n'
        f.write(tic_name)           #写标题
        try:
            all_data = insert_data(root)
            for i in range(len(all_data)):
                del all_data[i][6]              #删除字段被写死, 可待优化
                data = ','.join(all_data[i])
                inser_data = data + '\n'

                f.write(inser_data)         #写数据
            end_time = time.asctime()    
            return 0, end_time
        except:
            print("写入数据失败")
            return 1
        





def deal_info(sq_id,pro_result, onexml_path, csv_path, start_time, end_time):
    '''
    函数功能: 处理每XML文档的详细数据, 记录值并将每条csv数据处理记录存入列表并返回
    sq_id: 每条XML转存cvs文件的记录值id
    pro_result: 处理结果 成功为0, 失败为1
    onexml_path: 存放XML文件的目录和文件名
    csv_path: 存放csv文件的目录和文件名
    start_time: 开始处理XML文件的时间
    end_time: 处理结束csv文件的时间
    返回值:
    return: info_list 每条记录的列表
    '''

    # allinfo_list = []
    # print("pro_result:", pro_result)
    Xml_file_size = get_FileSize(onexml_path)            #xml文件大小
    input_xml_path = os.path.abspath(onexml_path)         #xml绝对路径
    output_csv_path = os.path.abspath(csv_path)           #csv绝对路径
    
    # time1 = start_time
    # print("文件大小：%.2f KB"%(Xml_file_size))
    # print("xml绝对路径:", input_xml_path)
    # print("csv_path绝对路径:", output_csv_path)
    # print("处理xml文件的时间:", start_time)
    # print("处理csv文件的时间", end_time)
    
    info_list = [str(sq_id),str(pro_result),
                str(Xml_file_size),
                input_xml_path,
                output_csv_path,
                start_time,
                end_time]
    
    # print(info_list)
    # allinfo_list.append(info_list)
    # print(allinfo_list)
    
    return info_list


def func(listTemp, n):
    '''
    函数功能: 将每个XML文件的ticket_data数据列表进行分割
    函数参数:
    listTemp: 为XML文件的ticket_data部分的数据列表
    n:        平分后每份列表的的个数
    '''
    for i in range(0, len(listTemp), n):
        yield listTemp[i:i + n]



def insert_data(root_path):
    '''
    函数功能:遍历XML文档根节点下的数据并存入列表，调用func函数并对其进行拆分
    为每个用户的八个字段的列表
    函数参数:
    root_path: XML文件根节点
    返回值:
    all_data: 返回每个XML文件数据的列表
    '''
    xml_list = []
    tic_data = []
    all_data = []
    # for i in range
    for xml in root_path[1][2]:
        # print(data.tag)
        xml_list.append(xml.tag)
        # print(len(data.tag))
    # print(len(xml_list))
    for i in range(len(xml_list)):
        for data in root_path[1][2][i]:
            # print(data.text)                    #得到每个用户的八个字段
            tic_data.append(data.text)
    temp = func(tic_data, 8)             # 返回的temp为平分后的每份可迭代对象
    for i in temp:
        # print(i)
        all_data.append(i)
    # print(len(all_data))
    return all_data
    # for j in range(len(tf.tickket_infofield)+1):
    #     one_data.append(tic_data[j])
        # print(tic_data[j])
    # print(one_data)
    # print(len(tf.tickket_infofield))
    # print(len(tic_data))


def main():
    '''
    函数功能:对所有功能进行整合
    '''

    xml_path = input("请输入待解析文件路径:")
    csv_pa = input("请输入解析后路径:")
    # xml_path = "cp02_input"
    file_abs_path = os.path.abspath(xml_path)
    csv_abspath = os.path.abspath(csv_pa)
    if not os.path.exists(csv_abspath):
        os.mkdir(csv_abspath)


    all_files = [f for f in os.listdir(file_abs_path)]
    # all_files = [f for f in os.listdir(path + '\\' + xml_path)]
    print(type(all_files))          #<class 'list'>


    csv_info_path = csv_abspath + '\\' + 'xml-handle-log-uuid.csv'



    with open(csv_info_path, 'a+', encoding='gbk') as f:       #写入输出信息表的标题
        info_titie = ['sequence_id',
                'process result',
                'xml-file-size',
                'input xml-path',
                'output-csv-path',
                'start time',
                'end time']

        info_title = ','.join(info_titie)
        tic_name = info_title + '\n'
        f.write(tic_name) 

    for i in range(len(all_files)):
        
        file_name, root, start_time= get_file(file_abs_path,i)
        # print("file_name:", file_name)
        onexml_path = './cp02_input/' + file_name
        csv_path = csv_abspath + '\\' + file_name + '.csv'
        print(csv_path)
        # insert_data(root)
        pro_result,  end_time = open_csv(csv_path,root)
        info_list = deal_info(i, pro_result, onexml_path, csv_path, start_time, end_time)
        # print(info_list)
        with open(csv_info_path, 'a+', encoding='gbk') as f:

            one_info = ','.join(info_list)
            ev_info = one_info + '\n'
        # print(info_list)
            f.write(ev_info)


if __name__ == "__main__":
    main()