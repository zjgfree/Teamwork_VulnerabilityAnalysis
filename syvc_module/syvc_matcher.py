from data_module.db_access import *
from data_module.method_set import *

def fc_matcher(node, node_dict):
    obj = node_dict[node]
    return obj["_label"] == "CALL" and obj["name"] in fc_matcher.sensitive_func


fc_matcher.sensitive_func = load_from_pickle(f"./syvc_module/sensitive_func.db")


def array_matcher(node, node_dict, ast):
    """ 数组筛选：下标不是常数时才考虑 """
    obj = node_dict[node]
    return (
        obj["_label"] == "CALL" 
        and obj["methodFullName"] == "<operator>.indirectIndexAccess"
        and not all(isConstant(node_dict[sub]) for sub in  ast.get_leaves(ast.edge_dict.get(node, [])[-1]))
    )

def pointer_matcher(node, node_dict, ast):
    """
    指针越界
    考虑：p+-len, p+-=len的情况，其中p为指针
    判断：为加减或assignmentPlus/Minus，左为指针。
    关键变量：p和len
    """
    obj = node_dict[node]
    child = ast.edge_dict.get(node, [])
    if (
        obj["_label"] == "CALL"
        and obj["methodFullName"] in ["<operator>.addition", "<operator>.subtraction", "<operator>.assignmentPlus", "<operator>.assignmentMinus"]
        and "*" in node_dict[child[0]]["typeFullName"]
    ):
        return True
    return False

def integerOverflow(node, node_dict, ae_flag, ast):
    """整数溢出"""
    obj = node_dict[node]
    child = ast.edge_dict.get(node, [])
    return (
        not ae_flag
        and obj["_label"] == "CALL"
        and (
            # 乘除左移的情况：直接考虑，因为一般只有int才会进行这种运算。
            obj["methodFullName"] in ae_func_1
            # 对加减的情况：左侧操作数为int或无法判断类型，且将 a+=2 类似的情况去除，因为这种太多且很少有漏洞。2的标签为"Literal"
            or obj["methodFullName"] in ae_func_2
            and node_dict[child[0]]["typeFullName"] in int_types
        )
        # 必须包含至少两个变量
        and list(isConstant(node_dict[sub]) for sub in  ast.get_leaves(node)).count(False) >= 2
    )

def NPD_matcher(node, node_dict):
    """CWE-476 NULL Pointer Dereference 空指针解引用"""
    obj = node_dict[node]
    return (
        obj["_label"] == "CALL"
        and obj["methodFullName"] == "<operator>.indirectFieldAccess"
        and "->" in obj["code"]
    )

def pathTraversal_matcher(node, node_dict, ast):
    """CWE-22 路径函数：通过关键字匹配"""
    obj = node_dict[node]
    key_list = [
        "open", "read", "mkdir", "append", "setPorperty"
    ]
    return (
        obj["_label"] == "CALL"
        and any(key in obj["methodFullName"] for key in key_list)
        and "thread" not in obj["methodFullName"]   # 用 read 时包含了它
        # 函数必须要有变量参数
        and not all(isConstant(node_dict[sub]) for sub in  ast.get_leaves(node))
    )

def divideByZero_matcher(node, node_dict, ast):
    """CWE-369 divide-by-zero error"""
    obj = node_dict[node]
    key_list = [
        "<operator>.division", "<operator>.assignmentDivision", "<operator>.modulo", "<operators>.assignmentModulo", "DIV"
    ]
    return (
        obj["_label"] == "CALL"
        and obj["methodFullName"] in key_list
        # 排除分母全是常量的情况
        and not all(isConstant(node_dict[sub]) for sub in ast.get_leaves(ast.edge_dict.get(node, [])[-1]))
    )

def assert_matcher(node, node_dict, ast):
    '''CWE-617 可达断言匹配, 通过关键字匹配'''
    obj = node_dict[node]
    key_list = [
        "assert", "BUG", "OVS_NOT_REACHED", "validate_as_request"
    ]
    return (
        obj["_label"] == "CALL"
        and any(key in obj["methodFullName"] for key in key_list)
        # 函数必须要有变量参数
        and not all(isConstant(node_dict[sub]) for sub in  ast.get_leaves(node))
    )

def free_matcher(node,node_dict, ast):
    '''CWE-415,CWE-416 UAF与DoubleFree'''
    obj = node_dict[node]
    key_list = ['free','delete','realloc','unregister','Destroy','close', 'RELEASE']
    return (
        obj["_label"] == "CALL"
        and any(key in obj["methodFullName"] for key in key_list)
        # 函数必须要有变量参数
        and not all(isConstant(node_dict[sub]) for sub in  ast.get_leaves(node))
    )