import os, shutil
from typing import List
from .joern_server import *
from .joern_parser import *
from config import tc_path, td_path


def move_singlefile_to_tmpdir() -> None:
    """move single file to tmpdir,and keep on the other project dir"""
    if not os.path.exists(td_path):             # 新建一个tmp文件夹
        os.mkdir(td_path)
    for obj in os.listdir(tc_path):             # 遍历testcase2中每个项目文件(夹)
        obj_dir = os.path.join(tc_path, obj)
        if os.path.isfile(obj_dir):             # 将单一文件移动到tmp中，文件夹保留
            shutil.move(obj_dir, td_path)

def exist_out():
    if not os.path.exists("parse_module/parse_result/out1.json"):
        print("out1\n")
        return False
    if not os.path.exists("parse_module/parse_result/out2a.json"):
        print("out2a\n")
        return False
    if not os.path.exists("parse_module/parse_result/out2b.json"):
        print("out2b\n")
        return False
    if not os.path.exists("parse_module/parse_result/out3.json"):
        print("out3\n")
        return False
    if not os.path.exists("parse_module/parse_result/out4.json"):
        print("out4\n")
        return False
    if not os.path.exists("parse_module/parse_result/out5.json"):
        print("out5\n")
        return False
    return True

def parse() -> None:
    move_singlefile_to_tmpdir()
    with open("log.txt","w") as l:      # 记录解析情况
        l.write("开始解析\n")
        client = start_joern_server()           # 新建joern客户端，解析文件
        parse_testcase(client)                  # 获取所需数据
        if exist_out():
            l.write("解析完成\n\n")
        else:
            l.write("解析失败，parse_module/parse_result文件夹中部分out文件未生成\n\n")
    kill_server()
