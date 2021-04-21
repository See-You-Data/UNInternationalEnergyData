import pandas as pd

def data_quality_by_column(df_test, column_name, bin_no=10):
    df_working = df_test.copy()
    df_working_sorted = df_working.value_counts(column_name).sort_values(ascending=False)
    quart_list = []
    for i in range(bin_no):
        quart_list.append('q' + str(bin_no - i))
    df_working_qcut = pd.qcut(q=bin_no, x=df_working_sorted, labels=quart_list).to_frame(
        name='country_rank').reset_index()
    df_out = pd.merge(left=df_working, right=df_working_qcut, how='left', on='country_or_area')

    return df_out