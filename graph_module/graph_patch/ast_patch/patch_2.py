from typing import List, Dict
from igraph import *


def traverse(
    node: str,
    edge_dict: Dict[str, List[str]],
    node_dict: Dict[str, Dict[str, str]],
    var_dict_list: List[Dict[str, str]],
):
    ch_list = edge_dict.get(node, [])

    obj = node_dict[node]
    label = obj["_label"]
    if label == "BLOCK":
        var_dict_list.append({})
    elif label == "LOCAL":
        var_dict_list[-1][obj["name"]] = node
    elif label == "IDENTIFIER" and obj["refto"] == "LOST":
        var = obj["name"]
        for var_dict in reversed(var_dict_list):
            pos = var_dict.get(var)
            if pos is not None:
                obj["refto"] = pos
                break

    for ch in ch_list:
        traverse(ch, edge_dict, node_dict, var_dict_list)

    if obj["_label"] == "BLOCK":
        var_dict_list.pop()


def patch(ast, node_dict):
    """
        for 循环语句的定义部分被放到了一个 block 下面，
    这个补丁将要修复这一块的 ref 信息。
    """
    traverse(ast.fid, ast.edge_dict, node_dict, [{}])
