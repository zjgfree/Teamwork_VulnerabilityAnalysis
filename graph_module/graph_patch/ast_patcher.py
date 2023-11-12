from .ast_patch import patch_1, patch_2


def patch_main(ast, node_dict):
    patch_1.patch(ast, node_dict)
    patch_2.patch(ast, node_dict)
