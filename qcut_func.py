# def qcut_james(x,q,labels):

import math as m
import numpy as np

# The purpose of this module is to replicate the qcut function due to issues
# when calling qcut in modules
def qcut_james(x, q, labels=[]):
    ret = x.sort_values(ascending=False)
    col_len = len(ret)
    quart_len = m.floor(col_len / q)
    quart_modulo = col_len % q


    if (len(labels) != q) & (not (not labels)):
        return "labels should be the same length as q"

    # utilizing linspace creates quick boundaries for the grouping function
    bin_boundary = np.linspace(0, col_len, q + 1).astype(int)

    bin_no = 1
    ret_categories = []
    for i in range(col_len):
        if i <= bin_boundary[bin_no]:
            ret_categories.append(bin_no)
        else:
            bin_no = bin_no + 1
            ret_categories.append(bin_no)


    ret = ret.to_frame()
    ret = ret.assign(
        category = ret_categories
    )



    # ret.columns()
    # return [ret, col_len, quart_len, quart_modulo]
    # return ret.columns()
    # return [bin_boundary, ret_categories]
    return [ret]