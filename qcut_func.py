# def qcut_james(x,q,labels):

import math as m
import numpy as np
import pandas as pd

# The purpose of this module is to replicate the qcut function due to issues
# when calling qcut in modules
def qcut_james(x, q, labels=[]):
    ret = x.sort_values(ascending=False)
    col_len = len(ret)

    # The following logic will return a warning if labels is declared but is not
    # equal to the length defined by q.
    # need to make this exit the func rather than set each row to the warning message
    if (len(labels) != q) & (not (not labels)):
        return "labels should be the same length as q"

    # utilizing linspace creates quick boundaries for the grouping function
    bin_boundary = np.linspace(0, col_len, q + 1).astype(int)

    # If labels is declared then the labels are output otherwise the categories are
    # titled 1, 2, ..., q
    if not (not labels):
        bin_no = 1
        ret_categories = []
        for i in range(col_len):
            if i <= bin_boundary[bin_no]:
                ret_categories.append(labels[bin_no-1])
            else:
                bin_no = bin_no + 1
                ret_categories.append(labels[bin_no-1])

    if not labels:
        bin_no = 1
        ret_categories = []
        for i in range(col_len):
            if i <= bin_boundary[bin_no]:
                ret_categories.append(bin_no)
            else:
                bin_no = bin_no + 1
                ret_categories.append(bin_no)

    # .to_frame() turns a series into a dataframe, which can then be appended
    # onto the existing df

    # This is done in order to return a column in the original order rather than
    # a sorted order. There is scope for improvement/ reduction in code here

    x = x.to_frame()
    x = x.assign(
        category=ret_categories
    )

    ret = ret.to_frame()
    ret = ret.assign(
        category=ret_categories
    )

    return [type(ret)]