from typing import List, Dict, Tuple
from igraph import *


def traverse(
    node: str,
    edge_dict: Dict[str, List[str]],
    node_dict: Dict[str, Dict[str, str]],
):
    ch_list = edge_dict.get(node, [])
    obj = node_dict[node]
    if (
        obj["_label"] == "CONTROL_STRUCTURE"
        and obj["controlStructureType"] == "FOR"
        and ch_list
    ):
        ch1st = ch_list[0]
        if node_dict[ch1st]["_label"] == "BLOCK":
            ch_list = edge_dict.get(ch1st, []) + ch_list[1:]
            for od, ch in enumerate(ch_list):
                node_dict[ch]["order"] = od + 1
            edge_dict[node] = ch_list

    for ch in ch_list:
        traverse(ch, edge_dict, node_dict)


def patch(ast, node_dict):
    """
        for 循环语句的定义部分被放到了一个 block 下面，
    这个补丁将要删除这个 block 节点。
    """

    traverse(ast.fid, ast.edge_dict, node_dict)
