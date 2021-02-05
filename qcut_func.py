# def qcut_james(x,q,labels):

#brief text to test personal access token
import math as m

def qcut_james(x, q):
    ret = x.sort_values(ascending=False)
    col_len = len(ret)
    # col_len = len(x)
    quart_len = m.floor(col_len / q)
    quart_modulo = col_len % q
    ret_categories = []

    bin_boundary = list()
    bin_cumulative = 0
    for i in range(q):
        if i + 1 <= quart_modulo:
            bin_size = quart_len + 1
        else:
            bin_size = quart_len

        bin_cumulative = bin_cumulative + bin_size
        bin_boundary.append(bin_cumulative)


    bin_no = 1
    for i in range(col_len):
        if i <= bin_boundary[bin_no - 1]:
            ret_categories.append(bin_no)
        else:
            bin_no = bin_no + 1
            ret_categories.append(bin_no)

    # ret.columns()
    
    # return [ret, col_len, quart_len, quart_modulo]
    return ret.columns()
    # return [bin_boundary, ret_categories]